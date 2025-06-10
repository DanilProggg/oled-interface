from system.app_template import AppTemplate
from system.interface.ListMenu.Button import Button
from system.interface.ListMenu.ListMenu import ListMenu

class SshModule(AppTemplate):

    def __init__(self):
           super().__init__()

    def menu_init(self):
        settings_menu = ListMenu(
            "SSH Settings",
            [
                Button("SSH1", hop_context=None),
                Button("SSH2", hop_context=None)
            ]
        )
        return settings_menu