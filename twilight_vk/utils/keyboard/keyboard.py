import logging

from .buttons.buttons import KeyboardButton

logger = logging.getLogger("keyboard")

class KeyboardMarkup:
    '''
    Клавиатура ВК
    '''
    def __init__(self,
                 one_time: bool = False,
                 inline: bool = False,
                 buttons: list[list[KeyboardButton]] = []):
        
        self._one_time: bool = None
        self._inline: bool = inline
        
        if not self._inline and one_time:
            self._one_time: bool = one_time

        self._buttons: list[list[KeyboardButton]] = buttons

        logger.debug("Generating keyboard markup...")

        self._buttons_markup: list[list[KeyboardButton]] = []

        for _line in self._buttons:
            self._buttons_markup.append([])
            for _button in _line:
                self._buttons_markup[-1].append(_button.getButton())

        self._keyboard_markup: dict = {
            "inline": self._inline,
            "buttons": self._buttons_markup
        }

        if not self._inline:
            self._keyboard_markup.setdefault("one_time", self._one_time)
        logger.debug(f"Keyboard markup was successfully generated: {self._keyboard_markup}")
    
    def getMarkup(self):
        '''
        Возвращает рамзетку клавиатуры
        '''
        return self._keyboard_markup