# Модуль работы с полем игры
# Copyright by Gennadiy S. aka GennDALF

from players import PLAYER, SAVES
from help import MESSAGES, ANSWERS

FIELD = [['']*3 for _ in range(3)]

def field():
    global FIELD
    pass

# проверка наличия сохранённой партии
def check_saves(*, single=True):
    global FIELD
    # для парной игры
    s = set(PLAYER)
    # для одиночной игры
    if single:
        s |= {'ai1', 'ai2'}
    for save in SAVES:
        if set(save).issubset(s):
            # хочет ли игрок загрузить найденную партию
            load = input(MESSAGES[6]).lower()
            if load in ANSWERS[6]:
                FIELD = SAVES[save]
                return save
    return False

