from ..logger.darky_visual import STYLE, FG, BG
from ..utils.config_loader import Configuration

CONFIG = Configuration().get_config()

def printLogo():
    logo = [
        "  :::::::::::     :::       :::       :::::::::::       :::        :::::::::::       ::::::::       :::    :::   :::::::::::",
        "     :+:         :+:       :+:           :+:           :+:            :+:          :+:    :+:      :+:    :+:       :+:     ",
        "    +:+         +:+       +:+           +:+           +:+            +:+          +:+             +:+    +:+       +:+      ",
        "   +#+         +#+  +:+  +#+           +#+           +#+            +#+          :#:             +#++:++#++       +#+       ",
        "  +#+         +#+ +#+#+ +#+           +#+           +#+            +#+          +#+   +#+#      +#+    +#+       +#+        ",
        " #+#          #+#+# #+#+#            #+#           #+#            #+#          #+#    #+#      #+#    #+#       #+#         ",
        "###           ###   ###         ###########       ########## ###########       ########       ###    ###       ###          "
    ]
    print(f"{STYLE.GRADIENT(logo, ["#44F", "#D0F"])}")
    print(f"{FG.BLACK}{STYLE.GRADIENT(f"VERSION: {CONFIG.framework.version}{" "*85}developed by {CONFIG.framework.developer}", ["#44F", "#D4F"], "BG")}{STYLE.RESET}")