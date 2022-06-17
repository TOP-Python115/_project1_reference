# Модуль работы со справкой
# Copyright by Gennadiy S. aka GennDALF

from shutil import get_terminal_size as gts
from math import ceil, floor

import field

COMMANDS = {'quit': ('quit', 'выход', 'q'),
            'help': ('help', 'помощь', 'h', '?'),
            'scores': ('scores', 'таблица'),
            'new': ('new', 'новая', 'yes', 'да', 'y', 'д', '1'),
            '': (),
            }
MESSAGES = ('хотите начать новую партию? > ',
            'введите имя игрока > ',
            'введите имя второго игрока > ',
            'выберите режим игры:\n  1 - с ботом\n  2 - с человеком\n> ',
            'выберите уровень сложности:\n  1 - лёгкий\n  2 - трудный\n> ',
            'вы хотите ходить первым? > ',
            'вы хотите загрузить сохранённую партию? > ',
            )
ANSWERS = (None,
           None,
           None,
           ('1', 'бот', 'б', '2', 'человек', 'ч'),
           ('1', 'лёгкий', 'л', '2', 'трудный', 'т'),
           ('yes', 'да', 'y', 'д', '1'),
           ('yes', 'да', 'y', 'д', '1'),
           )

h_r = f"""Правила игры:
    Вы играете одним из двух символов: крестиком '{field.SYMBOLS[0]}' или ноликом '{field.SYMBOLS[1]}'. Первым составьте последовательность из {field.DIM} символов в одной строке, в одном столбце, либо в одной диагонали."""
h_c1 = f"""Список команд:
Между партиями вы можете использовать следующие команды:"""


def show_help():
    print(h_r, end='\n\n')
    field.show_field([[f'{i},{j}' for j in range(field.DIM)]
                      for i in range(field.DIM)], center=True)
    print(h_c1, end='\n\n')
    print('\n'.join(['  ' + ' '.join(COMMANDS[comm]) for comm in COMMANDS]))

def show_message(text=''):
    width = gts()[0] - 1
    half_width = (width - len(text) - 2) / 2
    m = (f"\n{'#' * width}"
         + f"\n{'#' + ' ' * (width - 2) + '#'}"
         + f"\n{'#' + ' ' * ceil(half_width) + text.upper() + ' ' * floor(half_width) + '#'}"
         + f"\n{'#' + ' ' * (width - 2) + '#'}"
         + f"\n{'#' * width}")
    print(m, end='\n\n')
