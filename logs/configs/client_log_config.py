"""
Задание-05

Для проекта «Мессенджер» реализовать логирование с использованием модуля logging

1. В директории проекта создать каталог log, в котором для клиентской
и серверной сторон в отдельных модулях формата client_log_config.py и
server_log_config.py создать логгеры;

2. В каждом модуле выполнить настройку соответствующего логгера по следующему
алгоритму:
- Создание именованного логгера;
- Сообщения лога должны иметь следующий формат:
    "<дата-время> <уровеньважности> <имямодуля> <сообщение>";
- Журналирование должно производиться в лог-файл;
- На стороне сервера необходимо настроить ежедневную ротацию лог-файлов.

3. Реализовать применение созданных логгеров для решения двух задач:
- Журналирование обработки исключений try/except.
    Вместо функции print() использовать журналирование и обеспечить вывод
    служебных сообщений в лог-файл;
- Журналирование функций, исполняемых на серверной и клиентской сторонах при
    работе мессенджера.
"""

import logging.handlers
import os.path
import sys

from common.variables import ENCODING, LOGS_FORMAT, CLIENT_LOG_FILE_NAME, \
    CLIENT_LOGGER, LOG_LVL_BASE, LOG_LVL_FILE, LOG_LVL_CONSOLE

# получаем абсолютный путь до места запуска скрипта
basedir = os.path.abspath(os.getcwd())
# папка с логами на 1 уровень выше
logs_dir = os.path.abspath(os.path.join(basedir, '..'))
# формируем полный абсолютный путь к файлу лога
log_file_name = os.path.join(logs_dir, CLIENT_LOG_FILE_NAME)

# создаем форматтер для вывода сообщений
CLIENT_FORMATTER = logging.Formatter(LOGS_FORMAT)

# создаем обработчики вывода в консоль (ошибки) и в файл (debug инфо)
STREAM_HANDLER = logging.StreamHandler(sys.stderr)
LOG_FILE = logging.handlers.RotatingFileHandler (log_file_name,
                                                 encoding=ENCODING,
                                                 mode='a',
                                                 maxBytes=1048576,
                                                 backupCount=5)

# задаем для обработчиков формат вывода и уровень сообщений для логирования
STREAM_HANDLER.setFormatter(CLIENT_FORMATTER)
STREAM_HANDLER.setLevel(LOG_LVL_CONSOLE)
LOG_FILE.setFormatter(CLIENT_FORMATTER)
LOG_FILE.setLevel(LOG_LVL_FILE)

# создаем логгер и добавляем в него наши обработчики
LOGGER = logging.getLogger(CLIENT_LOGGER)
LOGGER.addHandler(STREAM_HANDLER)
LOGGER.addHandler(LOG_FILE)
LOGGER.setLevel(LOG_LVL_BASE)


if __name__ == '__main__':
    LOGGER.debug('Отладочная информация (клиент)')
    LOGGER.info('Информац. сообщение  (клиент)')
    LOGGER.warning('Предупреждение (клиент)')
    LOGGER.error('Предупреждение (клиент)')
    LOGGER.critical('Критическое сообщение (клиент)')
