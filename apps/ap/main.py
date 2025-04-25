from system.app_template import AppTemplate
from system.interface.list_menu import ListMenu, ListMenuItem, Button


class AccessPoint(AppTemplate):
    def __init__(self):
        super().__init__()


    def menu_init(self):
        menu = ListMenu(
            "AP",
            [
                Button("Запустить", hop_context=None)
            ]
        )
        return menu

