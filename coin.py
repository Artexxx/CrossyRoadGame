import random

from PyQt5 import QtWidgets
from PyQt5.QtGui import QFont, QPixmap

SHELF_SIZE = 50
T = 0
V = 1
A = 1
X_V = 1
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow


def make_w():
    window1 = QMainWindow()
    window1.showFullScreen()
    window1.setStyleSheet("background-color: #FF9E73")

    window1.show()


def move_clock(clock):
    x = clock.x()
    y = clock.y()


def jump_to_down(starting_cordinate_hero, hero):
    global T, V, A
    start_y = starting_cordinate_hero[0]
    Y = (V - 2) * T + A * T * T / 2
    hero.move(hero.x() + (Y * 0.1), start_y + (Y * 0.8))
    T = T + 0.7
    hero.resize(hero.width() + 3, hero.height() + 3)
    if hero.x() >= window.width() // 2 - hero.width() // 2 or hero.y() >= window.height() // 2 - hero.height() // 2:
        hero.timer.stop()


root = QApplication([])
window = QMainWindow()
bg_new = 'background-color: rgb(%d,%d,%d);' % (random.randint(1, 255), random.randint(1, 255), random.randint(1, 255))

window.setStyleSheet(bg_new)
window.resize(900, 600)
#
# quit = QAction("Quit", window)
# quit.triggered.connect(lambda: make_w())

clock = QtWidgets.QLabel(window)
clock.setFont(QFont("setItalic", 20))
clock.setText('Label Example')
bg_new = 'background-color: rgb(%d,%d,%d);' % (random.randint(1, 255), random.randint(1, 255), random.randint(1, 255))
clock.setStyleSheet(bg_new)
clock.move(0, 0)
window.layout().addWidget(clock)
window.clock = clock

clock.timer = QTimer()
timer = window.clock.timer
starting_cordinate_hero = [window.clock.y(), window.clock.x()]
timer.timeout.connect(lambda: jump_to_down(starting_cordinate_hero, window.clock))
timer.start(30)

window.show()
root.exec()
