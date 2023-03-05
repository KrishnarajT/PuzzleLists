from MainWindow import Ui_Puzzlelists
import os
import sys, time

import game_caller as gc
import constants as ct

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import QObject, Qt, QThread, QUrl, pyqtSlot
from PyQt6.QtWidgets import QFileDialog, QListWidget, QMainWindow
from PyQt6.QtCore import QObject, QThread, pyqtSignal

if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)

	window = Ui_Puzzlelists()

	with open(ct.STYLE_SHEET_PATH, "r") as f:
		_style = f.read()
		app.setStyleSheet(_style)

	window.show()

	window.change_Screen(1)

	# for i in range(5):
	#     window.change_Screen(i)
	#     time.sleep(1)
	app.exec()
