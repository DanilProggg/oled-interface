from system.interface.ListMenu.ListMenuItem import ListMenuItem
import logging

logger = logging.getLogger("debug")


class Button(ListMenuItem):
    def __init__(self, label, hop_context=None):
        self.hop_context = hop_context
        super().__init__(label)

    def get_item_text(self) -> str:
        return self.label

    def handle_ok(self, switch_context):
        switch_context(self.hop_context)
        logger.debug("Обработано нажатие OK. Вызван callback switch_context")

    def handle_left(self):
        pass

    def handle_right(self):
        pass