# Main Window File
# Manages everything in the UI section, and the windows related to it as well as multithreading.

# Pyqt imports

import random
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import QObject, Qt, QThread, QUrl, pyqtSlot
from PyQt6.QtWidgets import QFileDialog, QListWidget, QMainWindow, QPushButton
from PyQt6.QtCore import QObject, QThread, pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QHeaderView,
)

# conventional imports
import sys
import time
import os

# Custom imports
import constants as ct
from send_mail import send_mail
from security import find_hash
from database_manager import database_manager
import game_caller as gc
import pygame as pg

class Ui_Puzzlelists(QMainWindow):
    def __init__(self):
        super().__init__()

        # Basic window setup
        self.setWindowTitle("Puzzlelists")
        self.setEnabled(True)
        self.setFixedSize(QtCore.QSize(ct.UI_WIDTH, ct.UI_HEIGHT))

        # declaring variables
        self.generated_otp = "000000"
        self.user_name = ""
        self.user_email = ""
        self.dbms = database_manager()
        self.dbms.connect_and_create_tables()
        self.current_game = None
        self.table = QTableWidget(10, 7)
        self.vBox = QVBoxLayout()
        self.vBox.addWidget(self.table)

        # calling functions
        self.makeFonts()
        self.setupUi()
        self.center()
        self.start_music()

    def start_music(self):
        pg.mixer.init()
        # BGM AND CLICK SOUNC EFFECT
        self.BGM = pg.mixer.music.load(
            os.path.join(ct.ROOT_DIR, "resources/audio", "RetroFuture-Clean.mp3")
        )
        pg.mixer.music.play(-1)

    def create_hgScore_table(self):
        self.table.setHorizontalHeaderLabels(
            ["Name", "Snake", "2048", "Tetris", "Space_wars", "Icy", "Total Score"]
        )
        self.table.setColumnWidth(0, 250)

        for i, row in enumerate(self.dbms.top_scores):
            for j, item in enumerate(row):
                item = QTableWidgetItem(str(item))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(i, j, item)

        self.table.setEditTriggers(
            QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers
        )
        self.table.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows
        )
        self.table.setSelectionMode(
            QtWidgets.QAbstractItemView.SelectionMode.SingleSelection
        )
        self.table.setShowGrid(False)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.ResizeMode.Stretch
        )
        self.table.horizontalHeader().setStyleSheet(
            "background: '#fea7ec'; color: '#1c0940';"
        )
        self.table.horizontalScrollBar().setEnabled(False)
        self.table.verticalScrollBar().setEnabled(False)
        self.table.verticalHeader().setEnabled(False)
        self.table.horizontalHeader().setFont(QFont(self.games_played_Font, 15))

        self.table.setFont(QFont(self.games_played_Font, 15))

    def center(self):
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def makeFonts(self):
        # Games Played Font
        id = QtGui.QFontDatabase.addApplicationFont(
            ct.ROOT_DIR + "/resources/fonts/GamePlayed-vYL7.ttf"
        )
        if id < 0:
            print("Font Error")
        self.games_played_Font = QtGui.QFontDatabase.applicationFontFamilies(id)[0]

        # Games played outline font
        id = QtGui.QFontDatabase.addApplicationFont(
            ct.ROOT_DIR + "/resources/fonts/GamePlayedOutline-wrX8.ttf"
        )
        if id < 0:
            print("Font Error")
        self.games_played_outline_Font = QtGui.QFontDatabase.applicationFontFamilies(
            id
        )[0]

        # Games font
        id = QtGui.QFontDatabase.addApplicationFont(
            ct.ROOT_DIR + "/resources/fonts/Games-XvD2.ttf"
        )
        if id < 0:
            print("Font Error")
        self.games_Font = QtGui.QFontDatabase.applicationFontFamilies(id)[0]

        # Squid Game font
        id = QtGui.QFontDatabase.addApplicationFont(
            ct.ROOT_DIR + "/resources/fonts/GameOfSquids-1GMVL.ttf"
        )
        if id < 0:
            print("Font Error")
        self.squid_game_Font = QtGui.QFontDatabase.applicationFontFamilies(id)[0]

    def update_button_lables(self):
        self.chgame_coins_lbl.setText(str(self.dbms.user_data.get("user_score")))
        games = self.dbms.user_data.get("user_games")
        print(str(ct.GAME_PRICES.get(ct.GAMES[0])))
        if ct.GAMES[0] in games:
            self.chgame_game1_btn.setText("PLAY")
        else:
            self.chgame_game1_btn.setText(str(ct.GAME_PRICES.get(ct.GAMES[0])))

        if ct.GAMES[1] in games:
            self.chgame_game2_btn.setText("PLAY")
        else:
            self.chgame_game2_btn.setText(str(ct.GAME_PRICES.get(ct.GAMES[1])))

        if ct.GAMES[2] in games:
            self.chgame_game3_btn.setText("PLAY")
        else:
            self.chgame_game3_btn.setText(str(ct.GAME_PRICES.get(ct.GAMES[2])))

    def change_screen(self, screen_number):
        """changes the stacked widget screen.

        Args:
                screen_number (int): which screen to go to
                0 Login Screen
                1. Signup Screen
                2. Forgot Password Screen
                3. Change Game Scren
                4. Highscore Screen
        """

        if screen_number == 0:
            self.login_remark_lbl.setText("Fill All Fields to Continue")
            self.login_forgotPass_btn.setEnabled(False)
            self.stackedWidget.setCurrentIndex(0)
        elif screen_number == 1:
            self.signup_remark_lbl.setText("Fill All Fields to Continue")
            self.stackedWidget.setCurrentIndex(1)
        elif screen_number == 2:
            self.fpass_remark_lbl.setText("Fill All Fields to Continue")
            self.stackedWidget.setCurrentIndex(2)
        elif screen_number == 3:
            # update the coins so we get the latest value before purchase.
            self.update_button_lables()
            self.chgame_name_lbl.setText(self.dbms.user_data.get("user_name"))
            self.chgame_coins_lbl.setText(str(self.dbms.user_data.get("user_score")))
            self.stackedWidget.setCurrentIndex(3)
        elif screen_number == 4:
            self.display_highscores()
            self.stackedWidget.setCurrentIndex(4)

    def verifyOtp(self):
        """Verifies the otp entered by the user."""

        print("verifying otp")
        print("generated otp: ", self.generated_otp)
        # self.change_Screen(screen_number=0)

        # if you are at the forgot password screen
        if self.stackedWidget.currentIndex() == 2:
            self.entered_otp = int(self.fpass_enterOtp_lineedit.text())
            if self.entered_otp == self.generated_otp:
                self.fpass_remark_lbl.setText("OTP Verified!")
                self.fpass_verifyOtp_btn.setEnabled(False)
                self.dbms.user_data["user_name"] = self.user_name
                self.dbms.user_data["user_email"] = self.user_email
                self.dbms.user_data["user_pass_hash"] = self.user_pass_hash
                if self.dbms.update_user_password():
                    self.fpass_remark_lbl.setText("Password Changed!")
                else:
                    self.fpass_remark_lbl.setText(
                        "Couldnt Change Password!, Try Troubleshooting"
                    )
                self.change_screen(screen_number=0)
            else:
                self.fpass_remark_lbl.setText("OTP is wrong! Try Again")
                self.fpass_verifyOtp_btn.setEnabled(True)

        # if you at the signup screen
        elif self.stackedWidget.currentIndex() == 1:
            self.entered_otp = int(self.signup_enterOtp_lineedit.text())
            if self.entered_otp == self.generated_otp:
                self.signup_remark_lbl.setText("OTP Verified!")
                self.signup_verifyOtp_btn.setEnabled(False)
                self.dbms.user_data["user_name"] = self.user_name
                self.dbms.user_data["user_email"] = self.user_email
                self.dbms.user_data["user_score"] = 0
                self.dbms.user_data["user_pass_hash"] = self.user_pass_hash
                print(
                    "created and inserted user_pass_hash: ",
                    self.dbms.user_data.get("user_pass_hash"),
                )
                if self.dbms.insert_user():
                    print("user inserted")
                    self.signup_remark_lbl.setText("User Appended to Our PuzzleList!!")
                self.change_screen(screen_number=0)
            else:
                self.signup_remark_lbl.setText("OTP is wrong! Try Again")
                self.signup_verifyOtp_btn.setEnabled(True)

    # this function will have to be multithreaded.
    def generateOtp_andSendMail(self):
        """generates the otp and sends it to the user."""

        # if you are at the forgot password screen
        if self.stackedWidget.currentIndex() == 2:
            self.user_name = self.fpass_enterName_lineedit.text()
            self.user_pass_hash = self.fpass_enterPass_lineedit.text()
            self.user_email = self.fpass_enterEmail_lineedit.text()
            if self.user_name == "" or self.user_pass_hash == "":
                self.fpass_remark_lbl.setText("Please fill all the fields!")
                return

            if len(self.user_name) > 10:
                self.fpass_remark_lbl.setText(
                    "Username cannot be more than 10 characters!"
                )
                return

            if len(self.user_pass_hash) < 8:
                self.fpass_remark_lbl.setText(
                    "Password must be atleast 8 characters long!"
                )
                return
            if self.user_pass_hash == self.user_name:
                self.fpass_remark_lbl.setText("Password cannot be same as username!")
                return
            if self.user_pass_hash.isalpha():
                self.fpass_remark_lbl.setText("Password must contain atleast 1 number!")
                return
            if self.user_pass_hash.isnumeric():
                self.fpass_remark_lbl.setText(
                    "Password must contain atleast 1 alphabet!"
                )
                return
            if self.user_pass_hash.isalnum():
                self.fpass_remark_lbl.setText(
                    "Password must contain atleast 1 special character!"
                )
                return
            if self.user_pass_hash.islower():
                self.fpass_remark_lbl.setText(
                    "Password must contain atleast 1 uppercase letter!"
                )
                return
            if self.user_pass_hash.isupper():
                self.fpass_remark_lbl.setText(
                    "Password must contain atleast 1 lowercase letter!"
                )
                return
            if self.user_pass_hash == "password":
                self.fpass_remark_lbl.setText("Password cannot be 'password'!")
                return
            if self.user_pass_hash == "12345678":
                self.fpass_remark_lbl.setText("Password cannot be '12345678'!")
                return

            # you cannot send another otp immediately.
            self.fpass_sendOtp_btn.setEnabled(False)

        # if you at the signup screen
        elif self.stackedWidget.currentIndex() == 1:
            self.user_name = self.signup_enterName_lineedit.text()
            self.user_pass_hash = self.signup_enterPass_lineedit.text()
            self.user_email = self.signup_enterEmail_lineedit.text()
            if self.user_name == "" or self.user_pass_hash == "":
                self.signup_remark_lbl.setText("Please fill all the fields!")
                return

            if len(self.user_name) > 10:
                self.fpass_remark_lbl.setText(
                    "Username cannot be more than 10 characters!"
                )
                return

            if len(self.user_pass_hash) < 8:
                self.signup_remark_lbl.setText(
                    "Password must be atleast 8 characters long!"
                )
                return
            if self.user_pass_hash == self.user_name:
                self.signup_remark_lbl.setText("Password cannot be same as username!")
                return
            if self.user_pass_hash.isalpha():
                self.signup_remark_lbl.setText(
                    "Password must contain atleast 1 number!"
                )
                return
            if self.user_pass_hash.isnumeric():
                self.signup_remark_lbl.setText(
                    "Password must contain atleast 1 alphabet!"
                )
                return
            if self.user_pass_hash.isalnum():
                self.signup_remark_lbl.setText(
                    "Password must contain atleast 1 special character!"
                )
                return
            if self.user_pass_hash.islower():
                self.signup_remark_lbl.setText(
                    "Password must contain atleast 1 uppercase letter!"
                )
                return
            if self.user_pass_hash.isupper():
                self.signup_remark_lbl.setText(
                    "Password must contain atleast 1 lowercase letter!"
                )
                return
            if self.user_pass_hash == "password":
                self.signup_remark_lbl.setText("Password cannot be 'password'!")
                return
            if self.user_pass_hash == "12345678":
                self.signup_remark_lbl.setText("Password cannot be '12345678'!")
                return

            # you cannot send another otp immediately.
            self.signup_sendOtp_btn.setEnabled(False)

        print("generating otp")
        self.generated_otp = random.randint(100000, 999999)
        print("generated otp: ", self.generated_otp)
        if send_mail(self.user_email, self.generated_otp):
            self.fpass_remark_lbl.setText("OTP sent to your email!")
            self.signup_remark_lbl.setText("OTP sent to your email!")
            self.signup_verifyOtp_btn.setEnabled(True)
            self.fpass_verifyOtp_btn.setEnabled(True)
        else:
            self.fpass_remark_lbl.setText("Incorrect Email!")
            self.signup_remark_lbl.setText("Incorrect Email!")

    # this function will have to be multithreaded.
    def verify_login(self):
        self.user_name = self.login_enterName_lineedit.text()
        self.user_pass_hash = self.login_enterPass_lineedit.text()
        print("password you just entered is is: ", self.user_pass_hash)
        self.dbms.user_data["user_name"] = self.user_name
        if self.dbms.get_user_data():
            print("user pass hash from teh screen: ", self.user_pass_hash)

            # salt the password and hash it
            salted_pass = self.user_pass_hash + self.dbms.user_data.get("user_salt")
            self.user_pass_hash = find_hash(salted_pass)

            print(
                "user pass hash from the database: ",
                self.dbms.user_data.get("user_pass_hash"),
            )
            if self.user_pass_hash == self.dbms.user_data.get("user_pass_hash"):
                self.login_remark_lbl.setText("Login Successful!")
                self.chgame_coins_lbl.setText(
                    str(self.dbms.user_data.get("user_score"))
                )
                self.change_screen(screen_number=3)
            else:
                self.login_remark_lbl.setText("Incorrect Password! Try Again or Reset")
                self.login_forgotPass_btn.setEnabled(True)
        else:
            self.login_remark_lbl.setText("User does not exist!")

    def change_games(self):
        """changes the game that is being played, and updates the new scores in the database."""

        print(self.current_game)
        self.change_screen(screen_number=3)
        if self.current_game == ct.GAMES[0]:
            pg.mixer.music.stop()
            self.setVisible(False)
            self.dbms.user_game_scores[self.current_game] += gc.start_space_wars()
            self.dbms.user_data["user_score"] += self.dbms.user_game_scores[
                self.current_game
            ]
            self.chgame_coins_lbl.setText(str(self.dbms.user_data["user_score"]))
            self.setVisible(True)
            self.start_music()
        elif self.current_game == ct.GAMES[1]:
            pg.mixer.music.stop()
            self.setVisible(False)
            self.dbms.user_game_scores[self.current_game] += gc.start_2048()
            self.dbms.user_data["user_score"] += self.dbms.user_game_scores[
                self.current_game
            ]
            self.chgame_coins_lbl.setText(str(self.dbms.user_data["user_score"]))
            self.setVisible(True)
            self.start_music()
        elif self.current_game == ct.GAMES[2]:
            pg.mixer.music.stop()
            self.setVisible(False)
            score = gc.start_icy()
            print(score)
            self.dbms.user_game_scores[self.current_game] += score
            print(self.dbms.user_game_scores[self.current_game])
            self.dbms.user_data["user_score"] += self.dbms.user_game_scores[
                self.current_game
            ]
            self.chgame_coins_lbl.setText(str(self.dbms.user_data["user_score"]))
            self.setVisible(True)
            self.start_music()
        elif self.current_game == ct.GAMES[3]:
            pg.mixer.music.stop()
            self.setVisible(False)
            game = gc.snake_game()
            self.dbms.user_game_scores[self.current_game] += game.run()
            self.dbms.user_data["user_score"] += self.dbms.user_game_scores[
                self.current_game
            ]
            self.chgame_coins_lbl.setText(str(self.dbms.user_data["user_score"]))
            self.setVisible(True)
            self.start_music()

        elif self.current_game == ct.GAMES[4]:
            pg.mixer.music.stop()
            self.setVisible(False)
            tetris = gc.TetrisApp()
            self.dbms.user_game_scores[self.current_game] += tetris.run()
            self.dbms.user_data["user_score"] += self.dbms.user_game_scores[
                self.current_game
            ]
            self.chgame_coins_lbl.setText(str(self.dbms.user_data["user_score"]))
            self.setVisible(True)
            self.start_music()

        # now that the game has been played at this point, and the scores are with us, we can update the database, so that if the user now wishes to see the highscores, he can see the updated scores.
        self.dbms.update_database()

    # this function will have to be multithreaded.
    def purchase_game(self, game):
        """Checkes if the user has enough coins to purchase the game, and if
        so, then launches that game after reducing the coins, and otherwise does nothing.
        Args:
            game (str): title of the game.
        """
        coins = self.dbms.user_data.get("user_score")

        if game not in self.dbms.user_data.get("user_games"):
            if coins >= ct.GAME_PRICES[game]:
                self.dbms.user_data["user_games"].append(game)
                self.dbms.user_data["user_score"] -= ct.GAME_PRICES[game]
                self.chgame_coins_lbl.setText(str(self.dbms.user_data["user_score"]))
                self.dbms.update_database()
                self.current_game = game
                self.change_games()
        else:
            self.current_game = game
            self.change_games()

    def display_highscores(self):
        """Displays the highscores of the current game on the column view."""
        # first get the highscores
        self.dbms.get_top_scores()
        self.create_hgScore_table()

    def setupUi(self):
        # setting icons
        icon = QtGui.QIcon()
        icon.addPixmap(
            QtGui.QPixmap(ct.ICON), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off
        )
        self.setWindowIcon(icon)

        self.centralwidget = QtWidgets.QWidget(parent=self)
        self.centralwidget.setObjectName("centralwidget")
        self.stackedWidget = QtWidgets.QStackedWidget(parent=self.centralwidget)
        self.stackedWidget.setGeometry(QtCore.QRect(0, 0, 1280, 720))
        self.stackedWidget.setAutoFillBackground(False)
        self.stackedWidget.setStyleSheet("")
        self.stackedWidget.setInputMethodHints(QtCore.Qt.InputMethodHint.ImhNone)
        self.stackedWidget.setObjectName("stackedWidget")

        ################### LOGIN PAGE ############################

        self.Login = QtWidgets.QWidget()
        self.Login.setObjectName("Login")

        self.login_newUser_btn = QtWidgets.QPushButton(parent=self.Login)
        self.login_newUser_btn.setGeometry(QtCore.QRect(630, 650, 350, 60))
        self.login_newUser_btn.setFont(
            QFont(self.games_played_Font, pointSize=20, weight=50)
        )
        self.login_newUser_btn.setAutoFillBackground(False)
        self.login_newUser_btn.setCheckable(False)
        self.login_newUser_btn.setFlat(True)
        self.login_newUser_btn.setObjectName("login_newUser_btn")
        self.login_newUser_btn.clicked.connect(lambda: self.change_screen(1))

        self.login_forgotPass_btn = QtWidgets.QPushButton(parent=self.Login)
        self.login_forgotPass_btn.setGeometry(QtCore.QRect(290, 650, 350, 60))
        self.login_forgotPass_btn.setFont(
            QFont(self.games_played_Font, pointSize=20, weight=50)
        )
        self.login_forgotPass_btn.setAutoFillBackground(False)
        self.login_forgotPass_btn.setCheckable(False)
        self.login_forgotPass_btn.setFlat(True)
        self.login_forgotPass_btn.setObjectName("login_forgotPass_btn")
        self.login_forgotPass_btn.clicked.connect(lambda: self.change_screen(2))

        self.login_enterPass_lineedit = QtWidgets.QLineEdit(parent=self.Login)
        self.login_enterPass_lineedit.setGeometry(QtCore.QRect(810, 370, 401, 61))
        self.login_enterPass_lineedit.setFont(
            QFont(self.games_played_Font, pointSize=25, weight=50)
        )

        self.login_enterPass_lineedit.setAutoFillBackground(False)
        self.login_enterPass_lineedit.setInputMask("")
        self.login_enterPass_lineedit.setFrame(False)
        self.login_enterPass_lineedit.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.login_enterPass_lineedit.setCursorPosition(0)
        self.login_enterPass_lineedit.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.login_enterPass_lineedit.setObjectName("login_enterPass_lineedit")

        self.login_enterName_lbl = QtWidgets.QLabel(parent=self.Login)
        self.login_enterName_lbl.setGeometry(QtCore.QRect(10, 310, 611, 31))
        self.login_enterName_lbl.setFont(
            QFont(self.games_played_Font, pointSize=20, weight=50)
        )
        self.login_enterName_lbl.setStyleSheet("background: None;\n" 'color: "#15063d"')
        self.login_enterName_lbl.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.login_enterName_lbl.setObjectName("login_enterName_lbl")

        self.login_enterPass_lbl = QtWidgets.QLabel(parent=self.Login)
        self.login_enterPass_lbl.setGeometry(QtCore.QRect(750, 300, 501, 51))
        self.login_enterPass_lbl.setFont(
            QFont(self.games_played_Font, pointSize=25, weight=50)
        )
        self.login_enterPass_lbl.setStyleSheet("background: None;\n" 'color: "#15063d"')
        self.login_enterPass_lbl.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.login_enterPass_lbl.setObjectName("login_enterPass_lbl")

        self.login_welcome_lbl = QtWidgets.QLabel(parent=self.Login)
        self.login_welcome_lbl.setGeometry(QtCore.QRect(190, 40, 901, 181))
        self.login_welcome_lbl.setFont(QFont(self.games_Font, pointSize=60, weight=50))
        self.login_welcome_lbl.setAutoFillBackground(False)
        self.login_welcome_lbl.setStyleSheet("background: None;\n" 'color: "#fea7ec"')
        self.login_welcome_lbl.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.login_welcome_lbl.setObjectName("login_welcome_lbl")

        self.login_Begin_btn = QtWidgets.QPushButton(parent=self.Login)
        self.login_Begin_btn.setGeometry(QtCore.QRect(400, 460, 511, 121))
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.login_Begin_btn.sizePolicy().hasHeightForWidth()
        )
        self.login_Begin_btn.setSizePolicy(sizePolicy)
        self.login_Begin_btn.setFont(QtGui.QFont(self.games_Font, 42))
        self.login_Begin_btn.setCursor(
            QtGui.QCursor(QtCore.Qt.CursorShape.OpenHandCursor)
        )
        self.login_Begin_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.login_Begin_btn.setAutoFillBackground(False)
        self.login_Begin_btn.setFlat(True)
        self.login_Begin_btn.setObjectName("login_Begin_btn")
        self.login_Begin_btn.clicked.connect(lambda: self.verify_login())

        self.login_enterName_lineedit = QtWidgets.QLineEdit(parent=self.Login)
        self.login_enterName_lineedit.setGeometry(QtCore.QRect(100, 370, 401, 61))
        self.login_enterName_lineedit.setFont(
            QFont(self.games_played_Font, pointSize=25, weight=50)
        )
        self.login_enterName_lineedit.setInputMask("")
        self.login_enterName_lineedit.setText("")
        self.login_enterName_lineedit.setFrame(False)
        self.login_enterName_lineedit.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)
        self.login_enterName_lineedit.setCursorPosition(0)
        self.login_enterName_lineedit.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.login_enterName_lineedit.setObjectName("login_enterName_lineedit")

        self.login_remark_lbl = QtWidgets.QLabel(parent=self.Login)
        self.login_remark_lbl.setObjectName("login_remark_lbl")
        self.login_remark_lbl.setGeometry(QtCore.QRect(300, 600, 711, 41))
        self.login_remark_lbl.setFont(
            QFont(self.games_played_Font, pointSize=22, weight=50)
        )
        self.login_remark_lbl.setStyleSheet("background: None;\n" "color: white;")
        self.login_remark_lbl.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        ###################### SIGNUP PAGE #########################

        self.stackedWidget.addWidget(self.Login)

        self.Signup = QtWidgets.QWidget()
        self.Signup.setObjectName("Signup")
        self.signup_sendOtp_btn = QtWidgets.QPushButton(parent=self.Signup)
        self.signup_sendOtp_btn.setGeometry(QtCore.QRect(290, 610, 350, 60))
        self.signup_sendOtp_btn.setFont(
            QFont(self.games_played_Font, pointSize=20, weight=50)
        )
        self.signup_sendOtp_btn.setAutoFillBackground(False)
        self.signup_sendOtp_btn.setCheckable(False)
        self.signup_sendOtp_btn.setFlat(True)
        self.signup_sendOtp_btn.setObjectName("signup_sendOtp_btn")
        self.signup_sendOtp_btn.clicked.connect(self.generateOtp_andSendMail)

        self.signup_verifyOtp_btn = QtWidgets.QPushButton(parent=self.Signup)
        self.signup_verifyOtp_btn.setGeometry(QtCore.QRect(660, 610, 350, 60))
        self.signup_verifyOtp_btn.setFont(
            QFont(self.games_played_Font, pointSize=20, weight=50)
        )
        self.signup_verifyOtp_btn.setAutoFillBackground(False)
        self.signup_verifyOtp_btn.setCheckable(False)
        self.signup_verifyOtp_btn.setFlat(True)
        self.signup_verifyOtp_btn.setObjectName("signup_verifyOtp_btn")
        self.signup_verifyOtp_btn.setEnabled(False)
        self.signup_verifyOtp_btn.clicked.connect(self.verifyOtp)

        self.signup_enterPass_lineedit = QtWidgets.QLineEdit(parent=self.Signup)
        self.signup_enterPass_lineedit.setGeometry(QtCore.QRect(800, 280, 401, 61))
        self.signup_enterPass_lineedit.setFont(
            QFont(self.games_played_Font, pointSize=22, weight=50)
        )
        self.signup_enterPass_lineedit.setAutoFillBackground(False)
        self.signup_enterPass_lineedit.setInputMask("")
        self.signup_enterPass_lineedit.setFrame(False)
        self.signup_enterPass_lineedit.setEchoMode(
            QtWidgets.QLineEdit.EchoMode.Password
        )
        self.signup_enterPass_lineedit.setCursorPosition(4)
        self.signup_enterPass_lineedit.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.signup_enterPass_lineedit.setObjectName("signup_enterPass_lineedit")
        self.signup_enterName_lbl = QtWidgets.QLabel(parent=self.Signup)
        self.signup_enterName_lbl.setGeometry(QtCore.QRect(30, 230, 651, 41))
        self.signup_enterName_lbl.setFont(
            QFont(self.games_played_Font, pointSize=25, weight=50)
        )
        self.signup_enterName_lbl.setStyleSheet("background: None;\n" "color: white;")
        self.signup_enterName_lbl.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.signup_enterName_lbl.setObjectName("signup_enterName_lbl")
        self.signup_enterName_lineedit = QtWidgets.QLineEdit(parent=self.Signup)
        self.signup_enterName_lineedit.setGeometry(QtCore.QRect(150, 290, 461, 51))
        self.signup_enterName_lineedit.setFont(
            QFont(self.games_played_Font, pointSize=22, weight=50)
        )
        self.signup_enterName_lineedit.setInputMask("")
        self.signup_enterName_lineedit.setFrame(False)
        self.signup_enterName_lineedit.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)
        self.signup_enterName_lineedit.setCursorPosition(8)
        self.signup_enterName_lineedit.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.signup_enterName_lineedit.setObjectName("signup_enterName_lineedit")
        self.signup_enterPass_lbl = QtWidgets.QLabel(parent=self.Signup)
        self.signup_enterPass_lbl.setGeometry(QtCore.QRect(760, 230, 501, 51))
        self.signup_enterPass_lbl.setFont(
            QFont(self.games_played_Font, pointSize=25, weight=50)
        )
        self.signup_enterPass_lbl.setStyleSheet(
            "background: None;\n" "color: white\n" ""
        )
        self.signup_enterPass_lbl.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.signup_enterPass_lbl.setObjectName("signup_enterPass_lbl")
        self.signup_welcome_lbl = QtWidgets.QLabel(parent=self.Signup)
        self.signup_welcome_lbl.setGeometry(QtCore.QRect(160, 0, 1001, 171))
        self.signup_welcome_lbl.setFont(QFont(self.games_Font, pointSize=45, weight=50))
        self.signup_welcome_lbl.setLayoutDirection(
            QtCore.Qt.LayoutDirection.LeftToRight
        )
        self.signup_welcome_lbl.setAutoFillBackground(False)
        self.signup_welcome_lbl.setStyleSheet("background: None;\n" 'color: "#fea7ec"')
        self.signup_welcome_lbl.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.signup_welcome_lbl.setWordWrap(True)
        self.signup_welcome_lbl.setObjectName("signup_welcome_lbl")
        self.signup_enterEmail_lbl = QtWidgets.QLabel(parent=self.Signup)
        self.signup_enterEmail_lbl.setGeometry(QtCore.QRect(110, 370, 521, 61))
        self.signup_enterEmail_lbl.setFont(
            QFont(self.games_played_Font, pointSize=25, weight=50)
        )
        self.signup_enterEmail_lbl.setStyleSheet("background: None;\n" "color: white")
        self.signup_enterEmail_lbl.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.signup_enterEmail_lbl.setObjectName("signup_enterEmail_lbl")
        self.signup_enterEmail_lineedit = QtWidgets.QLineEdit(parent=self.Signup)
        self.signup_enterEmail_lineedit.setGeometry(QtCore.QRect(30, 450, 701, 41))
        self.signup_enterEmail_lineedit.setFont(
            QFont(self.games_played_Font, pointSize=22, weight=50)
        )
        self.signup_enterEmail_lineedit.setInputMask("")
        self.signup_enterEmail_lineedit.setFrame(False)
        self.signup_enterEmail_lineedit.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)
        self.signup_enterEmail_lineedit.setCursorPosition(23)
        self.signup_enterEmail_lineedit.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignCenter
        )
        self.signup_enterEmail_lineedit.setObjectName("signup_enterEmail_lineedit")
        self.signup_enterOtp_lineedit = QtWidgets.QLineEdit(parent=self.Signup)
        self.signup_enterOtp_lineedit.setGeometry(QtCore.QRect(830, 430, 351, 71))
        self.signup_enterOtp_lineedit.setFont(
            QFont(self.games_played_Font, pointSize=22, weight=50)
        )
        self.signup_enterOtp_lineedit.setInputMask("")
        self.signup_enterOtp_lineedit.setFrame(False)
        self.signup_enterOtp_lineedit.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)
        self.signup_enterOtp_lineedit.setCursorPosition(3)
        self.signup_enterOtp_lineedit.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.signup_enterOtp_lineedit.setObjectName("signup_enterOtp_lineedit")
        self.signup_enterOtp_lbl = QtWidgets.QLabel(parent=self.Signup)
        self.signup_enterOtp_lbl.setGeometry(QtCore.QRect(750, 370, 501, 51))
        self.signup_enterOtp_lbl.setFont(
            QFont(self.games_played_Font, pointSize=25, weight=50)
        )
        self.signup_enterOtp_lbl.setStyleSheet("background: None;\n" "color: white;")
        self.signup_enterOtp_lbl.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.signup_enterOtp_lbl.setObjectName("signup_enterOtp_lbl")
        self.signup_remark_lbl = QtWidgets.QLabel(parent=self.Signup)
        self.signup_remark_lbl.setGeometry(QtCore.QRect(310, 560, 711, 41))
        self.signup_remark_lbl.setFont(
            QFont(self.games_played_Font, pointSize=22, weight=50)
        )
        self.signup_remark_lbl.setStyleSheet("background: None;\n" "color: white;")
        self.signup_remark_lbl.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.signup_remark_lbl.setObjectName("signup_remark_lbl")

        ########################### Forgot Password Page ###################

        self.stackedWidget.addWidget(self.Signup)
        self.ForgotPass = QtWidgets.QWidget()
        self.ForgotPass.setObjectName("ForgotPass")
        self.fpass_enterName_lbl = QtWidgets.QLabel(parent=self.ForgotPass)
        self.fpass_enterName_lbl.setGeometry(QtCore.QRect(30, 230, 651, 41))
        self.fpass_enterName_lbl.setFont(
            QFont(self.games_played_Font, pointSize=25, weight=50)
        )
        self.fpass_enterName_lbl.setStyleSheet("background: None;\n" "color: white;")
        self.fpass_enterName_lbl.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.fpass_enterName_lbl.setObjectName("fpass_enterName_lbl")
        self.fpass_enterEmail_lineedit = QtWidgets.QLineEdit(parent=self.ForgotPass)
        self.fpass_enterEmail_lineedit.setGeometry(QtCore.QRect(30, 450, 701, 41))
        self.fpass_enterEmail_lineedit.setFont(
            QFont(self.games_played_Font, pointSize=22, weight=50)
        )
        self.fpass_enterEmail_lineedit.setInputMask("")
        self.fpass_enterEmail_lineedit.setFrame(False)
        self.fpass_enterEmail_lineedit.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)
        self.fpass_enterEmail_lineedit.setCursorPosition(23)
        self.fpass_enterEmail_lineedit.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.fpass_enterEmail_lineedit.setObjectName("fpass_enterEmail_lineedit")
        self.fpass_enterPass_lineedit = QtWidgets.QLineEdit(parent=self.ForgotPass)
        self.fpass_enterPass_lineedit.setGeometry(QtCore.QRect(800, 280, 401, 61))
        self.fpass_enterPass_lineedit.setFont(
            QFont(self.games_played_Font, pointSize=22, weight=50)
        )
        self.fpass_enterPass_lineedit.setAutoFillBackground(False)
        self.fpass_enterPass_lineedit.setInputMask("")
        self.fpass_enterPass_lineedit.setFrame(False)
        self.fpass_enterPass_lineedit.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.fpass_enterPass_lineedit.setCursorPosition(4)
        self.fpass_enterPass_lineedit.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.fpass_enterPass_lineedit.setObjectName("fpass_enterPass_lineedit")
        self.fpass_welcome_lbl = QtWidgets.QLabel(parent=self.ForgotPass)
        self.fpass_welcome_lbl.setGeometry(QtCore.QRect(160, 0, 1001, 171))
        self.fpass_welcome_lbl.setFont(QFont(self.games_Font, pointSize=45, weight=50))
        self.fpass_welcome_lbl.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.fpass_welcome_lbl.setAutoFillBackground(False)
        self.fpass_welcome_lbl.setStyleSheet("background: None;\n" 'color: "#fea7ec"')
        self.fpass_welcome_lbl.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.fpass_welcome_lbl.setWordWrap(True)
        self.fpass_welcome_lbl.setObjectName("fpass_welcome_lbl")
        self.fpass_enterEmail_lbl = QtWidgets.QLabel(parent=self.ForgotPass)
        self.fpass_enterEmail_lbl.setGeometry(QtCore.QRect(110, 370, 521, 61))
        self.fpass_enterEmail_lbl.setFont(
            QFont(self.games_played_Font, pointSize=25, weight=50)
        )
        self.fpass_enterEmail_lbl.setStyleSheet("background: None;\n" "color: white")
        self.fpass_enterEmail_lbl.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.fpass_enterEmail_lbl.setObjectName("fpass_enterEmail_lbl")
        self.fpass_enterOtp_lineedit = QtWidgets.QLineEdit(parent=self.ForgotPass)
        self.fpass_enterOtp_lineedit.setGeometry(QtCore.QRect(830, 430, 351, 71))
        self.fpass_enterOtp_lineedit.setFont(
            QFont(self.games_played_Font, pointSize=22, weight=50)
        )
        self.fpass_enterOtp_lineedit.setInputMask("")
        self.fpass_enterOtp_lineedit.setFrame(False)
        self.fpass_enterOtp_lineedit.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)
        self.fpass_enterOtp_lineedit.setCursorPosition(3)
        self.fpass_enterOtp_lineedit.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.fpass_enterOtp_lineedit.setObjectName("fpass_enterOtp_lineedit")
        self.fpass_enterPass_lbl = QtWidgets.QLabel(parent=self.ForgotPass)
        self.fpass_enterPass_lbl.setGeometry(QtCore.QRect(760, 230, 501, 51))
        self.fpass_enterPass_lbl.setFont(
            QFont(self.games_played_Font, pointSize=25, weight=50)
        )
        self.fpass_enterPass_lbl.setStyleSheet(
            "background: None;\n" "color: white\n" ""
        )
        self.fpass_enterPass_lbl.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.fpass_enterPass_lbl.setObjectName("fpass_enterPass_lbl")
        self.fpass_enterName_lineedit = QtWidgets.QLineEdit(parent=self.ForgotPass)
        self.fpass_enterName_lineedit.setGeometry(QtCore.QRect(150, 290, 461, 51))
        self.fpass_enterName_lineedit.setFont(
            QFont(self.games_played_Font, pointSize=22, weight=50)
        )
        self.fpass_enterName_lineedit.setInputMask("")
        self.fpass_enterName_lineedit.setFrame(False)
        self.fpass_enterName_lineedit.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)
        self.fpass_enterName_lineedit.setCursorPosition(8)
        self.fpass_enterName_lineedit.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.fpass_enterName_lineedit.setObjectName("fpass_enterName_lineedit")
        self.fpass_enterOtp_lbl = QtWidgets.QLabel(parent=self.ForgotPass)
        self.fpass_enterOtp_lbl.setGeometry(QtCore.QRect(750, 370, 501, 51))
        self.fpass_enterOtp_lbl.setFont(
            QFont(self.games_played_Font, pointSize=25, weight=50)
        )
        self.fpass_enterOtp_lbl.setStyleSheet("background: None;\n" "color: white;")
        self.fpass_enterOtp_lbl.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.fpass_enterOtp_lbl.setObjectName("fpass_enterOtp_lbl")
        self.fpass_sendOtp_btn = QtWidgets.QPushButton(parent=self.ForgotPass)
        self.fpass_sendOtp_btn.setGeometry(QtCore.QRect(290, 610, 350, 60))
        self.fpass_sendOtp_btn.setFont(
            QFont(self.games_played_Font, pointSize=20, weight=50)
        )
        self.fpass_sendOtp_btn.setAutoFillBackground(False)
        self.fpass_sendOtp_btn.setCheckable(False)
        self.fpass_sendOtp_btn.setFlat(True)
        self.fpass_sendOtp_btn.setObjectName("fpass_sendOtp_btn")
        self.fpass_sendOtp_btn.clicked.connect(self.generateOtp_andSendMail)

        self.fpass_verifyOtp_btn = QtWidgets.QPushButton(parent=self.ForgotPass)
        self.fpass_verifyOtp_btn.setGeometry(QtCore.QRect(660, 610, 350, 60))
        self.fpass_verifyOtp_btn.setFont(
            QFont(self.games_played_Font, pointSize=20, weight=50)
        )
        self.fpass_verifyOtp_btn.setAutoFillBackground(False)
        self.fpass_verifyOtp_btn.setCheckable(False)
        self.fpass_verifyOtp_btn.setFlat(True)
        self.fpass_verifyOtp_btn.setObjectName("fpass_verifyOtp_btn")
        self.fpass_verifyOtp_btn.clicked.connect(self.verifyOtp)
        self.fpass_verifyOtp_btn.setEnabled(False)

        self.fpass_remark_lbl = QtWidgets.QLabel(parent=self.ForgotPass)
        self.fpass_remark_lbl.setGeometry(QtCore.QRect(310, 560, 711, 41))
        self.fpass_remark_lbl.setFont(
            QFont(self.games_played_Font, pointSize=22, weight=50)
        )
        self.fpass_remark_lbl.setStyleSheet("background: None;\n" "color: white;")
        self.fpass_remark_lbl.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.fpass_remark_lbl.setObjectName("fpass_remark_lbl")

        ########################## Choose Game Page ############################

        self.stackedWidget.addWidget(self.ForgotPass)
        self.ChooseGame = QtWidgets.QWidget()
        self.ChooseGame.setFont(QFont(self.games_played_Font, pointSize=25, weight=50))
        self.ChooseGame.setObjectName("ChooseGame")
        self.chgame_game1_lbl = QtWidgets.QLabel(parent=self.ChooseGame)
        self.chgame_game1_lbl.setGeometry(QtCore.QRect(210, 240, 631, 61))
        self.chgame_game1_lbl.setFont(QFont(self.games_Font, pointSize=55, weight=50))
        self.chgame_game1_lbl.setStyleSheet("background: None;\n" "color: white;")
        self.chgame_game1_lbl.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeading
            | QtCore.Qt.AlignmentFlag.AlignLeft
            | QtCore.Qt.AlignmentFlag.AlignVCenter
        )
        self.chgame_game1_lbl.setObjectName("chgame_game1_lbl")
        self.chgame_welcome_lbl = QtWidgets.QLabel(parent=self.ChooseGame)
        self.chgame_welcome_lbl.setGeometry(QtCore.QRect(140, 110, 1021, 91))
        self.chgame_welcome_lbl.setFont(QFont(self.games_Font, pointSize=75, weight=50))
        self.chgame_welcome_lbl.setAutoFillBackground(False)
        self.chgame_welcome_lbl.setStyleSheet("background: None;\n" 'color: "#fea7ec"')
        self.chgame_welcome_lbl.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.chgame_welcome_lbl.setObjectName("chgame_welcome_lbl")
        self.chgame_game2_lbl = QtWidgets.QLabel(parent=self.ChooseGame)
        self.chgame_game2_lbl.setGeometry(QtCore.QRect(210, 320, 631, 61))
        self.chgame_game2_lbl.setFont(QFont(self.games_Font, pointSize=55, weight=50))
        self.chgame_game2_lbl.setStyleSheet("background: None;\n" "color: white;")
        self.chgame_game2_lbl.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeading
            | QtCore.Qt.AlignmentFlag.AlignLeft
            | QtCore.Qt.AlignmentFlag.AlignVCenter
        )
        self.chgame_game2_lbl.setObjectName("chgame_game2_lbl")
        self.chgame_game3_lbl = QtWidgets.QLabel(parent=self.ChooseGame)
        self.chgame_game3_lbl.setGeometry(QtCore.QRect(210, 400, 631, 61))
        self.chgame_game3_lbl.setFont(QFont(self.games_Font, pointSize=55, weight=50))
        self.chgame_game3_lbl.setStyleSheet("background: None;\n" "color: white;")
        self.chgame_game3_lbl.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeading
            | QtCore.Qt.AlignmentFlag.AlignLeft
            | QtCore.Qt.AlignmentFlag.AlignVCenter
        )
        self.chgame_game3_lbl.setObjectName("chgame_game3_lbl")
        self.chgame_game4_lbl = QtWidgets.QLabel(parent=self.ChooseGame)
        self.chgame_game4_lbl.setGeometry(QtCore.QRect(210, 490, 631, 61))
        self.chgame_game4_lbl.setFont(QFont(self.games_Font, pointSize=55, weight=50))
        self.chgame_game4_lbl.setStyleSheet("background: None;\n" "color: white;")
        self.chgame_game4_lbl.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeading
            | QtCore.Qt.AlignmentFlag.AlignLeft
            | QtCore.Qt.AlignmentFlag.AlignVCenter
        )
        self.chgame_game4_lbl.setObjectName("chgame_game4_lbl")
        self.chgame_game5_lbl = QtWidgets.QLabel(parent=self.ChooseGame)
        self.chgame_game5_lbl.setGeometry(QtCore.QRect(210, 580, 631, 61))
        self.chgame_game5_lbl.setFont(QFont(self.games_Font, pointSize=55, weight=50))
        self.chgame_game5_lbl.setStyleSheet("background: None;\n" "color: white;")
        self.chgame_game5_lbl.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeading
            | QtCore.Qt.AlignmentFlag.AlignLeft
            | QtCore.Qt.AlignmentFlag.AlignVCenter
        )
        self.chgame_game5_lbl.setObjectName("chgame_game5_lbl")
        self.chgame_name_lbl = QtWidgets.QLabel(parent=self.ChooseGame)
        self.chgame_name_lbl.setGeometry(QtCore.QRect(1010, 20, 251, 31))
        self.chgame_name_lbl.setFont(
            QFont(self.games_played_Font, pointSize=25, weight=50)
        )
        self.chgame_name_lbl.setStyleSheet("background: None;\n" 'color: "#fea7ec"')
        self.chgame_name_lbl.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignRight
            | QtCore.Qt.AlignmentFlag.AlignTrailing
            | QtCore.Qt.AlignmentFlag.AlignVCenter
        )
        self.chgame_name_lbl.setObjectName("chgame_name_lbl")
        self.chgame_coins_lbl = QtWidgets.QLabel(parent=self.ChooseGame)
        self.chgame_coins_lbl.setGeometry(QtCore.QRect(480, 20, 381, 31))
        self.chgame_coins_lbl.setFont(
            QFont(self.games_played_Font, pointSize=25, weight=50)
        )
        self.chgame_coins_lbl.setStyleSheet("background: None;\n" 'color: "#fea7ec"')
        self.chgame_coins_lbl.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.chgame_coins_lbl.setObjectName("chgame_coins_lbl")
        self.chgame_game1_btn = QtWidgets.QPushButton(parent=self.ChooseGame)
        self.chgame_game1_btn.setGeometry(QtCore.QRect(919, 250, 191, 71))
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.chgame_game1_btn.sizePolicy().hasHeightForWidth()
        )
        self.chgame_game1_btn.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        self.chgame_game1_btn.setFont(
            QFont(self.squid_game_Font, pointSize=30, weight=50)
        )
        self.chgame_game1_btn.setCursor(
            QtGui.QCursor(QtCore.Qt.CursorShape.OpenHandCursor)
        )
        self.chgame_game1_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.chgame_game1_btn.setAutoFillBackground(False)
        self.chgame_game1_btn.setStyleSheet(
            'color: "#fea7ec";\n' "border-radius: 30;\n" ""
        )
        self.chgame_game1_btn.setDefault(False)
        self.chgame_game1_btn.setFlat(True)
        self.chgame_game1_btn.setObjectName("chgame_game1_btn")
        self.chgame_game1_btn.clicked.connect(lambda: self.purchase_game(ct.GAMES[0]))

        self.chgame_game2_btn = QtWidgets.QPushButton(parent=self.ChooseGame)
        self.chgame_game2_btn.setGeometry(QtCore.QRect(920, 330, 191, 71))
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.chgame_game2_btn.sizePolicy().hasHeightForWidth()
        )
        self.chgame_game2_btn.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        self.chgame_game2_btn.setFont(
            QFont(self.squid_game_Font, pointSize=30, weight=50)
        )
        self.chgame_game2_btn.setCursor(
            QtGui.QCursor(QtCore.Qt.CursorShape.OpenHandCursor)
        )
        self.chgame_game2_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.chgame_game2_btn.setAutoFillBackground(False)
        self.chgame_game2_btn.setStyleSheet(
            'color: "#fea7ec";\n' "border-radius: 30;\n"
        )
        self.chgame_game2_btn.setFlat(True)
        self.chgame_game2_btn.setObjectName("chgame_game2_btn")
        self.chgame_game2_btn.clicked.connect(lambda: self.purchase_game(ct.GAMES[1]))

        self.chgame_game3_btn = QtWidgets.QPushButton(parent=self.ChooseGame)
        self.chgame_game3_btn.setGeometry(QtCore.QRect(920, 410, 191, 71))
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.chgame_game3_btn.sizePolicy().hasHeightForWidth()
        )
        self.chgame_game3_btn.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        self.chgame_game3_btn.setFont(
            QFont(self.squid_game_Font, pointSize=30, weight=50)
        )
        self.chgame_game3_btn.setCursor(
            QtGui.QCursor(QtCore.Qt.CursorShape.OpenHandCursor)
        )
        self.chgame_game3_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.chgame_game3_btn.setAutoFillBackground(False)
        self.chgame_game3_btn.setStyleSheet(
            'color: "#fea7ec";\n' "border-radius: 30;\n"
        )
        self.chgame_game3_btn.setFlat(True)
        self.chgame_game3_btn.setObjectName("chgame_game3_btn")
        self.chgame_game3_btn.clicked.connect(lambda: self.purchase_game(ct.GAMES[2]))

        self.chgame_game4_btn = QtWidgets.QPushButton(parent=self.ChooseGame)
        self.chgame_game4_btn.setGeometry(QtCore.QRect(920, 490, 191, 71))
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.chgame_game4_btn.sizePolicy().hasHeightForWidth()
        )
        self.chgame_game4_btn.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        self.chgame_game4_btn.setFont(
            QFont(self.squid_game_Font, pointSize=30, weight=50)
        )
        self.chgame_game4_btn.setCursor(
            QtGui.QCursor(QtCore.Qt.CursorShape.OpenHandCursor)
        )
        self.chgame_game4_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.chgame_game4_btn.setAutoFillBackground(False)
        self.chgame_game4_btn.setStyleSheet(
            'color: "#fea7ec";\n' "border-radius: 30;\n"
        )
        self.chgame_game4_btn.setFlat(True)
        self.chgame_game4_btn.setObjectName("chgame_game4_btn")
        self.chgame_game4_btn.clicked.connect(lambda: self.purchase_game(ct.GAMES[3]))

        self.chgame_game5_btn = QtWidgets.QPushButton(parent=self.ChooseGame)
        self.chgame_game5_btn.setGeometry(QtCore.QRect(920, 570, 191, 71))
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.chgame_game5_btn.sizePolicy().hasHeightForWidth()
        )
        self.chgame_game5_btn.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        self.chgame_game5_btn.setFont(
            QFont(self.squid_game_Font, pointSize=30, weight=50)
        )
        self.chgame_game5_btn.setCursor(
            QtGui.QCursor(QtCore.Qt.CursorShape.OpenHandCursor)
        )
        self.chgame_game5_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.chgame_game5_btn.setAutoFillBackground(False)
        self.chgame_game5_btn.setStyleSheet(
            'color: "#fea7ec";\n' "border-radius: 30;\n"
        )
        self.chgame_game5_btn.setFlat(True)
        self.chgame_game5_btn.setObjectName("chgame_game5_btn")
        self.chgame_game5_btn.clicked.connect(lambda: self.purchase_game(ct.GAMES[4]))

        self.chgame_viewScore_btn = QtWidgets.QPushButton(parent=self.ChooseGame)
        self.chgame_viewScore_btn.setGeometry(QtCore.QRect(10, 10, 331, 51))
        self.chgame_viewScore_btn.setFont(
            QFont(self.games_played_Font, pointSize=20, weight=50)
        )
        self.chgame_viewScore_btn.setAutoFillBackground(False)
        self.chgame_viewScore_btn.setCheckable(False)
        self.chgame_viewScore_btn.setFlat(True)
        self.chgame_viewScore_btn.setObjectName("chgame_viewScore_btn")
        self.chgame_viewScore_btn.clicked.connect(lambda: self.change_screen(4))

        ############################## Highscore Page ###################

        self.stackedWidget.addWidget(self.ChooseGame)
        self.HighScores = QtWidgets.QWidget()
        self.HighScores.setObjectName("HighScores")
        self.hgscore_welcome_lbl = QtWidgets.QLabel(parent=self.HighScores)
        self.hgscore_welcome_lbl.setGeometry(QtCore.QRect(160, 50, 1021, 91))
        self.hgscore_welcome_lbl.setFont(
            QFont(self.games_Font, pointSize=75, weight=50)
        )
        self.hgscore_welcome_lbl.setAutoFillBackground(False)
        self.hgscore_welcome_lbl.setStyleSheet("background: None;\n" 'color: "#fea7ec"')
        self.hgscore_welcome_lbl.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.hgscore_welcome_lbl.setObjectName("hgscore_welcome_lbl")
        self.hgscore_backToGame_btn = QtWidgets.QPushButton(parent=self.HighScores)
        self.hgscore_backToGame_btn.setGeometry(QtCore.QRect(470, 640, 391, 51))
        self.hgscore_backToGame_btn.setFont(
            QFont(self.games_played_Font, pointSize=20, weight=50)
        )
        self.hgscore_backToGame_btn.setAutoFillBackground(False)
        self.hgscore_backToGame_btn.setCheckable(False)
        self.hgscore_backToGame_btn.setFlat(True)
        self.hgscore_backToGame_btn.setObjectName("hgscore_backToGame_btn")
        self.hgscore_backToGame_btn.clicked.connect(lambda: self.change_screen(3))

        self.hgscore_score_tblView = QtWidgets.QTableView(parent=self.HighScores)
        self.hgscore_score_tblView.setGeometry(QtCore.QRect(70, 170, 1141, 441))
        self.hgscore_score_tblView.setFont(
            QFont(self.games_played_Font, pointSize=25, weight=50)
        )

        self.hgscore_score_tblView.setObjectName("hgscore_score_colview")
        self.hgscore_score_tblView.setLayout(self.vBox)

        self.stackedWidget.addWidget(self.HighScores)
        self.setCentralWidget(self.centralwidget)

        self.retranslateUi()
        self.stackedWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Puzzlelists", "Puzzlelists"))
        self.login_remark_lbl.setText(
            _translate("Puzzlelists", "Fill Details and Press Begin!")
        )
        self.login_newUser_btn.setText(_translate("Puzzlelists", "New User? Join Us!"))
        self.login_forgotPass_btn.setText(_translate("Puzzlelists", "Forgot Password?"))
        self.login_enterName_lbl.setText(
            _translate("Puzzlelists", "Enter your Puzzler Name")
        )
        self.login_enterPass_lbl.setText(
            _translate("Puzzlelists", "Enter your Password")
        )
        self.login_welcome_lbl.setText(
            _translate("Puzzlelists", "Welcome to the \n" "PuzzleLists")
        )
        self.login_Begin_btn.setText(_translate("Puzzlelists", "Begin Journey!"))
        self.signup_sendOtp_btn.setText(_translate("Puzzlelists", "Send OTP!"))
        self.signup_verifyOtp_btn.setText(_translate("Puzzlelists", "Verify OTP!"))
        self.signup_enterPass_lineedit.setText(_translate("Puzzlelists", ""))
        self.signup_enterName_lbl.setText(
            _translate("Puzzlelists", "What would you like to be called?")
        )
        self.signup_enterName_lineedit.setText(_translate("Puzzlelists", ""))
        self.signup_enterPass_lbl.setText(
            _translate("Puzzlelists", "Enter your Password")
        )
        self.signup_welcome_lbl.setText(
            _translate("Puzzlelists", "We are glad to Append you to our Puzzler List!")
        )
        self.signup_enterEmail_lbl.setText(
            _translate("Puzzlelists", "Enter your Email ID")
        )
        self.signup_enterEmail_lineedit.setText(_translate("Puzzlelists", ""))
        self.signup_enterOtp_lineedit.setText(_translate("Puzzlelists", ""))
        self.signup_enterOtp_lbl.setText(_translate("Puzzlelists", "Enter OTP"))
        self.signup_remark_lbl.setText(
            _translate("Puzzlelists", "An OTP Will be sent to your Email Account")
        )
        self.fpass_enterName_lbl.setText(
            _translate("Puzzlelists", "Enter your Puzzler Name")
        )
        self.fpass_enterEmail_lineedit.setText(_translate("Puzzlelists", ""))
        self.fpass_enterPass_lineedit.setText(_translate("Puzzlelists", ""))
        self.fpass_welcome_lbl.setText(
            _translate("Puzzlelists", "Forgot your password? Make a New One!")
        )
        self.fpass_enterEmail_lbl.setText(
            _translate("Puzzlelists", "Enter your Email ID")
        )
        self.fpass_enterOtp_lineedit.setText(_translate("Puzzlelists", ""))
        self.fpass_enterPass_lbl.setText(
            _translate("Puzzlelists", "Enter your new password")
        )
        self.fpass_enterName_lineedit.setText(_translate("Puzzlelists", ""))
        self.fpass_enterOtp_lbl.setText(_translate("Puzzlelists", "Enter OTP"))
        self.fpass_sendOtp_btn.setText(_translate("Puzzlelists", "Send OTP!"))
        self.fpass_verifyOtp_btn.setText(_translate("Puzzlelists", "Verify OTP!"))
        self.fpass_remark_lbl.setText(
            _translate("Puzzlelists", "An OTP Will be sent to your Email Account")
        )
        self.chgame_welcome_lbl.setText(_translate("Puzzlelists", "Select your Game!"))
        self.chgame_game1_lbl.setText(_translate("Puzzlelists", "1. Space Wars"))
        self.chgame_game2_lbl.setText(_translate("Puzzlelists", "2. 2048"))
        self.chgame_game3_lbl.setText(_translate("Puzzlelists", "3. Icy"))
        self.chgame_game4_lbl.setText(_translate("Puzzlelists", "4. Snake"))
        self.chgame_game5_lbl.setText(_translate("Puzzlelists", "5. Tetris"))
        self.chgame_name_lbl.setText(_translate("Puzzlelists", "Username"))
        self.chgame_coins_lbl.setText(_translate("Puzzlelists", "Puzzler Coins: $50"))
        self.chgame_game1_btn.setText(_translate("Puzzlelists", "$300"))
        self.chgame_game2_btn.setText(_translate("Puzzlelists", "$200"))
        self.chgame_game3_btn.setText(_translate("Puzzlelists", "$100"))
        self.chgame_game4_btn.setText(_translate("Puzzlelists", "Play!"))
        self.chgame_game5_btn.setText(_translate("Puzzlelists", "Play!"))
        self.chgame_viewScore_btn.setText(_translate("Puzzlelists", "View Highscores"))
        self.hgscore_welcome_lbl.setText(_translate("Puzzlelists", "HighScores"))
        self.hgscore_backToGame_btn.setText(
            _translate("Puzzlelists", "Back to Game Selection!")
        )
