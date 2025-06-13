from system.app_template import AppTemplate
from system.interface.ListMenu.Button import Button
from system.interface.ListMenu.ListMenu import ListMenu
import logging
import os, sys
import importlib.util
import inspect

logger = logging.getLogger("debug")

class AppsExplorer(AppTemplate):
    def __init__(self):
        super().__init__()

    def menu_init(self):
        return self.build_system_menu()

    def load_classes_from_main(self, py_path):
        logger.debug(f"Загрузка классов из {py_path}")
        classes = []

        spec = importlib.util.spec_from_file_location("main_module", py_path)
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            for name, obj in inspect.getmembers(module, inspect.isclass):
                if issubclass(obj, AppTemplate) and obj is not AppTemplate:
                    if not inspect.isabstract(obj):
                        logger.debug(f"Найден класс-приложение: {name}")
                        classes.append(obj)
                    else:
                        logger.debug(f"Пропускаем абстрактный AppTemplate-подкласс: {name}")
                else:
                    logger.debug(f"Пропускаем посторонний класс: {name}")

        else:
            logger.warning(f"Не удалось загрузить модуль из {py_path}")

        return classes



    def build_system_menu(self):
        logger.debug("Формирование меню Apps Explorer")
        buttons = []

        core_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
        apps_dir = os.path.join(core_dir, "apps")
        logger.debug(f"Путь к папке приложений: {apps_dir}")

        app_classes = []

        for entry in os.listdir(apps_dir):
            entry_path = os.path.join(apps_dir, entry)
            main_path = os.path.join(entry_path, "main.py")

            logger.debug(f"Проверяем {entry_path}")
            if os.path.isdir(entry_path) and os.path.isfile(main_path):
                logger.debug(f"Найдена папка с main.py: {entry_path}")
                found_classes = self.load_classes_from_main(main_path)
                logger.debug(f"Найдено классов: {len(found_classes)} в {main_path}")
                app_classes.extend(found_classes)
            else:
                logger.debug(f"Пропускаем {entry_path} — не папка с main.py")

        for app_class in app_classes:
            logger.debug(f"Создаём экземпляр класса {app_class.__name__}")
            app_instance = app_class()
            menu = app_instance.menu_init()
            buttons.append(Button(menu.title, hop_context=menu))

        system_menu = ListMenu("Apps", buttons)
        logger.debug(f"Меню сформировано с {len(buttons)} кнопками")
        return system_menu
