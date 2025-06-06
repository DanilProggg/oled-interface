from system.app_template import AppTemplate
from system.interface.ListMenu.Button import Button
from system.interface.ListMenu.ListMenu import ListMenu
from system.interface.keyboard import Keyboard
from system.apps.settings.modules.ssh.ssh import SshModule


class Settings(AppTemplate):
    def __init__(self):
        self.ssh = SshModule()
        self.test_keyboard = Keyboard()
        super().__init__()

    def menu_init(self):
        settings_menu = ListMenu(
            "Settings",
            [
                Button(self.ssh.menu.title, hop_context=self.ssh.menu_init()),
                Button("Setting 2", hop_context=None),
                Button("Test keyboard", hop_context=self.test_keyboard)
            ]
        )
        return settings_menu

