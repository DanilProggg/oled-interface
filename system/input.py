import pygame

class InputHandler:
    def __init__(self):
        # инициализация GPIO
        pass

    def get_action(self):
        return self._get_keyboard_action()

    def _get_keyboard_action(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                return {
                    pygame.K_UP: "UP",
                    pygame.K_DOWN: "DOWN",
                    pygame.K_RETURN: "LEFT",
                    pygame.K_ESCAPE: "RIGHT",
                    pygame.K_ENTER: "OK",
                    pygame.BACKSPACE: "BACK"
                }.get(event.key)
        return None



