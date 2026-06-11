import os
import logging
import sys
from functools import lru_cache

from ..utils.types.cli_colors import ColorTypes

logger = logging.getLogger(__name__)
logger.setLevel("DEBUG")

class ColorSupport:

    @classmethod
    def detect(cls):
        if os.getenv('NO_COLOR') or (os.getenv('CI') and not os.getenv('FORCE_COLOR')):
            return ColorTypes.NONE
        if not sys.stdout.isatty():
            return ColorTypes.NONE

        colorterm = os.getenv('COLORTERM')
        if colorterm in ('truecolor', '24bit'):
            return ColorTypes.TRUECOLOR

        term = os.getenv('TERM', '').lower()
        if '256color' in term:
            return ColorTypes.ANSI256

        if 'color' in term or os.getenv('COLORTERM'):
            return ColorTypes.ANSI16

        return ColorTypes.NONE

class VisualMeta(type):

    '''Automatic attribute formatting'''

    def __getattribute__(cls, name):
        attr = super().__getattribute__(name)
        
        if name in ("prefix", "mode", "_color_mode"):
            return attr
        
        if isinstance(attr, str) and attr.isdigit():
            if Visual._color_mode == ColorTypes.NONE:
                return ""
            return f"{cls.prefix}{attr}m"
        
        return attr

    def __getattr__(cls, name):
        logger.warning(f"Attribute '{name}' not found in '{cls.__name__}'")
        return f"<{cls.__name__}.{name}>"

class Visual(metaclass=VisualMeta):

    '''Styles for print functions and etc'''

    prefix = "\033["

    _color_mode = ColorSupport.detect()

    @classmethod
    def set_color_mode(cls, mode: int):
        '''
        Force set the color mode
        '''
        cls._color_mode = mode
    
    @staticmethod
    def ansi(silent:bool=False) -> None:
        '''Enabling ANSI support in Windows'''
        if os.name == "nt":
            os.system('')
            if not silent:
                logger.info(f"ANSI support initiated!")
        logger.debug(f"Color mode: {Visual._color_mode}")

    @staticmethod
    def hex_to_rgb(hex:str) -> tuple[int, int, int]:
        '''
        Converts HEX code to RGB

        :param hex: your hex code need to be converted to rgb code
        :type hex: str

        :returns: tuple of RGB integers (R, G, B)
        '''
        hex = hex.lstrip("#")

        if len(hex) not in (3, 6):
            raise ValueError(f"Invalid HEX code: #{hex}")
        
        if len(hex) == 3:
            hex = ''.join(c * 2 for c in hex)
            
        return tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))
    
    @staticmethod
    @lru_cache(maxsize=256)
    def _rgb_to_ansi256(r, g, b) -> int:
        '''
        Approximate color from RGB to 256-bit
        '''
        if r == g == b:
            if r < 8:
                return 16
            if r > 248:
                return 231
            return round(((r - 8) / 247) * 24) + 232
        return 16 + (36 * round(r / 51)) + (6 * round(g / 51)) + round(b / 51)
    
    @staticmethod
    def _custom_color(mode: str = "3", color: str = "#FFF") -> str:
        """
        Returns ANSI-code for custom color.

        :param mode: Foreground ("3") or Background mode ("4")
        :type mode: str

        :param color: HEX color
        :type color: str
        """
        if Visual._color_mode == ColorTypes.NONE:
            return ""

        r, g, b = Visual.hex_to_rgb(color)

        if Visual._color_mode == ColorTypes.TRUECOLOR:
            return f"{Visual.prefix}{mode}8;2;{r};{g};{b}m"

        if Visual._color_mode == ColorTypes.ANSI256:
            idx = Visual._rgb_to_ansi256(r, g, b)
            ansi_mode = "38" if mode == "3" else "48"
            return f"{Visual.prefix}{ansi_mode};5;{idx}m"

        if Visual._color_mode == ColorTypes.ANSI16:
            best = Visual._nearest_ansi16(r, g, b)
            if mode == "3":   # foreground
                if best < 8:
                    code = 30 + best
                else:
                    code = 90 + (best - 8)
            else:             # background
                if best < 8:
                    code = 40 + best
                else:
                    code = 100 + (best - 8)
            return f"{Visual.prefix}{code}m"

        return ""
    
    @staticmethod
    def _nearest_ansi16(r, g, b) -> int:
        '''
        Returns 0-15 index for nearest standart ANSI color
        '''
        ansi16__COLORS = [
            (0,0,0), (128,0,0), (0,128,0), (128,128,0),
            (0,0,128), (128,0,128), (0,128,128), (192,192,192),
            (128,128,128), (255,0,0), (0,255,0), (255,255,0),
            (0,0,255), (255,0,255), (0,255,255), (255,255,255)
        ]
        
        best = 0
        best_dist = float('inf')
        for i, (cr, cg, cb) in enumerate(ansi16__COLORS):
            d = (r-cr)**2 + (g-cg)**2 + (b-cb)**2
            if d < best_dist:
                best_dist = d
                best = i
        return best
    
    @staticmethod
    def _gradient(text: str | list[str], mode: str = "3", colors: list = ["#FFF"]) -> str:

        '''
        Returns the prepared gradient text
        
        :param text: - input text to gradient
        :type text: str

        :param mode: Foreground ("3") or Background mode ("4")
        :type mode: str

        :param colors: list of hex colors for gradient
        :type colors: list
        '''
        if Visual._color_mode == ColorTypes.NONE:
            return text if isinstance(text, str) else "\n".join(text)
        if len(colors) == 0:
            return text
        if len(colors) == 1:
            return f"{Visual._custom_color(mode, colors[0])}{text}{STYLE.RESET}"

        #   ANSI16
        if Visual._color_mode == ColorTypes.ANSI16:
            avg_r = avg_g = avg_b = 0
            for col in colors:
                r,g,b = Visual.hex_to_rgb(col)
                avg_r += r; avg_g += g; avg_b += b
            n = len(colors)
            avg_color = f"#{avg_r//n:02x}{avg_g//n:02x}{avg_b//n:02x}"
            if isinstance(text, list):
                lines = text
            elif isinstance(text, str) and '\n' in text:
                lines = text.split('\n')
            else:
                lines = [text]
            colored_lines = [f"{Visual._custom_color(mode, avg_color)}{line}{STYLE.RESET}" for line in lines]
            return '\n'.join(colored_lines)

        #   ANSI256 and TRUECOLOR
        if "\n" in text or isinstance(text, list):
            lines = text.split('\n') if isinstance(text, str) else text.copy()
            for i, line in enumerate(lines):
                lines[i] = Visual._gradient(line, mode, colors)
            return f"{'\n'.join(lines)}{STYLE.RESET}"

        rgb = [Visual.hex_to_rgb(c) for c in colors]
        total_len = len(text)
        num_segments = len(colors) - 1
        base_len = total_len // num_segments
        remainder = total_len % num_segments

        result = []
        pos = 0
        for i in range(num_segments):
            seg_len = base_len + (1 if i < remainder else 0)
            if seg_len == 0:
                continue
            sr, sg, sb = rgb[i]
            er, eg, eb = rgb[i+1]
            for step in range(seg_len):
                t = step / (seg_len - 1) if seg_len > 1 else 0
                r = int(sr + (er - sr) * t)
                g = int(sg + (eg - sg) * t)
                b = int(sb + (eb - sb) * t)
                hex_color = f"#{r:02x}{g:02x}{b:02x}"
                color_code = Visual._custom_color(mode, hex_color)
                result.append(f"{color_code}{text[pos]}")
                pos += 1
        return f"{''.join(result)}{STYLE.RESET}"


