""" Скрипт запуска серверной и клиентской части асинхронного чата """

from subprocess import Popen, CREATE_NEW_CONSOLE

CLIENTS_CNT = 5
# CMD_EXIT = 'q'
# CMD_RUN_ALL = 's'
# CMD_CLOSE_WINDOWS = 'x'
SERV_CMD_RUN = 'python server.py -p 7777 -a localhost'
CLIENT_CMD_RUN = 'python client.py localhost 7777'

# сюда будем накапливать запускаемые дочерние процессы
process = []
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
            process.append(Popen(SERV_CMD_RUN,
                                 creationflags=CREATE_NEW_CONSOLE))
            for client_idx in range(CLIENTS_CNT):
                process.append(Popen(CLIENT_CMD_RUN,
                                     creationflags=CREATE_NEW_CONSOLE))
        case 'x':
            while process:
                process_to_kill = process.pop()
                process_to_kill.kill()
        case _:  # всё остальное
            print(f'Введена недоступная команда: {user_cmd}')
