import json
from pprint import pprint
from socket import socket, AF_INET, SOCK_STREAM
from sys import argv
from common.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, GUEST,\
    DEFAULT_PORT, MAX_CONNECTIONS, RESPONSE, ERROR, BAD_REQUEST, \
    LOW_PORT_RANGE, HIGH_PORT_RANGE
from common.utils import get_message, send_message


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
    # если не все ладно - отдаем ошибку о несоотв. формате
    return {
        RESPONSE: 400,
        ERROR: BAD_REQUEST
    }


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

    # устанавливаем порт для прослушивания (по умолчанию или заданны)
    try:
        params = argv[1:]  # имя самого скрипта откидываем - только пар-ры
        if PORT in params:
            # сам номер порта - следующее значение после параметра '-p'
            port_num_str = params[params.index(PORT) + 1]
            listen_port = int(port_num_str)
        else:
            listen_port = DEFAULT_PORT

        # проверяем, чтобы номер порта был релевантным
        if listen_port < LOW_PORT_RANGE or listen_port > HIGH_PORT_RANGE:
            raise ValueError
    except IndexError as err:
        print(f'После параметра "{PORT}" нужно указать номер порта: {err}')
    except ValueError as err:
        print(f'Номер порта может быть только числом в диапазоне '
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
        print(f'После параметра "{ADDR}" нужно указать IP-адрес для '
              f'прослушивания сервером: {err}')
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
        print(f'\nУстановлено соединение с клиентом, адрес: {client_addr=}, '
              f'порт: {client_port=}')

        try:
            message_from_client = get_message(client_sock)
            # полученные из сокета байты - возвращаются в виде словаря
            print('Полученное сообщение от клиента:')
            pprint(message_from_client)
            # разбираем полученный словарь на служ. инфо JIM и само сообщение
            response = process_client_message(message_from_client)
            send_message(client_sock, response)
            print('Клиенту отправлен ответ:')
            pprint(response)
            client_sock.close()  # после отправки ответа - закрываем кл. сокет
            print('Соединение с клиентом закрыто!\n')
        except(ValueError, json.JSONDecodeError) as err:
            print(f'Получено некорректное сообщение от клиента '
                  f'{client_addr_port}, ошибка: {err}')
            client_sock.close()


if __name__ == '__main__':
    main()
