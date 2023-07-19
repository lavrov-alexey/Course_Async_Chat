""" Скрипт запуска серверной и клиентской части асинхронного чата """

from sys import stderr
from subprocess import Popen, CREATE_NEW_CONSOLE
from common.variables import DEFAULT_IP_ADDRESS, DEFAULT_PORT, \
    CLIENT_SEND_MODE, CLIENT_LISTEN_MODE

CLIENTS_CNT = 5
# CMD_EXIT = 'q'
# CMD_RUN_ALL = 's'
# CMD_CLOSE_WINDOWS = 'x'
SERV_CMD_RUN = f'python server.py -p {DEFAULT_PORT} -a {DEFAULT_IP_ADDRESS}'
CLIENT_CMD_RUN = f'python client.py -a {DEFAULT_IP_ADDRESS} -p {DEFAULT_PORT}'
CLIENT_SEND_CMD_RUN = f'python client.py -a {DEFAULT_IP_ADDRESS} ' \
                      f'-p {DEFAULT_PORT} -m {CLIENT_SEND_MODE}'
CLIENT_LISTEN_CMD_RUN = f'python client.py -a {DEFAULT_IP_ADDRESS} ' \
                        f'-p {DEFAULT_PORT} -m {CLIENT_LISTEN_MODE}'

# сюда будем накапливать запускаемые дочерние процессы
processes = []
while True:
    user_cmd = input(f'Доступные команды:\n'
                     f'q - выход из скрипта\n'
                     f's - запустить сервер и клиентов\n'
                     f'x - закрыть сервер и клиентов\n'
                     f'Ваша команда: ')
    match user_cmd:
        case 'q':
            break
        case 's':
            # запускаем процесс сервера и в цикле нужное кол-во клиентов
            processes.append(Popen(SERV_CMD_RUN,
                                   creationflags=CREATE_NEW_CONSOLE))

            # получаем кол-во клиентов для отправки сообщений
            try:
                send_count = int(input(f'- введите кол-во клиентов для '
                                       f'отправки сообщений (больше 0): '))
                if send_count < 1:
                    raise ValueError
            except Exception as err:
                stderr(f'Кол-во клиентов должно быть целым числом больше 0!')
                exit(1)

            # получаем кол-во клиентов для приема сообщений
            try:
                listen_count = int(input(f'- введите кол-во клиентов для приема'
                                         f' сообщений (больше 0): '))
                if listen_count < 1:
                    raise ValueError
            except Exception as err:
                stderr(f'Кол-во клиентов должно быть целым числом больше 0!')
                exit(1)

            # создаем нужное кол-во клиентов на отправку и прием сообщений
            for _ in range(send_count):
                processes.append(Popen(CLIENT_SEND_CMD_RUN,
                                       creationflags=CREATE_NEW_CONSOLE))
            for _ in range(listen_count):
                processes.append(Popen(CLIENT_LISTEN_CMD_RUN,
                                       creationflags=CREATE_NEW_CONSOLE))

        case 'x':
            while processes:
                process_to_kill = processes.pop()
                process_to_kill.kill()
        case _:  # всё остальное
            print(f'Введена недоступная команда: {user_cmd}')
