from typing import override

from system.app_template import AppTemplate
from system.interface.ListMenu.Button import Button
from system.interface.ListMenu.ListMenu import ListMenu


class Settings(AppTemplate):
    def __init__(self):
        super().__init__()

    @override
    def menu_init(self):
        settings_menu = ListMenu(
            "Settings",
            [
                Button("Setting 1", hop_context=None),
                Button("Setting 2", hop_context=None)
            ]
        )
        return settings_menu