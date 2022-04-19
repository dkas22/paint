

from PyQt5.QtWidgets import (QWidget, QSlider, QLineEdit, QLabel, QPushButton, QScrollArea,QApplication,
                             QHBoxLayout, QVBoxLayout, QMainWindow)
from PyQt5.QtCore import Qt, QSize
from PyQt5 import QtWidgets, uic
import sys



class MainWindow1(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.scroll = QScrollArea()             # Scroll Area which contains the widgets, set as the centralWidget
        self.widget = QWidget()                 # Widget that contains the collection of Vertical Box
        self.vbox = QVBoxLayout()               # The Vertical Box that contains the Horizontal Boxes of  labels and buttons


        aboutText = QLabel("Paint is a 2D Painting and Drawing Application. It can be used to for drawing and sketching. It has a number of tools for sketching and drawing like pen, brush, fill, spray etc. It has many standard shapes like rectangle, arrow left, arrow right, star, pentagon etc. It also provide user to change text color, text size, text style, brush size, spray size, eraser size etc. It also has a feature of undo and redo. It provides a number of features. e.g. user can save his/her sketch/drawing, user can crop a images, user can insert a picture into his/her sketching, user can write text on image. etc")

        aboutText.setMinimumWidth(720)
        aboutText.setStyleSheet("font-size:16px;")
        aboutText.setWordWrap(True)
        self.vbox.addWidget(aboutText, 1, Qt.AlignCenter)

        version = QLabel("Version: 1.0.0")
        version.setStyleSheet("font-size:16px;font-weight: bold;")
        self.vbox.addWidget(version, 0, Qt.AlignCenter)

        developedBy = QLabel("Developed By Chhotu Kumar")
        developedBy.setStyleSheet("font-size:20px; font-weight: bold; margin-bottom: 20px;")
        self.vbox.addWidget(developedBy, 0, Qt.AlignCenter)

        self.widget.setLayout(self.vbox)

        #Scroll Area Properties
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)

        self.setCentralWidget(self.scroll)

        self.setGeometry(600, 100, 1000, 900)
        self.setWindowTitle('About Paint')
