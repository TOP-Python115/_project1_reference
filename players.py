# Модуль работы с данными игроков
# Copyright by Gennadiy S. aka GennDALF

from configparser import ConfigParser
from help import MESSAGES, ANSWERS
from field import check_saves

SCORES = {}
# PLAYERS = {'Ivan': [1, 1, 0]}

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
                     [[' ' if c == '-' else c for c in field[i:i+3]]
                      for i in range(0,9,3)]
                 for name, field in config['Saves'].items()}
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
                           ''.join(['-' if c == ' ' else c for r in field for c in r])
                       for name, field in SAVES.items()}
    # если сохраняем данные, значит следующий запуск будет уже не первым
    config['General']['first'] = 'no'
    with open('data.ini', 'w', encoding='utf-8') as config_file:
        config.write(config_file)

# принять на вход имя пользователя или добавить бота или изменить очерёдность хода
def player_name(bot_mode='', *, change_order=False):
    global PLAYER
    # ввод имени первого игрока
    if len(PLAYER) == 0:
        PLAYER = (input(MESSAGES[1]).lower(), )
    # ввод второго имени
    elif len(PLAYER) == 1:
        # в этот параметр необходимо передать строку 'ai1' или 'ai2'
        if bot_mode:
            # добавить бота с уровнем сложности
            PLAYER = (PLAYER[0], bot_mode)
        else:
            # ввести имя второго игрока человека
            PLAYER = (PLAYER[0], input(MESSAGES[2]).lower())

    # для выбора символа поменять местами элементы кортежа
    # первый играет крестиком и ходит первым
    if change_order:
        PLAYER = (PLAYER[1], PLAYER[0])


# запросить у пользователя режимы игры
def game_mode():
    global PLAYER
    # запрашиваем у игрока режим игры
    while True:
        gm = input(MESSAGES[3]).lower()
        if gm in ANSWERS[3]:
            break
    # если одиночная
    if gm in ANSWERS[3][:3]:
        # есть ли сохранение для одиночной игры
        if save := check_saves():
            # восстановление уровня сложности и очерёдности хода из сохранённой партии
            PLAYER = save
            return True
        # запрашиваем у игрока уровень сложности
        while True:
            dl = input(MESSAGES[4]).lower()
            if dl in ANSWERS[4]:
                break
        # добавляем имя бота к PLAYER
        if dl in ANSWERS[4][:3]:
            dl = 'ai1'
        else:
            dl = 'ai2'
        player_name(dl)
    # если парная
    else:
        player_name()
        if save := check_saves(single=False):
            # восстановление уровня сложности и очерёдности хода из сохранённой партии
            PLAYER = save
            return True

    # выбор очерёдности хода
    if not (input(MESSAGES[5]).lower() in ANSWERS[5]):
        player_name(change_order=True)
