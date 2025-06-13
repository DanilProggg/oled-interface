import yaml
import os

import logging
logger = logging.getLogger("debug")

class TextMenu:
    def __init__(self):
        #yaml config
        self.config = self.load_config(os.path.join(os.getcwd(), "config.yaml"))
        
        #Output params
        self.lines = []
        self.offset = 0
        self.CHARS_IN_LINE = self.config["app"]["text-output"]["chars-in-line"]
        self.max_visible = self.config["app"]["text-output"]["visible-lines"]

    def load_config(self, path):
        with open(path, "r") as file:
            return yaml.safe_load(file)


    def get_draw_data(self):
        visible_lines = self.lines[self.offset:self.offset + self.max_visible]
        draw_data = {
            "type": "text_output",
            "lines": visible_lines,
            "title": self.filename
        }
        return draw_data

    def move(self, direction):
        if direction == "UP":
            if self.offset > 0:
                self.offset -= 1
        elif direction == "DOWN":
            if self.offset + self.max_visible < len(self.lines):
                self.offset += 1
        logger.debug(f"Move: {direction}, offset={self.offset}")