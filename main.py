# Модуль верхнего уровня приложения Крестики-Нолики
# Copyright by Gennadiy S. aka GennDALF

from players import *
from help import show_help, show_message


# приветствие
show_message('КРЕСТИКИ-НОЛИКИ')

# чтение .ini файла
if read_ini():
    show_help()

# запуск суперцикла
while True:
    command = input('_> ')

    if command in ('quit', 'выход'):
        # обработка завершения работы приложения
        break

    # ввод имени игрока
