import sys
import common.variables as prj_vars


def main() -> None:
    """
    Загрузка параметров командной строки, если параметры не переданы - задаются
    значения по умолчанию
    Пример запуска скрипта с заданием порта и адреса:
    server.py -p 1234 -a 192.168.99.99
    :return: None
    """

    PORT = '-p'  # ключ для передачи номера порта
    ADDR = '-a'  # ключ для передачи адреса для прослушивания
    LOW_PORT_RANGE = 1024  # меньше - служебные порты
    HIGH_PORT_RANGE = 65535  # больше не может быть по определению

    # устанавливаем порт для прослушивания (по умолчанию или заданны)
    try:
        params = sys.argv[1:]  # имя самого скрипта откидываем - только пар-ры
        if PORT in params:
            # сам номер порта - следующее значение после параметра '-p'
            port_num_str = params[params.index(PORT) + 1]
            listen_port = int(port_num_str)
        else:
            listen_port = prj_vars.DEFAULT_PORT

        # проверяем, чтобы номер порта был релевантным
        if listen_port < LOW_PORT_RANGE or listen_port > HIGH_PORT_RANGE:
            raise ValueError
    except IndexError as err:
        print(f'После параметра "{PORT}" нужно указать номер порта: {err}')
    except ValueError as err:
        print(f'Номер порта может быть только числом в диапазоне '
              f'от {LOW_PORT_RANGE} до {HIGH_PORT_RANGE}. '
              f'Получено: "{port_num_str}".\nОшибка: {err}')
        exit(1)

    # устанавливаем адрес для прослушивания
    try:
        if ADDR in params:
            # сам номер порта - след. значение после параметра '-a'
            listen_addr = params[params.index(ADDR) + 1]
        else:
            listen_addr = ''

    except IndexError as err:
        print(f'После параметра "{ADDR}" нужно указать IP-адрес для '
              f'прослушивания: {err}')



if __name__ == '__main__':
    main()
