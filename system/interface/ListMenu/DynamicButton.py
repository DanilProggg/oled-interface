from system.interface.ListMenu.Button import Button
from system.interface.Keyboard.Keyboard import Keyboard
import yaml


class DynamicButton(Button):
    def __init__(self, label, get_value_callback, set_value_callback, path: list[str], hop_context=None):
        super().__init__(label, hop_context=hop_context)
        self._get_value = get_value_callback
        self._set_value = set_value_callback
        self.path = path
        self._cached_value = self._get_value(path)
        self.full_label = self._format_label(self._cached_value)
        
        
        # Передача колбэка в клавиатуру для сохранения изменений
        if self.hop_context and isinstance(self.hop_context, Keyboard):
            self.hop_context.set_on_change_callback(self.on_keyboard_change)

    def on_keyboard_change(self, new_value):
        self._cached_value = new_value
        self._set_value(self.path, new_value)
        self.full_label = self._format_label(self._cached_value)

    def _format_label(self, value):
        return f"{self.label}{value}"

    def get_item_text(self):
        return self.full_label
        
    def refresh(self):
        self._cached_value = self._get_value(path)

        