from system.interface.menu_template import Menu
import logging

logger = logging.getLogger("debug")

class ListMenu(Menu):
    def __init__(self, title: str, items):
        super().__init__(title)
        self.index = 0
        self.items = items
        self.max_visible = 10
        self.offset = 0

    #Получение видимых элементов
    def get_visible_items(self):
        return self.items[self.offset:self.offset + self.max_visible]

    def get_draw_data(self):
        visible_items = self.get_visible_items()
        draw_data = {
            "type": "list",
            "title": self.title,
            "items": visible_items,
            "selected": self.index - self.offset
        }
        logger.debug("Draw data: %s", draw_data)
        return draw_data

    def move(self, direction):
        if self.items:
            if direction == "LEFT":
                self.items[self.index].handle_left()  # Свайп влево для переключателя
                logger.debug("Обработано нажатие LEFT")
            elif direction == "RIGHT":
                self.items[self.index].handle_right()  # Свайп вправо
                logger.debug("Обработано нажатие RIGHT")
            elif direction == "UP":
                if self.index > 0:
                    self.index -= 1
                    if self.index < self.offset:
                        self.offset -= 1
                logger.debug("Обработано нажатие UP")
            elif direction == "DOWN":
                if self.index < len(self.items) - 1:
                    self.index += 1
                    if self.index >= self.offset + self.max_visible:
                        self.offset += 1
                logger.debug("Обработано нажатие DOWN")

    def ok(self, switch_context):
        self.items[self.index].handle_ok(switch_context)

    def back(self, switch_context):
        switch_context()