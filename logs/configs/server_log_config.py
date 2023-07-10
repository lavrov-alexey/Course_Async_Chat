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

# import logging
import logging.handlers
import os.path
import sys

from common.variables import ENCODING, LOGS_FORMAT, SRV_LOG_FILE_NAME, \
    SRV_LOGGER, LOG_LVL_FILE, LOG_LVL_CONSOLE, LOG_LVL_BASE

# получаем абсолютный путь до места запуска скрипта
basedir = os.path.abspath(os.getcwd())
# папка с логами на 1 уровень выше
logs_dir = os.path.abspath(os.path.join(basedir, '..'))
# формируем полный абсолютный путь к файлу лога
log_file_name = os.path.join(logs_dir, SRV_LOG_FILE_NAME)

# создаем форматтер и задаем для него формат сообщений
SRV_FORMATTER = logging.Formatter(LOGS_FORMAT)

# создаем обработчики для вывода в консоль и файл и задаем уровни логирования
STREAM_HANDLER = logging.StreamHandler(sys.stderr)
STREAM_HANDLER.setLevel(LOG_LVL_CONSOLE)
# LOG_FILE = logging.FileHandler(log_file_name, encoding=ENCODING)
LOG_FILE = logging.handlers.TimedRotatingFileHandler(log_file_name,
                                                     encoding=ENCODING,
                                                     interval=10,
                                                     when='m',
                                                     utc=366)
LOG_FILE.setLevel(LOG_LVL_FILE)

# связываем обработчики с форматтером (будет одинаковый)
STREAM_HANDLER.setFormatter(SRV_FORMATTER)
LOG_FILE.setFormatter(SRV_FORMATTER)

# создаем сам логгер, который будет писать и добавляем в него обработчики
SRV_LOGGER = logging.getLogger(SRV_LOGGER)
SRV_LOGGER.addHandler(STREAM_HANDLER)
SRV_LOGGER.addHandler(LOG_FILE)
# выставляем требуемый уровень сообщений в целом логгеру
SRV_LOGGER.setLevel(LOG_LVL_BASE)


if __name__ == '__main__':
    SRV_LOGGER.debug('Отладочная информация (сервер)')
    SRV_LOGGER.info('Информац. сообщение (сервер)')
    SRV_LOGGER.warning('Предупреждение (сервер)')
    SRV_LOGGER.error('Предупреждение (сервер)')
    SRV_LOGGER.critical('Критическое сообщение (сервер)')
