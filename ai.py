# Модуль искусственного интеллекта игры
# Copyright by Gennadiy S. aka GennDALF

from random import randrange

import field

# стартовая весовая матрица:
#   [0] для стратегии "от центра" — стратегия крестика
#   [1] стратегии "по углам" — стратегия нолика
WEIGHT = [[[1, 0, 1], [0, 2, 0], [1, 0, 1]],
          [[1, 0, 2], [0, 0, 0], [2, 0, 1]]]


# для низкого уровня сложности
def random_turn():
    while True:
        y, x = randrange(field.DIM), randrange(field.DIM)
        if not field.FIELD[y][x]:
            break
    return y, x

# для высокого уровня сложности
# принимает индекс очерёдности хода
def ai_turn(s_ind):
    global WEIGHT
    #
    empweights_matrix = empty_weights(symbols_weights(field.FIELD, s_ind))
    #
    WEIGHT[s_ind] = clear_empweights(mat_sum(WEIGHT[s_ind], empweights_matrix))
    #
    y, x = mat_mx_ind(WEIGHT[s_ind])
    return y, x

# возвращает из матрицы ряд, в котором находится ячейка
def row_for_cell(matrix, y):
    return tuple(matrix[y])

# возвращает из матрицы столбец, в котором находится ячейка
def column_for_cell(matrix, x):
    return tuple(matrix[i][x] for i in range(field.DIM))

# возвращает из матрицы диагональ, в которой находится ячейка
def diagonal_for_cell(matrix, y, x):
    # главная диагональ
    if y == x:
        return tuple(matrix[i][i] for i in range(field.DIM))
    # побочная диагональ
    elif y == field.DIM - x - 1:
        return tuple(matrix[i][field.DIM - i - 1] for i in range(field.DIM))
    else:
        return tuple()

# возвращает сумму n матриц
def mat_sum(*matrices):
    return [[sum(m[i][j] for m in matrices) for j in range(field.DIM)]
            for i in range(field.DIM)]

# возвращает индексы максимального значения в матрице
def mat_mx_ind(matrix):
    mx, res = 0, tuple()
    for i in range(field.DIM):
        for j in range(field.DIM):
            if mx < matrix[i][j]:
                mx, res = matrix[i][j], (i, j)
    return res

# возвращает матрицу весов занятых ячеек для матрицы поля
def symbols_weights(field_matrix, s_ind):
    # устанавливает соответствие весов символам
    def weight_map(seq):
        res = tuple()
        for el in seq:
            if el:
                # для своего символа
                if el == field.SYMBOLS[s_ind]:
                    res += (1.5, )
                # для символа соперника
                elif el == field.SYMBOLS[s_ind - 1]:
                    res += (1, )
            # для пустого поля
            else:
                res += (0, )
        return res
    return tuple(map(weight_map, field_matrix))

# возвращает матрицу весов незанятых ячеек
def empty_weights(symweights_matrix):
    res = [[0] * field.DIM for _ in range(field.DIM)]
    for i in range(field.DIM):
        for j in range(field.DIM):
            if not symweights_matrix[i][j]:
                # если в последовательности присутствуют только крестики или только нолики,
                #   то вычислить квадрат суммы весов занятых ячеек
                if len(set(r := row_for_cell(symweights_matrix, i)) - {0}) == 1:
                    res[i][j] += int(sum(r)**2)
                if len(set(c := column_for_cell(symweights_matrix, j)) - {0}) == 1:
                    res[i][j] += int(sum(c)**2)
                if len(set(d := diagonal_for_cell(symweights_matrix, i, j)) - {0}) == 1:
                    res[i][j] += int(sum(d)**2)
    return res

def clear_empweights(turnweights_matrix):
    for i in range(field.DIM):
        for j in range(field.DIM):
            if field.FIELD[i][j]:
                turnweights_matrix[i][j] = 0
    return turnweights_matrix
