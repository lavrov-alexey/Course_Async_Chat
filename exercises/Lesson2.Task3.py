""" Урок 2. Задание 3
Задание на закрепление знаний по модулю yaml. Написать скрипт, автоматизирующий
сохранение данных в файле YAML-формата.
Для этого:
1. Подготовить данные для записи в виде словаря, в котором первому ключу
соответствует список, второму — целое число, третьему — вложенный словарь,
где значение каждого ключа — это целое число с юникод-символом, отсутствующим
в кодировке ASCII (например, €);
2. Реализовать сохранение данных в файл формата YAML — например,
в файл file.yaml. При этом обеспечить стилизацию файла с помощью параметра
default_flow_style, а также установить возможность работы с юникодом:
allow_unicode = True;
3. Реализовать считывание данных из созданного файла и проверить, совпадают
ли они с исходными."""

import json
from pprint import pprint

import yaml

if __name__ == '__main__':

    OUT_FILE = 'out_file.yaml'
    EURO = '\N{euro sign}'  # знак "евро" будем брать по его названию
    DATA_STRUCTURE = {
        'items': ['computer',
                  'printer',
                  'keyboard',
                  'mouse'],
        'items_price': {'computer': f'200{EURO}-1000{EURO}',
                        'printer': f'100{EURO}-300{EURO}',
                        'keyboard': f'5{EURO}-50{EURO}',
                        'mouse': f'4{EURO}-7{EURO}'},
        'items_quantity': 4
    }

    print('Заданная в ТЗ структура данных перед записью в yaml-файл:')
    pprint(DATA_STRUCTURE)

    # записываем структуру в yaml-файл в человекочитаемом стиле
    # (default_flow_style) и с возможностью работы с юникодом
    try:
        with open(OUT_FILE, 'w', encoding='utf-8') as fl:
            yaml.dump(DATA_STRUCTURE, fl, default_flow_style=False,
                      allow_unicode=True)
    except Exception as err:
        print(f'Что-то не то при записи в файл "{OUT_FILE}": {err}')

    # для проверки - считываем данные из файла обратно
    with open(OUT_FILE, 'r', encoding='utf-8') as fl:
        yaml_content = yaml.load(fl, Loader=yaml.FullLoader)

    print('\nCтруктура данных после её считывания из yaml-файл и'
          ' преобразования в Python-объекты:')
    pprint(yaml_content)
    print('\nСТРУКТУРЫ ДО И ПОСЛЕ - ОДИНАКОВЫ ПО ЗНАЧЕНИЮ')
