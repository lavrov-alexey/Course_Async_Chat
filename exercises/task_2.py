""" Задание 2.
Каждое из слов «class», «function», «method» записать в байтовом формате без
преобразования в последовательность кодов не используя!!! методы encode и
decode) и определить тип, содержимое и длину соответствующих переменных.
Подсказки:
--- b'class' - используйте маркировку b''
--- используйте списки и циклы, не дублируйте функции"""

if __name__ == '__main__':
    TEXT_WORDS = ('class', 'function', 'method')

    for text_word in TEXT_WORDS:
        bytes_word = bytes(text_word, encoding='ASCII')
        print(f'{text_word} ({type(text_word)}) => '
              f'{bytes_word} ({type(bytes_word)})')
