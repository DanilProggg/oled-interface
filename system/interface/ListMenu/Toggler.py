import json

from system.interface.ListMenu.ListMenuItem import ListMenuItem


class Toggler(ListMenuItem):
    def __init__(self, label, json_path, json_param):
        super().__init__(label)
        self.json_path = json_path
        self.json_param = json_param
        self.options = self.load_options()
        self.current_option = self._set_up_first_option()
    def _set_up_first_option(self):
        if self.options:
            return self.options[0]
        else:
            return None

    def load_options(self):
        with open(self.json_path, "r") as file:
            data = json.load(file)

            for i in data["options"]:
                if i == self.json_param:
                    return i["options"]
        return None


    def get_item_text(self) -> str:
        pass

    def handle_ok(self): pass

    def handle_left(self):
        pass

    def handle_right(self):
        pass
