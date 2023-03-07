# from ui_MainWindow import Ui_Puzzlelists
import os
import sys
import constants as ct
from pathlib import Path

sys.path.insert(1, str(ct.PATH_ROOT_DIR / "games" / "tetris" ))
sys.path.insert(1, str(ct.PATH_ROOT_DIR / "games" / "snake" ))
sys.path.insert(1, str(ct.PATH_ROOT_DIR / "games" / "2048" ))
sys.path.insert(1, str(ct.PATH_ROOT_DIR / "games" / "space_wars" ))
sys.path.insert(1, str(ct.PATH_ROOT_DIR / "games" / "icy" ))


from tetris_main import TetrisApp
from icy_main import start_icy
from space_wars_main import start_space_wars
from snake_main import snake_game
from main_2048 import start_2048

if __name__ == "__main__":
    # game = snake_game()
    # game.run()
    # print(start_icy())
    pass