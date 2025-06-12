import yaml
import os
from system.app_template import AppTemplate
from system.interface.ListMenu.Button import Button
from system.interface.ListMenu.ListMenu import ListMenu
from system.interface.FileReader.FileReader import FileReader

import logging
logger = logging.getLogger('debug')

class Explorer(AppTemplate):
    def __init__(self):
        self.config = self.load_config(os.path.join(os.getcwd(), "config.yaml"))
        super().__init__()

        
    
    def load_config(self, path):
            with open(path, "r", encoding="utf-8") as f:
                config = yaml.safe_load(f)
            return config

    def build_menu_from_path(self, path, title=None):
        items = []
        try:
            entries = sorted(os.listdir(path))
        except Exception:
            entries = []

        for entry in entries:
            full_path = os.path.join(path, entry)
            if os.path.isdir(full_path):
                submenu = self.build_menu_from_path(full_path, title=entry)
                items.append(Button(entry, hop_context=submenu))
            else:
                file_reader = FileReader(full_path)
                items.append(Button(entry, hop_context=file_reader))

        return ListMenu(title or os.path.basename(path), items)

    def menu_init(self):
        root_path = self.config["app"]["explorer"]["storage-path"]
        title = os.path.basename(root_path) or "Root"
        return self.build_menu_from_path(root_path, title=title)