from ui_MainWindow import Ui_Puzzlelists
import os
import sys
sys.path.insert(1, os.path.join(os.getcwd(), '../games/'))

# from tetris import settings
from tetris import main

if __name__ == '__main__':
    # print("Welcome to the Puzzlelists!")
    # ui = Ui_Puzzlelists()
    # ui.setupUi()
    main()
