import common.variables as prj_vars

def process_ans(message: dict) -> str:
    """
    Разбирает ответное сообщение сервера по протоколу JIM
    :param message:  Словарь с параметрами и текстом сообщения от сервера
    :return: Строка с кодом ответа и его текстом
    """

    # проверяем - есть ли в сообщении есть ключ ответа
    if prj_vars.RESPONSE in message:
        # и если ответ 200 - всё хорошо
        if message[prj_vars.RESPONSE] == 200:
            return '200: ОК'
        # если ответ не 200 - ругаемся
        return f'400: {message[prj_vars.ERROR]}'
    # а если ключа "ответ" нет в сообщении - ошибка протокола JIM
    raise ValueError
