from system.interface.ListMenu.ListMenuItem import ListMenuItem
import logging

logger = logging.getLogger("debug")


class Button(ListMenuItem):
    def __init__(self, label, hop_context=None, action=None):
        self.hop_context = hop_context
        self.action = action
        super().__init__(label)

    def get_item_text(self) -> str:
        return self.label

    def handle_ok(self, forward_context):
        forward_context(self.hop_context)
        logger.debug("Обработано нажатие OK")

    def handle_back(self, backward_context):
        backward_context()
        logger.debug("Обработано нажатие BACK")

    def handle_left(self):
        pass

    def handle_right(self):
        pass