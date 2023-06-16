""" Задание 2
1. Задание на закрепление знаний по модулю CSV. Написать скрипт, осуществляющий
выборку определенных данных из файлов info_1.txt, info_2.txt, info_3.txt
и формирующий новый «отчетный» файл в формате CSV.
Для этого:
1.1. Создать функцию get_data(), в которой в цикле осуществляется перебор файлов
с данными, их открытие и считывание данных. В этой функции из считанных данных
необходимо с помощью регулярных выражений извлечь значения параметров
«Изготовитель системы», «Название ОС», «Код продукта», «Тип системы».
Значения каждого параметра поместить в соответствующий список. Должно получиться
четыре списка — например, os_prod_list, os_name_list, os_code_list,
os_type_list. В этой же функции создать главный список для хранения данных
отчета — например, main_data — и поместить в него названия столбцов отчета в
виде списка: «Изготовитель системы», «Название ОС», «Код продукта»,
«Тип системы». Значения для этих столбцов также оформить в виде списка и
поместить в файл main_data (также для каждого файла);
1.2. Создать функцию write_to_csv(), в которую передавать ссылку на CSV-файл.
В этой функции реализовать получение данных через вызов функции get_data(),
а также сохранение подготовленных данных в соответствующий CSV-файл;
1.3. Проверить работу программы через вызов функции write_to_csv().

### 2. Задание на закрепление знаний по модулю json. Есть файл orders в формате
JSON с информацией о заказах. Написать скрипт, автоматизирующий его заполнение
данными. Для этого:
2.1. Создать функцию write_order_to_json(), в которую передается 5 параметров —
товар (item), количество (quantity), цена (price), покупатель (buyer),
дата (date). Функция должна предусматривать запись данных в виде словаря в файл
orders.json. При записи данных указать величину отступа в 4 пробельных символа;
2.2. Проверить работу программы через вызов функции write_order_to_json()
с передачей в нее значений каждого параметра.

### 3. Задание на закрепление знаний по модулю yaml. Написать скрипт,
автоматизирующий сохранение данных в файле YAML-формата. Для этого:
3.1. Подготовить данные для записи в виде словаря, в котором первому ключу
соответствует список, второму — целое число, третьему — вложенный словарь, где
значение каждого ключа — это целое число с юникод-символом, отсутствующим в
кодировке ASCII (например, €);
3.2. Реализовать сохранение данных в файл формата YAML — например,
в файл file.yaml.
При этом обеспечить стилизацию файла с помощью параметра default_flow_style, а
также установить возможность работы с юникодом: allow_unicode = True;
3.3. Реализовать считывание данных из созданного файла и проверить, совпадают
ли они с исходными."""


def detect_encode(file_name: str):
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
    except FileNotFoundError:
        print(f'Ошибка! Файл "{file_name}" не найден!', end='')
        exit(1)
    except:
        print('Неожиданная ошибка! Что-то пошло не так!', end='')
        exit(2)


def parse_data(in_files: list, parse_fields: dict):
    import re

    result = dict()

    # перебираем все файлы из списка
    for in_file in in_files:
        # читаем содержимое файла
        try:
            with open(in_file, 'r', encoding=detect_encode(in_file)) as fn:
                # читаем каждый из файлов целиком, кодировку - определяем сами
                fn_text = fn.read()
        except Exception as err:
            print(f'Что-то пошло не так при открытии файла {in_file}: {err}')
            exit(2)



def get_data(in_files: list, parse_fields: list):

    import re

    # os_prod_list, os_name_list, os_code_list, os_type_list = [], [], [], []
    # main_data = [list(parse_fields.values())]
    # print(f'{main_data=}, {type(main_data)=}')
    # try:
    #     reg_os_prod = re.compile(fr'{parse_fields["os_prod"]}:\s*(.+)')
    #     reg_os_name = re.compile(fr'{parse_fields["os_name"]}:\s*(.+)')
    #     reg_os_code = re.compile(fr'{parse_fields["os_code"]}:\s*(.+)')
    #     reg_os_type = re.compile(fr'{parse_fields["os_type"]}:\s*(.+)')
    # except Exception as err:
    #     print(f'Что-то пошло не так при создании reg_exp: {err}')
    #     exit(1)
    #
    # for in_file in in_files:
    #     try:
    #         with open(in_file, 'r', encoding=detect_encode(in_file)) as fn:
    #             # читаем каждый из файлов целиком, кодировку - определяем сами
    #             fn_text = fn.read()
    #     except Exception as err:
    #         print(f'Что-то пошло не так при открытии файла {in_file}: {err}')
    #         exit(2)
    #
    #     os_prod_list.append(reg_os_prod.findall(fn_text)[0])
    #     os_name_list.append(reg_os_name.findall(fn_text)[0])
    #     os_code_list.append(reg_os_code.findall(fn_text)[0])
    #     os_type_list.append(reg_os_type.findall(fn_text)[0])
    #
    # print(f'{os_prod_list=}\n{os_name_list=}\n{os_code_list=}\n{os_type_list=}')

    for in_file in in_files:

        with open(in_file, 'r', encoding=detect_encode(in_file)) as fn:
            # читаем каждый из файлов целиком, кодировку - определяем сами
            fn_text = fn.read()

        for parse_field in parse_fields:
            # для каждого поля ищем в файле значение на основании регулярки
            # само поле в начале строки, потом двоеточие и пробельные символы,
            # потом до конца строки - группа символов до конца строки с искомым
            # значением (её и сохраняем)
            reg_exp = re.compile(fr'{field_pattern}:\s*(.+)')
            res_values.append(reg_exp.findall(fn_text)[0])

        # добавляем в итоговый список - список найденных в файле значений
        # и переходим к анализу следующего файла из списка
        result.append(res_values)

    # проверочная распечатка списка списков (заговков и найденных значений
    # в каждом из файлов списка)
    for _ in result:
        print(_)

    return res_values


if __name__ == '__main__':

    IN_FILES = ('info_1.txt', 'info_2.txt', 'info_3.txt')
    RES_FILE = 'result_pars.csv'
    FIELDS = [
        'Изготовитель системы',
        'Название ОС',
        'Код продукта',
        'Тип системы'
    ]
    # FIELDS = {
    #     'os_prod': 'Изготовитель системы',
    #     'os_name': 'Название ОС',
    #     'os_code': 'Код продукта',
    #     'os_type': 'Тип системы'
    # }

    res_values = get_data(in_files=IN_FILES, parse_fields=FIELDS)
