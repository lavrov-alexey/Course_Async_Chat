""" Задание 4.
Преобразовать слова «разработка», «администрирование», «protocol», «standard» из
строкового представления в байтовое и выполнить обратное преобразование
(используя методы encode и decode).
Подсказки:
--- используйте списки и циклы, не дублируйте функции"""

if __name__ == '__main__':
    WORDS_TEXT_IN = ['разработка', 'администрирование', 'protocol', 'standard']

    for word_text_in in WORDS_TEXT_IN:
        # кодируем строковое представление в байты
        word_bytes = word_text_in.encode(encoding='utf-8')
        # декодируем байты обратно в строковое представление
        word_text_out = word_bytes.decode(encoding='utf-8')
        print(f'Исходный текст: "{word_text_in}"\n'
              f'текст, преобразованный в байты: "{word_bytes}"\n'
              f'текст после декодирования байтов в строку: "{word_text_out}"\n'
              f'сравнение до и после: {word_text_in == word_text_out}\n')
