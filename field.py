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
# отладка
DEBUG = True


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

# проверка на победу или ничью
def check_win_or_tie():
    # локальная функция: проверка на победу
    def check_win():
        # транспонированная матрица поля: для упрощения перебора
        #   столбцы прямой матрицы станут строками в транспонированной
        FIELD_T = [[FIELD[j][i] for j in range(DIM)] for i in range(DIM)]
        # список из главной и побочной диагоналей
        DIAGONALS = ([FIELD[i][i] for i in range(DIM)],
                     [FIELD[i][DIM-i-1] for i in range(DIM)])
        # перебираем прямую и транспонированную матрицы
        for matrix in (FIELD, FIELD_T, DIAGONALS):
            # есть ли ряд, целиком заполненный только одним символом
            if 1 in [len(set(row)) for row in matrix if all(row)]:
                # локальную функцию делали, чтобы не выполнять дальнейшие проверки,
                #   как только будет найдена первая победная комбинация
                return True
    # нет пустых  победа  ничья
    #   False     False   False
    #   False     True    False
    #   True      False   True
    #   True      True    False
    win = check_win()
    return win, all([all(row) for row in FIELD]) and not win

# одна партия
def game(load=False):
    global FIELD
    # одиночная False или парная True игра
    flag = set(players.PLAYER).isdisjoint({'ai1', 'ai2'})
    # флаг победы [0] или ничьей [1]
    win_or_tie = (False, False)
    # цикл для одной партии
    while not any(win_or_tie):
        # перебираем игроков в кортеже
        for i in range(2):
            # выбор приглашения для ввода
            prompt = ('ваш ход > ', f'ход игрока {players.PLAYER[i].title()} > ')[flag]
            # запросить ход бота
            if players.PLAYER[i].startswith('ai'):
                # в случае загружаемой партии c ботом, когда игрок ходит ноликом (вторым),
                #   переключаем параметр load и переходим к следующей итерации
                #   цикла for (следующему ходу)
                if load and not i:
                    load = False
                    continue
                # проверяем уровень сложности
                y, x = ai.random_turn() if players.PLAYER[i][-1] == '1' else ai.ai_turn(i)
            # запросить ход игрока
            else:
                # в случае загружаемой партии c игроком, когда первый ход в возобновлённой
                #   партии должен быть за вторым игроком, переключаем параметр load
                #   и переходим к следующей итерации цикла for (следующему ходу)
                if load and len([cell for row in FIELD for cell in row if cell]) % 2 != i:
                    load = False
                    continue
                # запрашиваем у игрока координаты пока он не укажет незанятую клетку
                while True:
                    y, x = map(int, input(prompt).split())
                    if not FIELD[y][x]:
                        break
            # обновляем матрицу поля
            FIELD[y][x] = SYMBOLS[i]
            # выводим поле с очередным ходом: слева или справа
            #   в зависимости от очерёдности хода
            if DEBUG:
                show_field(FIELD, ai.WEIGHT[bool(i)], right=bool(i))
            else:
                show_field(FIELD, right=bool(i))
            # проверяем, является ли данный ход завершающим
            win_or_tie = check_win_or_tie()
            # ещё не закончили
            if not any(win_or_tie):
                continue
            # чья-то победа
            elif win_or_tie[0]:
                # сообщение о победе игрока
                help.show_message(f'Победил игрок {players.PLAYER[i]}!')
                # очищаем поле
                FIELD = [['']*DIM for _ in range(DIM)]
                # Иван проиграл, а Олег выиграл
                #   ({'ivan': [0, 1, 0]}, {'oleg': [1, 0, 0]})
                return {players.PLAYER[i]: [1, 0, 0]}, {players.PLAYER[i-1]: [0, 1, 0]}
            # ничья
            elif win_or_tie[1]:
                # сообщение о ничьей
                help.show_message('Ничья!')
                # очищаем поле
                FIELD = [['']*DIM for _ in range(DIM)]
                # у обоих ничья
                #   ({'ivan': [0, 0, 1]}, {'oleg': [0, 0, 1]})
                return {players.PLAYER[i]: [0, 0, 1]}, {players.PLAYER[i-1]: [0, 0, 1]}
