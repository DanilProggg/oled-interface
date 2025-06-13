import yaml
import os
from system.app_template import AppTemplate
from system.interface.ListMenu.Button import Button
from system.interface.ListMenu.ListMenu import ListMenu
from system.interface.FileReader.FileReader import FileReader
from system.util.Configurable import Configurable

import logging
logger = logging.getLogger('debug')

class Explorer(AppTemplate, Configurable):
    def __init__(self):
        Configurable.__init__(self, os.path.join(os.getcwd(), "config.yaml"))
        AppTemplate.__init__(self)

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