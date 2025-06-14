from system.interface.ListMenu.DynamicButton import DynamicButton
from system.interface.ListMenu.Button import Button
from system.interface.ListMenu.ListMenu import ListMenu
from system.interface.Keyboard.Keyboard import Keyboard
from system.interface.AppRunner.AppRunner import AppRunner
from system.app_template import AppTemplate
from system.util.Configurable import Configurable
import os

class Nmap(AppTemplate):
    def __init__(self):
        self.configurable = Configurable(os.path.join(os.path.dirname(__file__), "config.yaml"))
        super().__init__()

    def get_command(self) -> str:
        command = f"nmap {self.configurable.get_value(['nmap', 'params'])} {self.configurable.get_value(['nmap', 'target'])}"
        return command
        
        
    '''
        DynamicButton has callback in Keyboard to get input update
    '''    


    def menu_init(self):
        nmap_menu = ListMenu(
            "Nmap",
            [
                DynamicButton(
                    "Target ", 
                    self.configurable.get_value,
                    self.configurable.set_value, 
                    ["nmap", "target"], 
                    hop_context=Keyboard()
                ),
                DynamicButton(
                    "Params ", 
                    self.configurable.get_value,
                    self.configurable.set_value, 
                    ["nmap", "params"], 
                    hop_context=Keyboard()
                ),
                Button(
                    "Start",
                    hop_context=AppRunner("Nmap stdout", self.configurable, self.get_command)
                )
            ]
        )
        return nmap_menu
