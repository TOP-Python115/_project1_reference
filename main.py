# Модуль верхнего уровня приложения Крестики-Нолики
# Copyright by Gennadiy S. aka GennDALF

from players import *
from help import show_help, show_message, COMMANDS, MESSAGES


# приветствие
show_message('КРЕСТИКИ-НОЛИКИ')

# чтение .ini файла
if read_ini():
    show_help()

# запуск суперцикла
while True:
    command = input(MESSAGES[0]).lower()

    # выход из программы
    if command in COMMANDS['quit']:
        # обработка завершения работы приложения
        break
    # показать справку
    elif command in COMMANDS['help']:
        show_help()
    # показать таблицу результатов
    elif command in COMMANDS['scores']:
        pass
    # начало новой партии
    elif command in COMMANDS['new']:
        # есть ли текущий игрок
        if not PLAYER:
            # запрос имени игрока
            player_name()
        #
        if game_mode():
            # продолжаем сохранённую партию
            pass
        else:
            # начинаем новую партию
            pass

