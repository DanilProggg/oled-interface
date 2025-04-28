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
        self.current_context = None                 # Функция, что возвращает меню
        self.menu_stack = deque()                   # Стек с меню

    def build_system_menu(self):
        buttons = []

        app_classes = [Settings]  # Тут можно динамически загружать из папки

        # Создаем кнопки для каждого приложения
        for app_class in app_classes:
            app_instance = app_class()  # Создаем экземпляр приложения
            menu = app_instance.menu_init()  # Получаем меню
            buttons.append(Button(menu.title, hop_context=menu))

        system_menu = ListMenu("Main Menu", *buttons)
        return system_menu
    
    async def process_action(self):
        while True:
            action = self.input_handler.get_action()

    async def run(self):
        input_task = asyncio.create_task()      #задача для ввода
        display_task = asyncio.create_task()    #задача для вывода
        await asyncio.gather(input_task, display_task)
