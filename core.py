import asyncio
from typing import Deque

from system.apps.settings import Settings
from system.interface.list_menu import ListMenu, Button
from system.interface.menu_template import Menu
from system.input import InputHandler
from collections import deque

"""
При запуске системы должны инициализироваться:
- дисплей
- устройства ввода
- загружаться все модули
"""

class System:
    def __init__(self):
        self.display = None                         # Дисплей
        self.input_handler = InputHandler()         # Обработчик нажатий
        self.app_loader = None                      # Загрузчик модулей
        self.current_context = None                 # Функция, что возвращает меню
        self.menu_stack = deque()                   # Стек с меню

    def build_system_menu(self):
        system_menu = ListMenu(
            "Main menu",
            Button("Apps", hop_context=None),
            Button("Setting", hop_context=Settings().menu_init())
        )
    
    async def process_action(self):
        while True:
            action = self.input_handler.get_action()

    async def run(self):
        input_task = asyncio.create_task()      #задача для ввода
        display_task = asyncio.create_task()    #задача для вывода
        await asyncio.gather(input_task, display_task)