class _COLORS:
    BLACK = "0"
    RED = "1"
    GREEN = "2"
    YELLOW = "3"
    BLUE = "4"
    PURPLE = "5"
    CIAN = "6"
    WHITE = "7"

class STYLE(Visual):
    RESET = "0"
    BOLD = "1"
    DIM = "2"
    ITALIC = "3"
    UNDERLINE = "4"
    BLINK = "5"
    NEGATIVE = "7"
    INVISIBLE = "8"
    CROSS = "9"

class FG(STYLE):
    _mode = "3"
    BLACK = _mode + _COLORS.BLACK
    RED = _mode + _COLORS.RED
    GREEN = _mode + _COLORS.GREEN
    YELLOW = _mode + _COLORS.YELLOW
    BLUE = _mode + _COLORS.BLUE
    PURPLE = _mode + _COLORS.PURPLE
    CIAN = _mode + _COLORS.CIAN
    WHITE = _mode + _COLORS.WHITE

    @staticmethod
    def CUSTOM_COLOR(color:str="#FFFFFF") -> str:
        return Visual._custom_color("3", color)
    
    @staticmethod
    def GRADIENT(text:str|list[str], _COLORS:list=["#FFFFFF"]) -> str:
        return Visual._gradient(text, "3", _COLORS)

class BG(STYLE):
    _mode = "4"
    BLACK = _mode + _COLORS.BLACK
    RED = _mode + _COLORS.RED
    GREEN = _mode + _COLORS.GREEN
    YELLOW = _mode + _COLORS.YELLOW
    BLUE = _mode + _COLORS.BLUE
    PURPLE = _mode + _COLORS.PURPLE
    CIAN = _mode + _COLORS.CIAN
    WHITE = _mode + _COLORS.WHITE

    @staticmethod
    def CUSTOM_COLOR(color:str="#FFFFFF") -> str:
        return Visual._custom_color("4", color)
    
    @staticmethod
    def GRADIENT(text:str|list[str], _COLORS:list=["#FFFFFF"]) -> str:
        return Visual._gradient(text, "4", _COLORS)