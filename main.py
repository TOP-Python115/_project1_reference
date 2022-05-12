# импорты



# глобальные переменные
FIELD = [['']*3 for _ in range(3)]


# функции
def field():
    global FIELD
    pass


# чтение .ini файла


# запуск суперцикла
while True:
    command = input()

    if command in ('quit', 'выход'):
        # обработка завершения работы приложения
        break

    # ввод имени игрока
