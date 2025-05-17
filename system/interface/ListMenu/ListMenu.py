from system.interface.menu_template import Menu



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
        return {
            "type": "list",
            "title": self.title,
            "items": visible_items,
            "selected": self.index - self.offset
        }

    def move(self, direction):
        if direction == "LEFT":
            self.items[self.index].handle_left()  # Свайп влево для переключателя
        elif direction == "RIGHT":
            self.items[self.index].handle_right()  # Свайп вправо
        elif direction == "UP":
            if self.index > 0:
                self.index -= 1
                if self.index < self.offset:
                    self.offset -= 1
        elif direction == "DOWN":
            if self.index < len(self.items) - 1:
                self.index += 1
                if self.index >= self.offset + self.max_visible:
                    self.offset += 1

    def ok(self, set_context):
        self.items[self.index].handle_ok(set_context)

    def back(self):
        self.items[self.index].handle_back(backward_context)