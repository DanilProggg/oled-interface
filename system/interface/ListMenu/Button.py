from system.interface.ListMenu.ListMenuItem import ListMenuItem


class Button(ListMenuItem):
    def __init__(self, label, hop_context):
        super().__init__(label)
        self.hop_context = hop_context

    def get_item_text(self) -> str:
        return self.label

    def handle_ok(self, forward_context):
        forward_context(self.hop_context)
        input_logger.debug("Обработано нажатие OK")

    def handle_back(self, backward_context):
        backward_context()
        input_logger.debug("Обработано нажатие BACK")

    def handle_left(self):
        pass

    def handle_right(self):
        pass