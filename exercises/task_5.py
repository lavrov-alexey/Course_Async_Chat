""" Задание 5.
Выполнить пинг веб-ресурсов yandex.ru, youtube.com и
преобразовать результаты из байтовового в строковый тип на кириллице.
Подсказки:
--- используйте модуль chardet, иначе задание не засчитается!!!"""

if __name__ == '__main__':
    import subprocess
    import chardet

    # кортеж с именем запускаемой утилиты и параметрами к ней
    ARGS = ('ping', 'gb.ru', '-n', '6')
    # создаем подпроцесс запуска команды пинг, результат вывода перехватываем
    gb_ping = subprocess.Popen(ARGS, stdout=subprocess.PIPE)
    # выводим результат работы подпроцесса
    for line in gb_ping.stdout:
        # вариант явного указания кодовой страницы (хардкод, что нехорошо)
        # print(line.decode(encoding='cp866'), end='')
        # определяем код. страницу для каждой байтовой строки вывода скрипта
        detect_res = chardet.detect(line)
        # получаем словарь с кодировкой, языком и точностью определения
        # print(detect_res)
        detect_enc = detect_res['encoding']
        # выводим строки с определенной утилитой кодировкой
        print(line.decode(detect_enc), end='')
