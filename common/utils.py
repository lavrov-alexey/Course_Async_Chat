""" Общие вспомогательные утилиты для проекта """
import json
import socket
import logging
import common.variables as prj_vars
from common.decorators import logging_deco


@logging_deco
def detect_encode(file_name: str) -> str:
    """
    Возвращает автоматически определенную кодировку переданного на вход файла с
    использованием утилиты chardet. Файл читается построчно до достижения
    уверенности в определении кодировки (для работы с большими файлами).
    :param file_name: имя файла (путь) для определения кодировки
    :return: строка с определенной кодировкой файла
    """
    from chardet.universaldetector import UniversalDetector

    # создаем детектор
    detector = UniversalDetector()

    try:
        # Пробуем открыть файл на чтение в байтах
        with open(file_name, 'rb') as fl:
            '''Для определения кодировки файла будем считывать и скармливать 
            автодетекту файл построчно (на случай, если файл большой). Как 
            только автодетект будет уверен в кодировке - останавливаемся'''
            for line in fl:
                detector.feed(line)
                if detector.done:
                    break
            detector.close()
            return detector.result['encoding']
    except FileNotFoundError as err:
        print(f'Ошибка! Файл "{file_name}" не найден! {err}')
        exit(1)
    except Exception as err:
        print(f'Неожиданная ошибка! Что-то пошло не так! {err}')
        exit(2)


@logging_deco
def get_message(sock: socket) -> dict:
    """
    Принимает через объект сокета байты и декодирует сообщение в словарь,
    если принято что-то другое поднимает ошибку значения (ValueError)
    :param sock: сокет для чтения байт
    :return: словарь с данными
    """

    # читаем из сокета данные (с учетом ограничений настройки проекта)
    encoded_response = sock.recv(prj_vars.MAX_PACKAGE_LENGTH)
    if isinstance(encoded_response, bytes):
        # если это байты - декодируем их в JSON-строку кодировкой проекта
        json_response = encoded_response.decode(prj_vars.ENCODING)
        # из JSON-строки переводим в Python-объекты
        response = json.loads(json_response)
        # если получился словарь - отдаём, если нет - поднимаем ошибку значения
        if isinstance(response, dict):
            return response
    raise ValueError


@logging_deco
def send_message(sock: socket, message: dict) -> None:
    """
    Принимает сообщение (в протоколе JIM), кодирует его и отправляет в сокет
    :param sock: сокет для отправки сообщения
    :param message: сообщение для отправки в виде словаря с самим сообщением
    и доп. параметрами протокола JIM
    :return:
    """

    # переводим сообщение (словарь) в JSON-строку
    json_message = json.dumps(message)
    # кодируем JSON-строку в байты в кодировке проекта
    encoded_message = json_message.encode(prj_vars.ENCODING)
    # отправляем закодированные байты в сокет
    sock.send(encoded_message)
