from twilight_vk.logger.darky_logger import DarkyLogger
from twilight_vk.components.logo import LogoComponent
from twilight_vk.logger.darky_visual import FG, BG, STYLE, Visual
from tests.fixtures.logging import CONFIG

def test_color_modes(caplog):

    for colormode in [0, 1, 2, 3]:
        print()
        Visual.set_color_mode(colormode)
        logger = DarkyLogger("test", CONFIG, silent=True)
        logo = LogoComponent()
        print(f"This is non colored text")
        print(f"{FG.CUSTOM_COLOR("#F00")}This is red text{STYLE.RESET}")
        print(f"{FG.GRADIENT("This is a very long gradient text for testing colors in foreground and background in different color modes", ["#06F", "#F06"])}")
        print(f"{FG.GRADIENT("This is a very long gradient text for testing colors in foreground and background in different color modes", ["#F00", "#FF0", "#0F0", "#0FF", "#00F", "#F0F"])}")
        print()
        print(f"Background:")
        print(f"{BG.CUSTOM_COLOR("#F00")}This is red text{STYLE.RESET}")
        print(f"{BG.GRADIENT("This is a very long gradient text for testing colors in foreground and background in different color modes", ["#06F", "#F06"])}")
        print(f"{BG.GRADIENT("This is a very long gradient text for testing colors in foreground and background in different color modes", ["#F00", "#FF0", "#0F0", "#0FF", "#00F", "#F0F"])}")
        print(logo.colored)