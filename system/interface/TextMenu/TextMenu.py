import yaml
import os
from system.util.Configurable import Configurable

import logging
logger = logging.getLogger("debug")

class TextMenu:
    def __init__(self, title):
        self.title = title
        #yaml config
        self.textmenu_configurable = Configurable(os.path.join(os.getcwd(), "config.yaml"))
        
        #Output params
        self.lines = []
        self.offset = 0
        self.CHARS_IN_LINE = self.textmenu_configurable.get_value(["app", "text-output", "chars-in-line"])
        self.max_visible = self.textmenu_configurable.get_value(["app", "text-output", "visible-lines"])


    def get_draw_data(self):
        visible_lines = self.lines[self.offset:self.offset + self.max_visible]
        draw_data = {
            "type": "text_output",
            "lines": visible_lines,
            "title": self.title
        }
        logger.debug(draw_data)
        return draw_data

    def move(self, direction):
        if direction == "UP":
            if self.offset > 0:
                self.offset -= 1
        elif direction == "DOWN":
            if self.offset + self.max_visible < len(self.lines):
                self.offset += 1
        logger.debug(f"Move: {direction}, offset={self.offset}")