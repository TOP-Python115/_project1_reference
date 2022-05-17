# Основной файл программы Крестики-Нолики
# Copyright by Gennadiy S. aka GennDALF


# импорты
from configparser import ConfigParser


# глобальные переменные
FIELD = [[' ']*3 for _ in range(3)]
PLAYERS = {}
# PLAYERS = {'Ivan': [1, 1, 0]}
SAVES = {}
# SAVES = {('ivan', 'ai1'): [[]],
#          ('ivan', 'oleg'): [[]]}


# функции
def field():
    global FIELD
    pass

def show_help():
    pass

def read():
    global PLAYERS, SAVES
    config = ConfigParser()
    if config.read('data.ini', encoding='utf-8'):
        PLAYERS = {name.title(): [int(n) for n in score.split(',')]
                   for name, score in config['Scores'].items()}
        SAVES = {tuple(name.split(';')):
                     [[' ' if c == '-' else c for c in field[i:i+3]]
                      for i in range(0,9,3)]
                 for name, field in config['Saves'].items()}
        return True if config['General']['first'] == 'yes' else False
    else:
        raise FileNotFoundError

def save():
    config = ConfigParser()
    config['Scores'] = {name: ','.join(str(n) for n in score)
                        for name, score in PLAYERS.items()}
    config['Saves'] = {';'.join(name):
                           ''.join(['-' if c == ' ' else c for r in field for c in r])
                       for name, field in SAVES.items()}
    config['General']['first'] = 'no'
    with open('data.ini', 'w', encoding='utf-8') as config_file:
        config.write(config_file)


# чтение .ini файла
if read():
    show_help()

# запуск суперцикла
while True:
    command = input()

    if command in ('quit', 'выход'):
        # обработка завершения работы приложения
        break

    # ввод имени игрока
