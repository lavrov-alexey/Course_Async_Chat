""" Скрипт клиентской программы асинхронного чата """
import sys
from pprint import pprint
from sys import argv
import json
from socket import socket, AF_INET, SOCK_STREAM
import time
import logging

from common.utils import get_message, send_message
from common.variables import RESPONSE, ERROR, LOW_PORT_RANGE, HIGH_PORT_RANGE, \
    DEFAULT_PORT, DEFAULT_IP_ADDRESS, GUEST, ACTION, PRESENCE, TIME, USER, \
    ACCOUNT_NAME, CLIENT_LOGGER
# подтягиваем готовый конфиг логгера
import logs.configs.client_log_config
# подтягиваем декоратор для логирования работы функций
from common.decorators import logging_deco
# запуск логирования клиента (получаем клиент. логгер из файла конфига)
LOGGER = logging.getLogger(CLIENT_LOGGER)


@logging_deco
def create_presense(account_name=GUEST) -> dict:
    """
    Формирует словарь-сообщение присутствия в формате протокола JIM
    :param account_name: задаёт имя пользователя
    :return: словарь-сообщение присутствия для сервера в формате протокола JIM
    """
    presence_msg = {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name
        }
    }
    return presence_msg


@logging_deco
def process_answ(message: dict) -> str:
    """
    Разбирает ответное сообщение сервера по протоколу JIM
    :param message:  Словарь с параметрами и текстом сообщения от сервера
    :return: Строка с кодом ответа и его текстом
    """
    # проверяем - есть ли в сообщении есть ключ ответа
    if RESPONSE in message:
        # и если ответ 200 - всё хорошо
        if message[RESPONSE] == 200:
            response = '200: OK'
            LOGGER.debug(f'Ответ сервера успешный: {response}')
            return response
        # если ответ не 200 - ругаемся
        response = f'400: {message[ERROR]}'
        LOGGER.warning(f'Ответ сервера с ошибкой: {response}')
        return response
    # а если ключа "ответ" нет в сообщении - ошибка протокола JIM
    LOGGER.critical(f'В ответе сервера нет ключа "response"!')
    raise ValueError


def main() -> None:
    """
    Загрузка параметров командной строки клиента (нужно передать адрес и порт
    сервера), например:
    # client.py 192.168.38.62 4567
    # server.py -p 4567 -a 192.168.38.62
    :return:
    """

    LOGGER.debug(f'Параметры вызова: {argv[1:]=}')
    try:
        # в 1-м параметре запуска клиентского скрипта ждём адрес, 2й - порт
        serv_addr = argv[1]
        serv_port = int(argv[2])
        LOGGER.debug(f'Cервер - адрес: {serv_addr}, порт: {serv_port}')

        # валидируем полученный порт сервера
        if serv_port < LOW_PORT_RANGE or serv_port > HIGH_PORT_RANGE:
            raise ValueError
    except IndexError as err:
        serv_addr = DEFAULT_IP_ADDRESS
        serv_port = DEFAULT_PORT
        LOGGER.debug(f'Используются значения адреса и порта сервера '
                     f'по умолчанию: {DEFAULT_IP_ADDRESS}:{DEFAULT_PORT}')
    except ValueError as err:
        LOGGER.critical(f'Порт сервера должен быть числом в диапазоне '
                        f'{LOW_PORT_RANGE}-{HIGH_PORT_RANGE}. '
                        f'Получено: "{serv_port}". Ошибка: {err}')
        exit(1)

    # создаем объект клиент. сокета (сетевой, потоковый), подключаемся к серверу
    JIM_socket = socket(AF_INET, SOCK_STREAM)
    JIM_socket.connect((serv_addr, serv_port))
    # после установления связи с сервером (рукопожатия / accept от сервера)
    # формируем и отправляем на сервер сообщение о присутствии в формате JIM
    message_to_serv = create_presense()
    send_message(JIM_socket, message_to_serv)
    LOGGER.debug(f'На сервер адрес: {serv_addr}, порт: {serv_port} '
                 f'направлено сообщение: {message_to_serv}')
    try:
        # получаем ответ от сервера и парсим его
        answer = process_answ(get_message(JIM_socket))
        LOGGER.info(f'От сервера получен ответ: {answer}')
    except (ValueError, json.JSONDecodeError) as err:
        LOGGER.error(f'Не удалось декодировать сообщение от сервера: {err}')
        pass
    input('Нажмите Enter для завершения...')


if __name__ == '__main__':
    main()
