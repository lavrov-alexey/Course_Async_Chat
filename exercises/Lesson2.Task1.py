""" Задание 2
1. Задание на закрепление знаний по модулю CSV. Написать скрипт, осуществляющий
выборку определенных данных из файлов info_1.txt, info_2.txt, info_3.txt
и формирующий новый «отчетный» файл в формате CSV.
Для этого:
Создать функцию get_data(), в которой в цикле осуществляется перебор файлов
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
Создать функцию write_to_csv(), в которую передавать ссылку на CSV-файл. В этой
функции реализовать получение данных через вызов функции get_data(), а также
сохранение подготовленных данных в соответствующий CSV-файл;
Проверить работу программы через вызов функции write_to_csv().

### 2. Задание на закрепление знаний по модулю json. Есть файл orders в формате
JSON с информацией о заказах. Написать скрипт, автоматизирующий его заполнение
данными. Для этого:
Создать функцию write_order_to_json(), в которую передается 5 параметров —
товар (item), количество (quantity), цена (price), покупатель (buyer),
дата (date). Функция должна предусматривать запись данных в виде словаря в файл
orders.json. При записи данных указать величину отступа в 4 пробельных символа;
Проверить работу программы через вызов функции write_order_to_json() с передачей
в нее значений каждого параметра.

### 3. Задание на закрепление знаний по модулю yaml. Написать скрипт,
автоматизирующий сохранение данных в файле YAML-формата. Для этого:
Подготовить данные для записи в виде словаря, в котором первому ключу
соответствует список, второму — целое число, третьему — вложенный словарь, где
значение каждого ключа — это целое число с юникод-символом, отсутствующим в
кодировке ASCII (например, €);
Реализовать сохранение данных в файл формата YAML — например, в файл file.yaml.
При этом обеспечить стилизацию файла с помощью параметра default_flow_style, а
также установить возможность работы с юникодом: allow_unicode = True;
Реализовать считывание данных из созданного файла и проверить, совпадают ли они
с исходными."""


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


if __name__ == '__main__':

    IN_FILES = ('info_1.txt', 'info_2.txt', 'info_3.txt')
    RES_FILE = 'result_pars.csv'

    for fl in IN_FILES:
        fl_enc = detect_encode(fl)
        
