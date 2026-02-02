from ..logger.darky_visual import STYLE, FG, BG

def make_it_colored(value, color: str = None, indent: int = 10):

    _color = FG.CUSTOM_COLOR("#555")
    _text = "None"

    if isinstance(value, str):
        _color = FG.CUSTOM_COLOR("#888")
        _text = value

    if isinstance(value, bool):
        if value:
            _color = FG.GREEN
            _text = "YES"
        else:
            _color = FG.RED
            _text = "NO"
    
    if color:
        _color = color
    
    return f"{_color}{_text:<{indent}}{STYLE.RESET}"