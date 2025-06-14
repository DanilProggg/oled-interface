from system.interface.ListMenu.DynamicButton import DynamicButton
from system.interface.ListMenu.ListMenu import ListMenu
from system.interface.Keyboard.Keyboard import Keyboard
from system.app_template import AppTemplate
from system.util.Configurable import Configurable
import os

class Nmap(AppTemplate, Configurable):
    def __init__(self):
        self.config_path = os.path.join(os.path.dirname(__file__), "config.yaml")
        Configurable.__init__(self, self.config_path)
        AppTemplate.__init__(self)
        
        

    def menu_init(self):
        nmap_menu = ListMenu(
            "Nmap",
            [
                DynamicButton(
                    "Target ", 
                    self.get_value,
                    self.set_value, 
                    ["nmap", "target"], 
                    hop_context=Keyboard()
                )
            ]
        )
        return nmap_menu
