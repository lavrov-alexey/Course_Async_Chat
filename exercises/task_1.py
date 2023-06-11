""" Задание 1.
Каждое из слов «разработка», «сокет», «декоратор» представить в буквенном
формате и проверить тип и содержание соответствующих переменных.
Затем с помощью онлайн-конвертера преобразовать в набор кодовых точек Unicode
(НО НЕ В БАЙТЫ!!!) и также проверить тип и содержимое переменных.

*Попытайтесь получить кодовые точки без онлайн-конвертера! Без хардкода!

Подсказки:
--- 'разработка' - буквенный формат
--- '\u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\' - набор кодовых точек
--- используйте списки и циклы, не дублируйте функции
"""


def str_to_codepoints(str_text: str, encoding='utf-8'):
    """
    Конвертирует строку текста на входе в строку с кодовыми точками юникод
    заданной кодировки
    :param str_text: Строка с текстом для конвертации
    :param encoding: Кодировка юникод для возврата кодовых точек,
    по умолчанию - utf-8
    :return: Строка с кодовыми точками в заданной кодировке
    """
    return str_text.encode('unicode-escape').decode(encoding=encoding)


if __name__ == '__main__':
    from pprint import pprint

    TEXT_WORDS = ['разработка', 'сокет', 'декоратор']
    words = dict.fromkeys(TEXT_WORDS, '')

    for text_word in words:
        print(f'\nТип: "{type(text_word)}", исходная строка: "{text_word}"')
        codepoint_word = str_to_codepoints(text_word)
        words[text_word] = codepoint_word
        print(f'Тип: "{type(codepoint_word)}", '
              f'строка с кодовыми точками: "{codepoint_word}"')

    # в словаре ключ - строка в тексте, значение - строка в кодовых точках
    pprint(words)
