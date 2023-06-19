""" Константы для работы проекта """

# Порт по умолчанию для сетевого взаимодействия
DEFAULT_PORT = 7777
# IP-адрес по умолчанию для подключения клиента
DEFAULT_IP_ADDRESS = '127.0.0.1'  # он же 'localhost'
# Максимальная очередь подключений
MAX_CONNECTIONS = 5
# Максимальная длинна сообщения в байтах
MAX_PACKAGE_LENGTH = 1024
# Используемая в проекте кодировка текста
ENCODING = 'utf-8'

# Взаимодействие по протоколу JIM (передача JSON-объектов через TCP-сокеты).
# JIM. Основные ключи:
ACTION = 'action'
TIME = 'time'
USER = 'user'
ACCOUNT_NAME = 'account_name'

# JIM. Прочие ключи:
PRESENCE = 'presence'
RESPONSE = 'response'
ERROR = 'error'
