""" Скрипт запуска серверной и клиентской части асинхронного чата """

from subprocess import Popen, CREATE_NEW_CONSOLE

CLIENTS_CNT = 5
# CMD_EXIT = 'q'
# CMD_RUN_ALL = 's'
# CMD_CLOSE_WINDOWS = 'x'
SERV_CMD_RUN = 'python server.py -p 7777 -a localhost'
CLIENT_CMD_RUN = 'python client.py localhost 7777'

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
            listen_count = input(f'- введите нужное кол-во клиентов '))
            for client_idx in range(CLIENTS_CNT):
                processes.append(Popen(CLIENT_CMD_RUN,
                                       creationflags=CREATE_NEW_CONSOLE))
        case 'x':
            while processes:
                process_to_kill = processes.pop()
                process_to_kill.kill()
        case _:  # всё остальное
            print(f'Введена недоступная команда: {user_cmd}')
