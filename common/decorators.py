"""
Модуль декораторов для проекта Async "Chat"
"""

import sys
import logging
import traceback
import inspect
from functools import wraps

from common.variables import CLIENT_LOGGER, SRV_LOGGER
import logs.configs.server_log_config
import logs.configs.client_log_config

# # Получаем логгер сервера или клиента по имени скрипта на входе.
# try:
#     # если в имени скрипта есть 'client' - берем клиентский конфиг логов
#     script_name = sys.argv[0]
#     if script_name.find('client') != -1:
#         LOGGER = logging.getLogger(CLIENT_LOGGER)
#     # если в имени скрипта есть 'server' - берем клиентский конфиг логов
#     elif script_name.find('server') != -1:
#         LOGGER = logging.getLogger(SRV_LOGGER)
#     else:
#         raise ValueError
# except ValueError as err:
#     print(f'Попытка залогировать работу неизвестного скрипта {script_name}: '
#           f'{err}')
#     exit(1)


def logging_deco(logger):
    def wrap(func_for_logging):
        """
        Функция-декоратор для логирования функций (параметры, результаты),
        """
        @wraps(func_for_logging)
        def deco(*args, **kwargs):
            """
            Функция-обёртка для логирования пар-ров и рез-та декорируемой функции
            """

            logger.debug(f'\nВызов функции: {func_for_logging.__name__} '
                         f'с параметрами: {args}, {kwargs}\n'
                         f'из модуля: {func_for_logging.__module__}, '
                         # оба варианта получения имени функции, из которой был
                         # вызов логируемой функции - работают
                         # f'функции: {traceback.format_stack()[0].split()[-1]}')
                         f'функции: {inspect.stack()[1][3]}')

            res = func_for_logging(*args, **kwargs)
            logger.debug(f'Результат работы функции: {res}')
            return res
        return deco
    return wrap
