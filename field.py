# Модуль работы с полем игры
# Copyright by Gennadiy S. aka GennDALF

from shutil import get_terminal_size as gts

import players
import help
import ai

# размерность поля
DIM = 3
# матрица поля
FIELD = [['']*DIM for _ in range(DIM)]
# символы
SYMBOLS = ('X', 'O')


# проверка наличия сохранённой партии
def check_saves(single=True):
    global FIELD
    # для парной игры
    s = set(players.PLAYER)
    # для одиночной игры
    if single:
        s |= {'ai1', 'ai2'}
    for save in players.SAVES:
        if set(save).issubset(s):
            # хочет ли игрок загрузить найденную партию
            load = input(help.MESSAGES[6]).lower()
            if load in help.ANSWERS[6]:
                FIELD = players.SAVES[save]
                return save
    return False

# отображение поля
def show_field(matrix, *matrices, right=False, center=False):
    # одна матрица есть обязательно, другие опционально
    matrices = (matrix, ) + matrices
    # количество переданных матриц для отображения
    n = len(matrices)
    # список для строк с рядами матриц, список с шириной каждой матрицы, интервал между матрицами
    rows, m_wd, pad = [''] * DIM, [], ' '*4
    # ширина терминала
    term_wd = gts()[0] - 1
    # перебор переданных матриц
    for i in range(n):
        # длина строки с максимальным количеством символов
        mx = max([len(str(cell)) for row in matrices[i] for cell in row])
        # количество символов-заполнителей для горизонтальной линии-разделителя
        m_wd += [mx*DIM + DIM*3 - 1]
        for j in range(DIM):
            # формирование списка выводимых строк со значениями
            r = '|'.join([str(cell).center(mx + 2) for cell in matrices[i][j]])
            # дописать строку из очередной матрицы к уже имеющейся непустой строке
            rows[j] = pad.join(s for s in (rows[j], r) if s)
    # общая ширина строки с рядами матриц
    tot_m_wd = len(pad) * (n - 1) + sum(m_wd)
    # отступ для выравнивания вывода слева, по центру или справа
    margin = (' ' * (term_wd - tot_m_wd)
                if right else
              ' ' * ((term_wd - tot_m_wd) // 2)
                if center else ' ')
    rows = [margin + row for row in rows]
    # вывод строк со значениями с горизонтальными линиями-разделителями
    print(('' if center else '\n')
          + ('\n' + margin + pad.join(['—'*wd for wd in m_wd]) + '\n').join(rows)
          + '\n')
