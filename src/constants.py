# this file contains the locations of the million things that are used in this project.

import os
from PyQt6 import QtCore

# Basics
UI_WIDTH = 1280
UI_HEIGHT = 720

# Path related
# this is the puzzlelists directory
ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))

QtCore.QDir.addSearchPath('images', os.path.join(ROOT_DIR, 'resources/images'))
STYLE_SHEET_PATH = os.path.join(ROOT_DIR, 'src/stylesheet.qss')

# Game related


# Database related


# UI Related

ICON = os.path.join(ROOT_DIR, "resources/logo/icon.svg")

# Stylesheets

background_qss = "background: url('/run/media/krishnaraj/Programs/Python/PuzzleLists/resources/images/login_bg_blur.jpg');\n"
'color:"#be3114"\n' ""
