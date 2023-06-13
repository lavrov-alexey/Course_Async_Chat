""" Задание 3.
Определить, какие из слов «attribute», «класс», «функция», «type» невозможно
записать в байтовом типе с помощью маркировки b'' (без encode decode).
Подсказки:
--- используйте списки и циклы, не дублируйте функции
--- обязательно!!! усложните задачу, "отловив" исключение,
придумайте как это сделать"""

if __name__ == '__main__':
    TEXT_WORDS = ['attribute', 'класс', 'функция', 'type']

    for text_word in TEXT_WORDS:
        try:
            bytes_word = bytes(text_word, encoding='ASCII')
            print(f'Слово "{text_word}" сконвертировалось в байты кодировки '
                  f'ASCII: {bytes_word} (тип: {type(bytes_word)})')
        # кириллица не входит в ASCII-таблицу, поэтому будет ошибка кодирования
        except UnicodeEncodeError:
            print(f'Слово "{text_word}" не может быть сконвертировано в байты '
                  f'кодировки ASCII')
