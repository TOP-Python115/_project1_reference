# Модуль работы с данными игроков
# Copyright by Gennadiy S. aka GennDALF

from configparser import ConfigParser

import help
import field

SCORES = {}
# SCORES = {'Ivan': [1, 1, 0]}

PLAYER = tuple()
# PLAYER = ('ivan', 'ai1')

SAVES = {}
# SAVES = {('ivan', 'ai1'): [[]],
#          ('ivan', 'oleg'): [[]]}


# читать из конфигурационного файла статистику игроков и их сохранения
def read_ini():
    global SCORES, SAVES
    config = ConfigParser()
    if config.read('data.ini', encoding='utf-8'):
        # статистика побед хранится в виде строки – делаем из неё список чисел
        SCORES = {name.title(): [int(n) for n in score.split(',')]
                  for name, score in config['Scores'].items()}
        # сохранение партии хранится в виде строки – делаем из неё матрицу поля
        SAVES = {tuple(name.split(';')):
                     [[' ' if c == '-' else c for c in matrix[i:i+3]]
                      for i in range(0,9,3)]
                 for name, matrix in config['Saves'].items()}
        # первый запуск приложения
        return True if config['General']['first'] == 'yes' else False
    else:
        raise FileNotFoundError

# сохранить в конфигурационный файл статистику игроков и их сохранения
def save_ini():
    config = ConfigParser()
    # статистику побед записываем для каждого игрока в виде строки
    config['Scores'] = {name: ','.join(str(n) for n in score)
                        for name, score in SCORES.items()}
    # из матрицы поля формируем строку для хранения в конфигурационном файле
    config['Saves'] = {';'.join(name):
                           ''.join(['-' if c == ' ' else c for r in matrix for c in r])
                       for name, matrix in SAVES.items()}
    # если сохраняем данные, значит следующий запуск будет уже не первым
    config['General']['first'] = 'no'
    with open('data.ini', 'w', encoding='utf-8') as config_file:
        config.write(config_file)

# принять на вход имя пользователя или добавить бота или изменить очерёдность хода
def player_name(bot_mode='', *, change_order=False):
    global PLAYER
    # ввод имени первого игрока
    if len(PLAYER) == 0:
        PLAYER = (input(help.MESSAGES[1]).lower(),)
    # ввод второго имени
    elif len(PLAYER) == 1:
        # в этот параметр необходимо передать строку 'ai1' или 'ai2'
        if bot_mode:
            # добавить бота с уровнем сложности
            PLAYER = (PLAYER[0], bot_mode)
        else:
            # ввести имя второго игрока человека
            PLAYER = (PLAYER[0], input(help.MESSAGES[2]).lower())

    # для выбора символа поменять местами элементы кортежа
    # первый играет крестиком и ходит первым
    if change_order:
        PLAYER = (PLAYER[1], PLAYER[0])


# запросить у пользователя режимы игры
def game_mode():
    global PLAYER
    # запрашиваем у игрока режим игры
    while True:
        gm = input(help.MESSAGES[3]).lower()
        if gm in help.ANSWERS[3]:
            break
    # если одиночная
    if gm in help.ANSWERS[3][:3]:
        # есть ли сохранение для одиночной игры
        if save := field.check_saves():
            # восстановление уровня сложности и очерёдности хода из сохранённой партии
            PLAYER = save
            return True
        # запрашиваем у игрока уровень сложности
        while True:
            dl = input(help.MESSAGES[4]).lower()
            if dl in help.ANSWERS[4]:
                break
        # добавляем имя бота к PLAYER
        if dl in help.ANSWERS[4][:3]:
            dl = 'ai1'
        else:
            dl = 'ai2'
        player_name(dl)
    # если парная
    else:
        player_name()
        if save := field.check_saves(single=False):
            # восстановление уровня сложности и очерёдности хода из сохранённой партии
            PLAYER = save
            return True

    # выбор очерёдности хода
    if not (input(help.MESSAGES[5]).lower() in help.ANSWERS[5]):
        player_name(change_order=True)

# изменить статистику
def modify_stats(players):
    global SCORES
    for player_stat in players:
        for player, stat_change in player_stat.items():
            if not player.startswith('ai'):
                SCORES[player] = [SCORES.setdefault(player, [0, 0, 0])[i] + stat_change[i]
                                  for i in range(3)]

# вывести статистику или таблицу результатов
def show_stats(table=False):
    if table:
        pass
    else:
        for player in PLAYER:
            if not player.startswith('ai'):
                print(player.title(), '\t\t', *SCORES[player], '\n')
