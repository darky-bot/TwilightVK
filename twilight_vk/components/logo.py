from art import text2art
from ..logger.darky_visual import STYLE, FG, BG

def printLogo():
    ansii_art = text2art("Twilight", font="alligator")
    print(f"{STYLE.GRADIENT(text2art("Twilight", font="alligator"), ["#44F", "#D4F"])}")
    print(f"{FG.BLACK}{STYLE.GRADIENT(f"VERSION: 0.0.1{" "*80}developed by darky_wings", ["#44F", "#D4F"], "BG")}{STYLE.RESET}")