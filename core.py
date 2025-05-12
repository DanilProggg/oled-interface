import asyncio
from typing import Deque

from system.app_template import AppTemplate
from system.apps.Settings import Settings
from system.interface.ListMenu.Button import Button
from system.interface.ListMenu.ListMenu import ListMenu

from system.interface.menu_template import Menu
from system.input import InputHandler
from collections import deque

"""
При запуске системы должны инициализироваться:
- дисплей
- устройства ввода
- загружаться все модули
"""

class Core:
    def __init__(self):
        self.display = None                         # Дисплей
        self.input_handler = InputHandler()         # Обработчик нажатий
        self.app_loader = None                      # Загрузчик модулей
        self.current_context = build_system_menu()  # Функция, что возвращает меню
        self.menu_stack = deque()                   # Стек с меню

    #
    #   ОДНОРАЗОВОЕ СОЗДАНИЕ ГЛАВНОГО (СИСТЕМНОГО МЕНЮ)
    #
    def build_system_menu(self):
        buttons = []

        app_classes = [Settings]  # Тут можно динамически загружать из папки

        # Создаем кнопки для каждого приложения
        for app_class in app_classes:
            app_instance = app_class()  # Создаем экземпляр приложения
            menu = app_instance.menu_init()  # Получаем меню
            buttons.append(Button(menu.title, hop_context=menu))

        system_menu = ListMenu("Main Menu", buttons)
        return system_menu
    

    # СМЕНА КОНТЕКСТА
    def set_context(self, hop_context):
        self.menu_stack.append(self.current_context)
        self.current_context = hop_context

    #
    #   ОБРАБОТКА НАЖАТИЙ  временно pygame
    #
    async def input_action(self):
        while True:
            action = self.input_handler.get_action()
            if action == "OK:
                current_context.ok(set_context)
            elif action == "BACK":
                current_context.back()
            elif action == "LEFT":
                current_context.move("LEFT")
            elif action == "RIGHT":
                current_context.move("RIGHT")
            elif action == "UP":
                current_context.move("UP")
            elif action == "DOWN":
                current_context.move("DOWN")

            await asyncio.sleep(0.2)

    async def draw_display(self):
        while True:
            self.current_context.draw()
            await asyncio.sleep(0.2)

    async def run(self):
        input_task = asyncio.create_task(self.input_action())      #задача для ввода
        display_task = asyncio.create_task(self.draw_display())    #задача для вывода
        await asyncio.gather(input_task, display_task)
