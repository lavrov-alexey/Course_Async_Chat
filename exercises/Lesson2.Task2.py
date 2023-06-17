""" Урок 2. Задание 2
Задание на закрепление знаний по модулю json. Есть файл orders в формате JSON
с информацией о заказах.
Написать скрипт, автоматизирующий его заполнение данными.
Для этого:
1. Создать функцию write_order_to_json(), в которую передается 5 параметров —
товар (item), количество (quantity), цена (price), покупатель (buyer),
дата (date).
Функция должна предусматривать запись данных в виде словаря в файл orders.json.
При записи данных указать величину отступа в 4 пробельных символа;
2. Проверить работу программы через вызов функции write_order_to_json()
с передачей в нее значений каждого параметра."""

import json

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


def write_order_to_json(order: dict, file_name_json='orders.json',
                        indent_json=4) -> None:
    """
    Дописывает в конец указанного файла с заказами переданный заказ
    :param order: словарь с заказом (параметрами заказа)
    :param file_name_json: путь к файлу с заказами для дополнения
    :param indent_json: отступ для формирования читаемого json-формата
    :return: None
    """

    # считываем что уже есть в файле
    try:
        with open(file_name_json, 'r',
                  encoding=detect_encode(file_name_json)) as fl:
            json_content = json.load(fl)
    except Exception as err:
        print(f'Что-то пошло не так при открытии файла {file_name_json}: {err}')
        exit(3)

    # дописываем новый товар в конец
    try:
        json_content['orders'].append(order)
    except Exception as err:
        print(f'Проблема при попытке добавить заказ в массив заказов: {err}')
        exit(5)

    # записываем обновленный список
    try:
        with open(file_name_json, 'w', encoding='utf-8') as fl:
            json.dump(json_content, fl, indent=indent_json, ensure_ascii=False)
    except Exception as err:
        print(f'Что-то пошло не так при записи файла {file_name_json}: {err}')
        exit(4)


if __name__ == '__main__':

    ORDERS_FILE = 'orders.json'
    TEST_ORDERS = [
        {'item': 'Товар-1',
         'quantity': 11,
         'price': 100,
         'buyer': 'Покупатель-1',
         'date': '11-11-2022'},
        {'item': 'Товар-2',
         'quantity': 22,
         'price': 200,
         'buyer': 'Покупатель-2',
         'date': '22-12-2022'},
        {'item': 'Товар-666',
         'quantity': 666,
         'price': 666,
         'buyer': 'Покупатель-666',
         'date': '01-01-0000'}
    ]

    # смотрим что есть в файле до добавления
    try:
        with open(ORDERS_FILE, 'r',
                  encoding=detect_encode(ORDERS_FILE)) as fl:
            print(f'Файл "{ORDERS_FILE}" ДО добавления заказов:')
            print(json.load(fl))
    except Exception as err:
        print(f'Что-то пошло не так при открытии файла {ORDERS_FILE}: {err}')
        exit(3)

    # добавляем заказы
    for order in TEST_ORDERS:
        write_order_to_json(order, file_name_json=ORDERS_FILE, indent_json=4)

    # смотрим что стало в файле после записи
    try:
        with open(ORDERS_FILE, 'r',
                  encoding=detect_encode(ORDERS_FILE)) as fl:
            print(f'Файл "{ORDERS_FILE}" ПОСЛЕ добавления заказов:')
            print(json.load(fl))
    except Exception as err:
        print(f'Что-то пошло не так при открытии файла {ORDERS_FILE}: {err}')
        exit(3)
