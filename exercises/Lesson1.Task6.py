""" Задание 6.
Создать текстовый файл test_file.txt, заполнить его тремя строками:
«сетевое программирование», «сокет», «декоратор».
Проверить кодировку файла по умолчанию. Принудительно открыть файл в формате
Unicode и вывести его содержимое."""

if __name__ == '__main__':
    import chardet
    from chardet.universaldetector import UniversalDetector

    FILE_NAME = 'test_file.txt'

    # создаем детектор
    detector = UniversalDetector()

    try:
        # Пробуем открыть файл на чтение в байтах
        with open(FILE_NAME, 'rb') as fl:
            '''Для определения кодировки файла будем считывать и скармливать 
            автодетекту файл построчно (на случай, если файл большой). Как 
            только автодетект будет уверен в кодировке - останавливаемся'''
            print(f'\n1. Автоопределение кодировки файла "{FILE_NAME}"')
            for idx, line in enumerate(fl, 1):
                detector.feed(line)
                # можно посмотреть сколько строк понадобилось для определения
                print(f'Строка №{idx} (вывод в байтах): {line}')
                if detector.done:
                    break
            detector.close()
            print(f'Результат автодетекта кодировки: {detector.result}')
            detected_enc = detector.result['encoding']
    except FileNotFoundError:
        print(f'Ошибка! Файл "{FILE_NAME}" не найден!', end='')
        exit(1)
    except:
        print('Неожиданная ошибка! Что-то пошло не так при открытии файла!',
              end='')
        exit(2)

    # знаем, что файл существует и его кодировку - спокойно можем читать
    print(f'\n2. Файл "{FILE_NAME}" в определенной кодировке "{detected_enc}":')
    with open(FILE_NAME, 'r', encoding=detected_enc) as fl:
        for idx, line in enumerate(fl, 1):
            print(f'Строка №{idx}: {line}', end='')

    print(f'\n\n3. Файл "{FILE_NAME}" принудительно в кодировке "UTF-8":')
    try:
        with open(FILE_NAME, 'r', encoding='utf-8') as fl:
            for idx, line in enumerate(fl, 1):
                print(f'Строка №{idx}: {line}', end='')
    except UnicodeDecodeError as err:
        print(f'Поймали ошибку декодирования файла: {err}', end='')
        exit(3)
    except:
        print('Неожиданная ошибка! Что-то пошло не так!', end='')
        exit(4)
