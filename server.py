import json
import logging
from pprint import pprint
from socket import socket, AF_INET, SOCK_STREAM
from sys import argv
from common.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, GUEST,\
    DEFAULT_PORT, MAX_CONNECTIONS, RESPONSE, ERROR, BAD_REQUEST, \
    LOW_PORT_RANGE, HIGH_PORT_RANGE, SRV_LOGGER
from common.utils import get_message, send_message
import logs.configs.server_log_config

# запуск логирования сервера (получаем серв. логгер из файла конфига)
SRV_LOGGER = logging.getLogger(SRV_LOGGER)


def process_client_message(message: dict) -> dict:
    """
    Обрабатывает сообщения от клиентов, принимает словарь по протоколу JIM,
    проверяет корректность и возвращает словарь-ответ для клиента тоже в JIM
    :param message: словарь-сообщение клиента по протоколу JIM
    :return: ответ клиенту - словарь по протоколу JIM
    """
    # логируем пришедшее на разбор сообщение клиента (на уровне debug)
    SRV_LOGGER.debug(f'Обработка сообщения от клиента: {message}')

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
        # и логируем это на уровне "инфо"
        response = {RESPONSE: 200}
        SRV_LOGGER.info(f'Сообщение корректное. Ответ: {response}')
        return response
    # если не все хорошо - отдаем ошибку о несоотв. формате и логируем
    response = {
        RESPONSE: 400,
        ERROR: BAD_REQUEST
    }
    SRV_LOGGER.error(f'Сообщение не в формате протокола JIM. Ответ: {response}')
    return response


def main() -> None:
    """
    Загрузка параметров командной строки, если параметры не переданы - задаются
    значения по умолчанию
    Пример запуска скрипта с заданием порта и адреса:
    server.py -p 1234 -a 192.168.99.99
    :return: None
    """

    PORT = '-p'  # ключ для передачи номера порта
    ADDR = '-a'  # ключ для передачи адреса для прослушивания

    # логируем параметры - запуска сервера
    SRV_LOGGER.debug(f'Запуск сервера с параметрами: {argv[1:]}')

    # устанавливаем порт для прослушивания (по умолчанию или заданны)
    try:
        params = argv[1:]  # имя самого скрипта откидываем - только пар-ры
        if PORT in params:
            # сам номер порта - следующее значение после параметра '-p'
            port_num_str = params[params.index(PORT) + 1]
            listen_port = int(port_num_str)
        else:
            listen_port = DEFAULT_PORT

        # логируем параметры - порт запуска сервера
        SRV_LOGGER.debug(f'- порт сервера: {listen_port}')

        # проверяем, чтобы номер порта был релевантным
        if listen_port < LOW_PORT_RANGE or listen_port > HIGH_PORT_RANGE:
            raise ValueError
    except IndexError as err:
        # логируем ошибку "не указан номер порта"
        SRV_LOGGER.critical(f'После параметра "{PORT}" нужно указать номер '
                            f'порта: {err}')
    except ValueError as err:
        # логируем ошибку "некорректный номер порта"
        SRV_LOGGER.critical(f'Номер порта может быть только числом в диапазоне '
                            f'от {LOW_PORT_RANGE} до {HIGH_PORT_RANGE}. '
                            f'Получено: "{port_num_str}".\nОшибка: {err}')
        exit(1)

    # устанавливаем адрес для прослушивания
    try:
        if ADDR in params:
            # сам номер порта - след. значение после параметра '-a'
            listen_addr = params[params.index(ADDR) + 1]
        else:
            listen_addr = ''  # если не задан - слушаем все

    except IndexError as err:
        SRV_LOGGER.critical(f'После параметра "{ADDR}" не указан IP-адрес для '
                            f'прослушивания сервером: {err}')
        exit(2)

    # логируем параметры - адрес запуска сервера
    SRV_LOGGER.debug(f'- адрес сервера: {listen_addr}')

    # создаем (сетевой, потоковый) сокет, привязываем его и начинаем слушать
    JIM_socket = socket(AF_INET, SOCK_STREAM)
    JIM_socket.bind((listen_addr, listen_port))
    JIM_socket.listen(MAX_CONNECTIONS)

    # т.е. это сервер - основной цикл запускаем в бесконечном варианте
    while True:
        # при поступлении запроса - принимаем объект клиентского сокета и адрес
        client_sock, client_addr_port = JIM_socket.accept()
        client_addr, client_port = client_addr_port
        SRV_LOGGER.info(f'Установлено соединение с клиентом, '
                        f'адрес: {client_addr=}, порт: {client_port=}')

        try:
            message_from_client = get_message(client_sock)
            # полученные из сокета байты - возвращаются в виде словаря
            # print('Полученное сообщение от клиента:')
            # pprint(message_from_client)
            SRV_LOGGER.info(f'Полученное сообщение от клиента: '
                            f'{message_from_client}')
            # разбираем полученный словарь на служ. инфо JIM и само сообщение
            response = process_client_message(message_from_client)
            send_message(client_sock, response)
            # print('Клиенту отправлен ответ:')
            # pprint(response)
            SRV_LOGGER.info(f'Клиенту отправлен ответ: {response}')
            client_sock.close()  # после отправки ответа - закрываем кл. сокет
            # print('Соединение с клиентом закрыто!\n')
            SRV_LOGGER.info('Соединение с клиентом закрыто!')
        except(ValueError, json.JSONDecodeError) as err:
            SRV_LOGGER.error(f'Получено некорректное сообщение от клиента '
                             f'{client_addr_port}, ошибка: {err}')
            client_sock.close()


if __name__ == '__main__':
    main()
