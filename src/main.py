from ui_MainWindow import Ui_Puzzlelists
import os
import sys
# sys.path.insert(1, os.path.join(os.getcwd(), '../games/'))
# sys.path.insert(1, os.path.join(os.getcwd(), '../games/tetris/'))
sys.path.insert(1, '../PuzzleLists/games/tetris')

# from tetris import settings
# from tetris import main
from tetris_main import App

if __name__ == '__main__':
    # print("Welcome to the Puzzlelists!")
    # ui = Ui_Puzzlelists()
    # ui.setupUi()
    app = App()
    app.run()

    