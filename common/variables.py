""" Константы для работы проекта """
import logging

# Порт по умолчанию для сетевого взаимодействия
DEFAULT_PORT = 7777
# IP-адрес по умолчанию для подключения клиента
DEFAULT_IP_ADDRESS = '127.0.0.1'  # он же 'localhost'
# Максимальная очередь подключений
MAX_CONNECTIONS = 5
# Максимальная длинна сообщения в байтах
MAX_PACKAGE_LENGTH = 1024
# Используемая в проекте кодировка текста
ENCODING = 'UTF-8'
LOW_PORT_RANGE = 1024  # меньше - служебные порты
HIGH_PORT_RANGE = 65535  # больше не может быть по определению

# Взаимодействие по протоколу JIM (передача JSON-объектов через TCP-сокеты).
# JIM. Основные ключи:
ACTION = 'ACTION'
TIME = 'TIME'
USER = 'USER'
ACCOUNT_NAME = 'ACCOUNT_NAME'

# JIM. Прочие ключи:
PRESENCE = 'PRESENCE'
RESPONSE = 'RESPONSE'
ERROR = 'ERROR'
BAD_REQUEST = 'BAD REQUEST'
GUEST = 'GUEST'

# Logging config params
SRV_LOG_FILE_NAME = 'async_chat_srv.log'
SRV_LOGGER = 'async_chat_log.serv'

CLIENT_LOG_FILE_NAME = 'async_chat_client.log'
CLIENT_LOGGER = 'async_chat_log.client'

LOGS_FORMAT = '%(asctime)-30s %(levelname)-10s %(module)-20s %(message)s'
LOG_LVL_CONSOLE = logging.ERROR
LOG_LVL_FILE = logging.DEBUG
LOG_LVL_BASE = logging.ERROR
