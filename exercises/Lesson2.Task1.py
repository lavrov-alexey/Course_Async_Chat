""" Урок 2. Задание 1
Закрепление знаний по модулю CSV. Написать скрипт, осуществляющий
выборку определенных данных из файлов info_1.txt, info_2.txt, info_3.txt
и формирующий новый «отчетный» файл в формате CSV.
Для этого:

1. Создать функцию get_data(), в которой в цикле осуществляется перебор файлов
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

2. Создать функцию write_to_csv(), в которую передавать ссылку на CSV-файл.
В этой функции реализовать получение данных через вызов функции get_data(),
а также сохранение подготовленных данных в соответствующий CSV-файл;

3. Проверить работу программы через вызов функции write_to_csv().

P.S. Для удобства работы с данными - использована немного другая структура
хранения, чем в ТЗ.
"""

from pprint import pprint


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


def get_data(in_files: list, parse_fields: list) -> dict:
    """
    Парсит переданный на вход список текстовых файлов для отбора значений
    переданного списка полей
    Парсинг регуляркой по каждому полю: fr'{parse_field}:\s*(.+)'
    :param in_files: список текстовых файлов для парсинга (кодировка опред.
    автоматически)
    :param parse_fields: список полей для парсинга (наименования параметров)
    :return: словарь ключ: имя файла, значение: словарь с искомым параметром
    (ключ) и их значениями в файле
    """
    """стуктура итогового (возвращаемого) результата:
        {
          file_name1: { param1: value1
                        ...
                        paramN: valueN }
          ...
          file_nameM: { param1: value1
                        ...
                        paramN: valueN }
        }"""

    import re

    """создаем список скомпилированных регулярок для всех полей поиска
    для каждого поля будем искать в файле значение на основании регулярки:
    само поле в начале строки, потом двоеточие и пробельные символы,
    потом до конца строки - группа символов до конца строки с искомым
    значением (её и будем сохранять)"""
    parse_regexps = [re.compile(fr'{parse_field}:\s*(.+)')
                     for parse_field in parse_fields]
    # можно глянуть - что получилось в итоге в списке
    # for item in parse_regexps:
    #     print(item, type(item))

    res_data = dict()
    # читаем поочередно каждый из файлов списка целиком, кодировку - определяем
    for in_file in in_files:
        try:
            with open(in_file, 'r', encoding=detect_encode(in_file)) as fn:
                fn_text = fn.read()
        except Exception as err:
            print(f'Что-то пошло не так при открытии файла {in_file}: {err}')
            exit(3)

        # для каждого из полей регуляркой ищем в кажд. файле значение поля
        file_values = dict()
        for parse_regexp, parse_field in zip(parse_regexps, parse_fields):
            parse_value = parse_regexp.findall(fn_text)[0]
            file_values[parse_field] = parse_value

        # сохраняем в итог. словарь - найденное в этом файле и переход к след.
        res_data[in_file] = file_values

    # проверочная распечатка итоговой структуры парсинга всех файлов из списка
    # pprint(res_data)
    return res_data


def write_parsed_data_to_csv(pars_data: dict, csv_file_name='parsed_data.csv',
                             encoding='utf-8') -> None:
    import csv

    FIELD_FILENAME = 'Имя файла'

    # формируем заголовки полей
    headers = [FIELD_FILENAME]
    for params_in_file in pars_data.values():
        headers.extend(params_in_file.keys())
        break

    # формируем итоговый список со списком данных для сохранения
    res_data = [headers]
    for file_name, params_in_file in pars_data.items():
        data_lst = [file_name]
        for param_value in params_in_file.values():
            data_lst.append(param_value)
        res_data.append(data_lst)

    # for line in res_data:  # тестовый вывод итога
    #     print(line)

    # сохраняем итоговый список в файл
    try:
        with open(csv_file_name, 'w', encoding=encoding) as fl:
            fl_writer = csv.writer(fl)
            fl_writer.writerows(res_data)
    except Exception as err:
        print(f'Что-то пошло не так при записи результата в файл: {err}')
        exit(4)


if __name__ == '__main__':

    IN_FILES = ('info_1.txt', 'info_2.txt', 'info_3.txt')
    RES_FILE = 'result_pars.csv'
    FIELDS = [
        'Изготовитель системы',
        'Название ОС',
        'Код продукта',
        'Тип системы'
    ]

    parsed_data = get_data(in_files=IN_FILES, parse_fields=FIELDS)
    write_parsed_data_to_csv(parsed_data)
