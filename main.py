# Модуль верхнего уровня приложения Крестики-Нолики
# Copyright by Gennadiy S. aka GennDALF

from players import read_ini, player_name, game_mode, modify_stats, show_stats, PLAYER
from help import show_help, show_message, COMMANDS, MESSAGES
from field import game


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
        show_stats(table=True)
    # начало новой партии
    elif command in COMMANDS['new']:
        # есть ли текущий игрок
        if not PLAYER:
            # запрос имени игрока
            player_name()
        # запрос режимов игры
        if game_mode():
            # продолжаем сохранённую партию
            modify_stats(game(load=True))
        else:
            # начинаем новую партию
            modify_stats(game())
        # после завершения партии показываем статистику
        #   для участвовавших игроков людей
        show_stats()
