import asyncio
from typing import Deque

from system.app_template import AppTemplate
from system.apps.settings.main import Settings
from system.apps.explorer.main import Explorer
from system.apps.apps_explorer.main import AppsExplorer
from system.interface.ListMenu.Button import Button
from system.interface.ListMenu.ListMenu import ListMenu

from system.interface.menu_template import Menu
from system.input import InputHandler
from system.display import DisplayManager
from collections import deque

import logging
from system.logger.logger_ini import setup_logging_from_json

# Инициализация логирования
setup_logging_from_json("./system/logger/logger.json")
logger = logging.getLogger("debug")

"""
При запуске системы должны инициализироваться:
- дисплей
- устройства ввода
- загружаться все модули
"""

class Core:
    def __init__(self):
        logger.debug("Запуск инициализации ядра")
        self.display = DisplayManager()             # Дисплей
        self.input_handler = InputHandler()         # Обработчик нажатий
        self.app_loader = None                      # Загрузчик модулей
        self.current_context = self.build_system_menu()  # Функция, что возвращает меню
        self.menu_stack = deque()                   # Стек с меню
        logger.info("Успешная инициализация ядра")

    #
    #   ОДНОРАЗОВОЕ СОЗДАНИЕ ГЛАВНОГО (СИСТЕМНОГО МЕНЮ)
    #
    def build_system_menu(self):
        logger.debug("Формирование системного меню")
        buttons = []

        app_classes = [AppsExplorer, Settings, Explorer]  # Тут можно динамически загружать из папки

        # Создаем кнопки для каждого приложения
        for app_class in app_classes:
            app_instance = app_class()  # Создаем экземпляр приложения
            menu = app_instance.menu_init()  # Получаем меню
            buttons.append(Button(menu.title, hop_context=menu))

        system_menu = ListMenu("Main Menu", buttons)
        return system_menu
    

    # СМЕНА КОНТЕКСТА
    def switch_context(self, new_context=None):
        if new_context is not None:
            logger.info(f"Попытка сменить контекст на {new_context}")
            self.menu_stack.append(self.current_context)
            self.current_context = new_context
            logger.info(f"Контекст сменён на {self.current_context.title}")
        else:
            logger.info("Попытка вернуться на предыдущий контекст")
            if self.menu_stack:
                del self.current_context
                self.current_context = self.menu_stack.pop()
                logger.info(f"Контекст сменён на {self.current_context.title}")
            else:
                logger.warning("Меню-стек пуст. Возврат невозможен.")
    #
    #   ОБРАБОТКА НАЖАТИЙ  временно pygame
    #
    async def input_action(self):
        while True:
            action = self.input_handler.get_action()
            if action == "OK":
                self.current_context.ok(self.switch_context)
            elif action == "BACK":
                self.current_context.back(self.switch_context)
            elif action == "LEFT":
                self.current_context.move("LEFT")
            elif action == "RIGHT":
                self.current_context.move("RIGHT")
            elif action == "UP":
                self.current_context.move("UP")
            elif action == "DOWN":
                self.current_context.move("DOWN")

            await asyncio.sleep(0.2)

    async def draw_display(self):
        while True:
            self.display.draw(self.current_context)
            await asyncio.sleep(0.2)

    async def run(self):
        input_task = asyncio.create_task(self.input_action())      #задача для ввода
        display_task = asyncio.create_task(self.draw_display())    #задача для вывода
        await asyncio.gather(input_task, display_task)

if __name__ == "__main__":
    core = Core()
    asyncio.run(core.run())
