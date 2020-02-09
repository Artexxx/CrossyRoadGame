from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel


class Box(QLabel):
    pass


def make_monster(window):
    monst = Box()
    monst.setFixedSize(200, 100)
    monst.move((window.width() - 300) / 2, window.height() / 2)
    monst.setStyleSheet("background-color:  brown")
    window.layout().addWidget(monst)
    HeroWindow.monst = monst

def check_colision(window):
    hero = window.hero
    x_b = hero.x()
    y_b = hero.y()
    x1_b = hero.x() + hero.width()
    y1_b = hero.y() + hero.height()

    monst = window.monst
    x_m = monst.x()
    y_m = monst.y()
    x1_m = monst.x() + monst.width()
    y1_m = monst.y() + monst.height()
    if (x1_b > x_m) and (x_b < x1_m) and (y1_b > y_m) and (y_b < y1_m):
        monst.setStyleSheet("background-color:  red")
    else:
        monst.setStyleSheet("background-color:  brown")


def check_colision2(window):
    hero = window.hero
    x_b = hero.x()
    y_b = hero.y()
    x1_b = hero.x() + hero.width()
    y1_b = hero.y() + hero.height()

    monst = window.monst
    x_m = monst.x()
    y_m = monst.y()
    x1_m = monst.x() + monst.width()
    y1_m = monst.y() + monst.height()

    s1 = (x_b > x_m and x_b < x1_m) or (x1_b > x_m and x1_b < x1_m)
    s2 = (y_b > y_m and y_b < y1_m) or (y1_b > y_m and y1_b < y1_m)
    s3 = (x_m > x_b and x_m < x1_b) or (x1_m > x_b and x1_m < x1_b)
    s4 = (y_m > y_b and y_m < y1_b) or (y1_m > y_b and y1_m < y1_b)

    if ((s1 and s2) or (s3 and s4)) or ((s1 and s4) or (s3 and s2)):
        monst.setStyleSheet("background-color:  red")
    else:
        monst.setStyleSheet("background-color:  brown")


def make_button(window, x, y):
    hero = Box()
    hero.setFixedSize(100, 100)
    hero.move(x, y)
    hero.direction = Qt.Key_Up
    hero.setStyleSheet("background-color:  black")
    window.layout().addWidget(hero)
    window.hero = hero
    HeroWindow.hero = hero


def move_button(window, key):
    speed = 100
    x = window.hero.x()
    y = window.hero.y()
    hero = window.hero
    if key == Qt.Key_Left:
        hero.move(x - speed, y)
    elif key == Qt.Key_Up:
        hero.move(x, y - speed)
    elif key == Qt.Key_Right:
        hero.move(x + speed, y)
    elif key == Qt.Key_Down:
        hero.move(x, y + speed)
    check_colision(window)


class HeroWindow(QMainWindow):
    def keyPressEvent(self, event):
        key = event.key()
        move_button(window, key)


root = QApplication([])
window = HeroWindow()
window.resize(900, 600)
window.setStyleSheet("background-color:  #FF9E73")

make_button(window, 300, 300)
make_monster(window)

move_button(window, HeroWindow.hero.direction)

window.show()
root.exec()
