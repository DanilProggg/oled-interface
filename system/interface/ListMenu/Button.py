from system.interface.ListMenu.ListMenuItem import ListMenuItem


class Button(ListMenuItem):
    def __init__(self, label, hop_context):
        super().__init__(label)
        self.hop_context = hop_context

    def get_item_text(self) -> str:
        return self.label

    def handle_ok(self, set_context):
        set_context(hop_context)

    def handle_left(self):
        pass

    def handle_right(self):
        pass