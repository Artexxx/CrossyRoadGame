import time

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel

T = 0
V = 10
A = 2
X_V = 5


class Box(QLabel):
    pass


def make_hero(window, x, y):
    hero = Box()
    hero.setFixedSize(100, 100)
    hero.move(x, y)
    hero.direction = Qt.Key_Up
    hero.setStyleSheet("background-color:  black")
    window.layout().addWidget(hero)
    window.hero = hero
    HeroWindow.hero = hero


def jump_to_right(start_y, hero):
    global T, V, A
    Y = -V * T + A * T * T / 2
    hero.move(hero.x() + X_V, start_y + Y)
    T = T + 1
    if hero.y() > start_y:  # or hero.y() == stop_x():
        T = 0
        hero.timer = "Stop"


def desine(start_y, hero):
    global T
    jump_to_right(start_y, hero)


def start_timer_on_hero(hero):
    window.hero.timer = QTimer()
    timer = window.hero.timer
    start_x = window.hero.y()
    timer.timeout.connect(lambda: desine(start_x, window.hero))
    timer.start(30)


def move_hero(window, key):
    speed = 100
    x = window.hero.x()
    y = window.hero.y()
    hero = window.hero
    if key == Qt.Key_Left:
        hero.move(x - speed, y)
    elif key == Qt.Key_Up:
        hero.move(x, y - speed)
    elif key == Qt.Key_Right:
        window.hero.timer = "Stop"
        if hero.timer == "Stop":
            start_timer_on_hero(window.hero)

    elif key == Qt.Key_Down:
        hero.move(x, y + speed)


class HeroWindow(QMainWindow):
    def keyPressEvent(self, event):
        key = event.key()
        move_hero(window, key)


root = QApplication([])
window = HeroWindow()
window.resize(900, 600)
window.setStyleSheet("background-color:  #FF9E73")

make_hero(window, 300, 300)

move_hero(window, HeroWindow.hero.direction)

window.show()
root.exec()
