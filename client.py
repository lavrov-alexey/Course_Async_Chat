""" Скрипт клиентской программы асинхронного чата """
import argparse
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
    ACCOUNT_NAME, CLIENT_LOGGER, CLIENT_SEND_MODE, CLIENT_LISTEN_MODE
# подтягиваем готовый конфиг логгера
import logs.configs.client_log_config
# подтягиваем декоратор для логирования работы функций
from common.decorators import logging_deco, LogForFunc
# запуск логирования клиента (получаем клиент. логгер из файла конфига)
LOGGER = logging.getLogger(CLIENT_LOGGER)


# @logging_deco
@LogForFunc()
def run_args_parser():
    """
    Разбирает параметры, переданные при запуске скрипта, например:
    client.py -a 192.168.38.62 -p 4567 - m send
    :return: кортеж (адрес_сервера, порт_сервера, режим_работы_клиента)
    """

    LOGGER.debug(f'Параметры вызова: {argv[1:]=}')

    # создаём экземпляр парсера и добавляем параметры
    parser = argparse.ArgumentParser(description='Парсер параметров запуска '
                                                 'скрипта клиента')
    parser.add_argument('-a', '--addr', default=DEFAULT_IP_ADDRESS, type=str,
                        help=f'IP-адрес сервера, по умолчанию '
                             f'{DEFAULT_IP_ADDRESS}', nargs='?')
    parser.add_argument('-p', '--port', default=DEFAULT_PORT, type=int,
                        help=f'Порт сервера, по умолчанию {DEFAULT_PORT}',
                        nargs='?')
    parser.add_argument('-m', '--mode', choices=[CLIENT_SEND_MODE,
                                                 CLIENT_LISTEN_MODE],
                        help=f'Режим работы клиента: {CLIENT_SEND_MODE} / '
                             f'{CLIENT_LISTEN_MODE}',
                        nargs='?')

    # разбираем параметры, переданные при запуске скрипта (без имени скрипта)
    run_args = parser.parse_args(sys.argv[1:])
    serv_addr = run_args.addr
    client_mode = run_args.mode

    try:
        serv_port = int(run_args.port)
        LOGGER.debug(f'Cервер - адрес: {serv_addr}, порт: {serv_port}')

        # валидируем полученный порт сервера
        if serv_port < LOW_PORT_RANGE or serv_port > HIGH_PORT_RANGE:
            raise ValueError
    except ValueError as err:
        LOGGER.critical(f'Порт сервера должен быть числом в диапазоне '
                        f'{LOW_PORT_RANGE}-{HIGH_PORT_RANGE}. '
                        f'Получено: "{serv_port}". Ошибка: {err}')
        exit(1)

    return serv_addr, serv_port, client_mode


# @logging_deco
@LogForFunc()
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


# @logging_deco
@LogForFunc()
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
    # получаем параметры запуска скрипта
    serv_addr, serv_port, client_mode = run_args_parser()
    LOGGER.info(f'Запущен клиент, сервер: {serv_addr}:{serv_port}, '
                f'режим: {client_mode}')


    # ПРОДОЛЖАЕМ ЗДЕСЬ!



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
