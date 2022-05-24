# Модуль работы со справкой
# Copyright by Gennadiy S. aka GennDALF

from shutil import get_terminal_size as gts
from math import floor, ceil

COMMANDS = {'quit': ('quit', 'выход'),
            'help': ('help', 'помощь', 'h', '?'),
            'scores': ('scores', 'таблица'),
            'new': ('new', 'новая', 'yes', 'да', 'y', 'д'),
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
           ('yes', 'да', 'y', 'д'),
           ('yes', 'да', 'y', 'д'),
           )


h = f"""Правила игры:

Список команд:
{' '.join(COMMANDS['quit'])}
"""


def show_help():
    print(h)

def show_message(text=''):
    width = gts()[0] - 1
    half_width = (width - len(text) - 2) / 2
    m = (f"\n{'#' * width}"
         + f"\n{'#' + ' ' * (width - 2) + '#'}"
         + f"\n{'#' + ' ' * ceil(half_width) + text.upper() + ' ' * floor(half_width) + '#'}"
         + f"\n{'#' + ' ' * (width - 2) + '#'}"
         + f"\n{'#' * width}")
    print(m, end='\n\n')
