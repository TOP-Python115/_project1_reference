# Модуль искусственного интеллекта игры
# Copyright by Gennadiy S. aka GennDALF

from random import randrange
from itertools import chain

import field


# для низкого уровня сложности
def random_turn():
    while True:
        y, x = randrange(field.DIM), randrange(field.DIM)
        if not field.FIELD[y][x]:
            break
    return y, x

# поиск самой длинной последовательности (ряд, столбец, диагональ),
#   заполненной только одним символом
def preferred_seq(symbol):
    def preferred_row(collection):
        rows = []
        for i in range(len(collection)):
            if symbol in collection[i]:
                if len(set([el for el in collection[i] if el])) == 1:
                    rows += [(collection[i].count(symbol), i)]
        try:
            return sorted(rows, reverse=True)[0]
        except IndexError:
            return -1, -1
    FIELD_T = [[field.FIELD[j][i] for j in range(field.DIM)] for i in range(field.DIM)]
    DIAGONALS = [[field.FIELD[i][i] for i in range(field.DIM)],
                 [field.FIELD[i][field.DIM-i-1] for i in range(field.DIM)]]
    seqs = []
    for key, matrix in {'r': field.FIELD, 'c': FIELD_T, 'd': DIAGONALS}.items():
        seqs += [(*preferred_row(matrix), key)]
    index, sequence = sorted(seqs, reverse=True)[0][1:]
    if sequence == 'r':
        return index, field.FIELD[index].index('')
    elif sequence == 'c':
        return [field.FIELD[i][index] for i in range(field.DIM)].index(''), index
    elif sequence == 'd':
        if index:
            y = [field.FIELD[i][field.DIM-i-1] for i in range(field.DIM)].index('')
            x = field.DIM - y - 1
            return y, x
        else:
            y = x = [field.FIELD[i][i] for i in range(field.DIM)].index('')
            return y, x

# для высокого уровня сложности
def ai_turn(symbol_index):
    center = sum(divmod(field.DIM, 2)) - 1
    # поставить в центр
    if not field.FIELD[center][center]:
        return center, center
    else:
        # по диагоналям рядом с центром
        if field.FIELD[center][center] == field.SYMBOLS[symbol_index]:
            if tuple(chain(*field.FIELD)).count(field.SYMBOLS[symbol_index - 1]) < field.DIM - 1:
                for y in (center-1, center+1):
                    for x in (center-1, center+1):
                        if not field.FIELD[y][x]:
                            return y, x
            # заблокировать противника
            y_en, x_en = preferred_seq(field.SYMBOLS[symbol_index - 1])
            # продолжить свой ряд
            y, x = preferred_seq(field.SYMBOLS[symbol_index])
            return y_en, x_en
        # по углам
        else:
            if tuple(chain(*field.FIELD)).count(field.SYMBOLS[symbol_index - 1]) < field.DIM - 1:
                for y in (0, field.DIM - 1):
                    for x in (0, field.DIM - 1):
                        if not field.FIELD[y][x]:
                            return y, x
            # заблокировать противника
            y_en, x_en = preferred_seq(field.SYMBOLS[symbol_index - 1])
            # продолжить свой ряд
            y, x = preferred_seq(field.SYMBOLS[symbol_index])
            return y_en, x_en


