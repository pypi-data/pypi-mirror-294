import logging
import sys


# # Создание логгера с именем вашего фреймворка
# logger = logging.getLogger('qagalaxy')
#
# # Установка уровня логирования (по умолчанию)
# logger.setLevel(logging.DEBUG)
#
# # Создание консольного обработчика с простым форматом
# ch = logging.StreamHandler()
# ch.setLevel(logging.DEBUG)
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# ch.setFormatter(formatter)
#
# # Добавление обработчика к логгеру
# logger.addHandler(ch)


# def setup_logging(level=logging.DEBUG):
#     logging.basicConfig(
#         format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
#         level=level
#     )
def setup_logging(level=logging.DEBUG):
    # Создаём корневой логгер
    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    if not logger.hasHandlers():
        # Создаём консольный обработчик (StreamHandler)
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)

        # Создаём форматтер и добавляем его к консольному обработчику
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)

        # Добавляем консольный обработчик к корневому логгеру
        root_logger.addHandler(console_handler)

    # # Если нужно, настройка отдельных логгеров для частей библиотеки
    # my_lib_logger = logging.getLogger('my_lib')
    # my_lib_logger.setLevel(level)
    # my_lib_logger.propagate = False
    # my_lib_logger.addHandler(console_handler)
    #
    # # Пример настройки логгера для подмодуля
    # folder2_logger = logging.getLogger('my_lib.folder1.folder2')
    # folder2_logger.setLevel(logging.ERROR)  # Например, для этого логгера включаем только ERROR
    # folder2_logger.propagate = False
    # folder2_logger.addHandler(console_handler)

    # Отключаем логи для встроенных и сторонних библиотек
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('asyncio').setLevel(logging.WARNING)
    logging.getLogger('selenium').setLevel(logging.WARNING)


logger = logging.getLogger('sputnikqa')
