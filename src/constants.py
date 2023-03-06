# this file contains the locations of the million things that are used in this project.

import os
from PyQt6 import QtCore, QtGui, QtWidgets

# Basics
UI_WIDTH = 1280
UI_HEIGHT = 720

# Path related

# this is the puzzlelists directory
ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), ".."))
STYLE_SHEET_PATH = os.path.join(ROOT_DIR, "src/stylesheet.qss")

# Adding directories to use in the stylesheet
QtCore.QDir.addSearchPath("images", os.path.join(ROOT_DIR, "resources/images"))
QtCore.QDir.addSearchPath("fonts", os.path.join(ROOT_DIR, "resources/fonts"))

# Game related
GAMES = ["space wars", "2048", "icy", "snake", "tetris"]
GAME_PRICES = {
    GAMES[0]: 300,
    GAMES[1]: 200,
    GAMES[2]: 100,
    GAMES[3]: 0,
    GAMES[4]: 0,
}

# Fonts


# Database related


# UI Related

ICON = os.path.join(ROOT_DIR, "resources/logo/icon.svg")
