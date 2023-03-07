# this file contains the locations of the million things that are used in this project.

import os
from PyQt6 import QtCore, QtGui, QtWidgets
from pathlib import Path

# Basics
UI_WIDTH = 1280
UI_HEIGHT = 720

# Path related

# this is the puzzlelists directory
ROOT_DIR = str(Path(__file__).parent.parent)
PATH_ROOT_DIR = Path(__file__).parent.parent

STYLE_SHEET_PATH = os.path.join(ROOT_DIR, "src/stylesheet.qss")

# Adding directories to use in the stylesheet
QtCore.QDir.addSearchPath("images", os.path.join(ROOT_DIR, "resources/images"))
QtCore.QDir.addSearchPath("fonts", os.path.join(ROOT_DIR, "resources/fonts"))

# Game related
GAMES = ["space wars", "2048", "icy", "snake", "tetris"]
GAME_PRICES = {
    GAMES[0]: 400,
    GAMES[1]: 200,
    GAMES[2]: 100,
    GAMES[3]: 0,
    GAMES[4]: 0,
}

# Database related

# UI Related
ICON = os.path.join(ROOT_DIR, "resources/logo/icon.svg")
