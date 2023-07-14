import argparse
import json
import logging
import sys
from pprint import pprint
from socket import socket, AF_INET, SOCK_STREAM
from sys import argv
from common.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, GUEST,\
    DEFAULT_PORT, MAX_CONNECTIONS, RESPONSE, ERROR, BAD_REQUEST, \
    LOW_PORT_RANGE, HIGH_PORT_RANGE, SRV_LOGGER, SRV_PORT_KEY, SRV_ADDR_KEY
from common.utils import get_message, send_message
from common.decorators import logging_deco
# подтягиваем готовый конфиг логгера
import logs.configs.server_log_config
from common.decorators import logging_deco

# запуск логирования сервера (получаем серв. логгер из файла конфига)
LOGGER = logging.getLogger(SRV_LOGGER)


@logging_deco
def process_client_message(message: dict) -> dict:
    """
    Обрабатывает сообщения от клиентов, принимает словарь по протоколу JIM,
    проверяет корректность и возвращает словарь-ответ для клиента тоже в JIM
    :param message: словарь-сообщение клиента по протоколу JIM
    :return: ответ клиенту - словарь по протоколу JIM
    """
    # валидация словаря на соотв. протоколу JIM
    # должен содержать ключ действия, само действие - "присутствие",
    # должен содержать ключ "время" и "пользователь" (с именем "Гость")
    if ACTION in message and \
            message[ACTION] == PRESENCE and \
            TIME in message and \
            USER in message and \
            ACCOUNT_NAME in message[USER] and \
            message[USER][ACCOUNT_NAME] == GUEST:
        # если все соответствует - отвечаем 200 (ок)
        return {RESPONSE: 200}
    # если не все хорошо - отдаем ошибку о несоотв. формате и логируем
    response = {
        RESPONSE: 400,
        ERROR: BAD_REQUEST
    }
    LOGGER.error(f'Сообщение не в формате протокола JIM. Ответ: {response}')
    return response


def create_arg_parser():
    """
    Парсер аргументов командной строки
    :return:
    """
    # создаем объект парсера и вытаскиваем по ключам адрес и порт
    parser = argparse.ArgumentParser()
    # если порт не задан явно - используем по умолчанию из конфига
    parser.add_argument(SRV_PORT_KEY, default=DEFAULT_PORT, type=int, nargs='?')
    # если адрес не задан явно - будем слушать всё
    parser.add_argument(SRV_ADDR_KEY, default='', nargs='?')
    return parser


def main() -> None:
    """
    Загрузка параметров командной строки, если параметры не переданы - задаются
    значения по умолчанию
    Пример запуска скрипта с заданием порта и адреса:
    server.py -p 1234 -a 192.168.99.99
    :return: None
    """

    # логируем параметры - запуска сервера
    LOGGER.debug(f'Запуск сервера с параметрами: {argv[1:]}')

    # создаём парсер и передаем для разбора параметры (без имени самого файла)
    parser = create_arg_parser()
    try:
        namespace = parser.parse_args(sys.argv[1:])
    except Exception as err:
        LOGGER.critical(f'Ошибка обработки параметров запуска сервера: {err}')
        exit(1)
    # сохраняем распарсенные адрес и порт, заданные в параметрах запуска скрипта
    listen_addr = namespace.a
    listen_port = namespace.p

    # логируем параметры - адрес и порт запуска сервера
    LOGGER.debug(f'порт сервера: {listen_port}, адрес сервера: {listen_addr}')

    # проверяем, чтобы номер порта был релевантным
    try:
        if listen_port < LOW_PORT_RANGE or listen_port > HIGH_PORT_RANGE:
            raise ValueError
    except ValueError as err:
        # логируем ошибку "некорректный номер порта"
        LOGGER.critical(f'Номер порта может быть только числом в диапазоне '
                        f'от {LOW_PORT_RANGE} до {HIGH_PORT_RANGE}. '
                        f'Получено: "{listen_port}".\nОшибка: {err}')
        exit(2)

    # создаем (сетевой, потоковый) сокет, привязываем его и начинаем слушать
    JIM_socket = socket(AF_INET, SOCK_STREAM)
    JIM_socket.bind((listen_addr, listen_port))
    JIM_socket.listen(MAX_CONNECTIONS)

    # т.е. это сервер - основной цикл запускаем в бесконечном варианте
    while True:
        # при поступлении запроса - принимаем объект клиентского сокета и адрес
        client_sock, client_addr_port = JIM_socket.accept()
        client_addr, client_port = client_addr_port
        LOGGER.info(f'Установлено соединение с клиентом, '
                    f'адрес: {client_addr=}, порт: {client_port=}')

        try:
            message_from_client = get_message(client_sock)
            # полученные из сокета байты - возвращаются в виде словаря
            LOGGER.info(f'Полученное сообщение от клиента: '
                        f'{message_from_client}')
            # разбираем полученный словарь на служ. инфо JIM и само сообщение
            response = process_client_message(message_from_client)
            send_message(client_sock, response)
            LOGGER.info(f'Клиенту отправлен ответ: {response}')
            client_sock.close()  # после отправки ответа - закрываем кл. сокет
            LOGGER.info('Соединение с клиентом закрыто!')
        except(ValueError, json.JSONDecodeError) as err:
            LOGGER.error(f'Получено некорректное сообщение от клиента '
                         f'{client_addr_port}, ошибка: {err}')
            client_sock.close()


if __name__ == '__main__':
    main()
