import time

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel

T = 0
V = 10
A = 2
X_V = 5
is_movement_blocked = False


class Box(QLabel):
    pass


def make_hero(window, x, y):
    hero = Box()
    hero.setFixedSize(100, 100)
    hero.move(x, y)
    hero.direction = Qt.Key_Up
    hero.timer = "Stop"
    hero.setStyleSheet("background-color:  black")
    window.layout().addWidget(hero)
    window.hero = hero
    HeroWindow.hero = hero


def jump_to_right(starting_cordinate_hero, hero):
    global T, V, A
    start_y = starting_cordinate_hero[0]
    Y = -V * T + A * T * T / 2
    hero.move(hero.x() + X_V, start_y + Y)
    T = T + 1
    if hero.y() > start_y:
        hero.move(hero.x(), start_y)
        T = 0
        hero.timer = "Stop"


def jump_to_left(starting_cordinate_hero, hero):
    global T, V, A
    start_y = starting_cordinate_hero[0]
    Y = -V * T + A * T * T / 2
    hero.move(hero.x() - X_V, start_y + Y)
    T = T + 1
    if hero.y() > start_y:
        hero.move(hero.x(), start_y)
        T = 0
        hero.timer = "Stop"


def jump_to_down(starting_cordinate_hero, hero):
    global T, V, A
    start_y = starting_cordinate_hero[0]
    Y = (-V + 11) * T + A * T * T / 2
    hero.move(hero.x(), start_y + Y)
    T = T + 1
    if hero.y() > start_y + 100:
        T = 0
        hero.timer = "Stop"


def jump_to_up(starting_cordinate_hero, hero):
    global T, V, A
    start_y = starting_cordinate_hero[0]
    Y = (-V - 11) * T + A * T * T / 2  # если 10, то недопрыгнит
    hero.move(hero.x(), start_y + Y)
    T = T + 1
    if hero.y() < start_y - 100:
        T = 0
        hero.timer = "Stop"


def start_jump_hero(hero, function_direction_jump: 'function'):
    if hero.timer == "Stop":
        hero.timer = QTimer()
        timer = window.hero.timer
        starting_cordinate_hero = [window.hero.y(), window.hero.x()]
        timer.timeout.connect(lambda: function_direction_jump(starting_cordinate_hero, hero))
        timer.start(30)


def move_hero(window, key):
    global jump_to_right
    if key == Qt.Key_Left:
        start_jump_hero(window.hero, jump_to_left)
    elif key == Qt.Key_Up:
        start_jump_hero(window.hero, jump_to_up)
    elif key == Qt.Key_Right:
        start_jump_hero(window.hero, jump_to_right)
    elif key == Qt.Key_Down:
        start_jump_hero(window.hero, jump_to_down)


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
