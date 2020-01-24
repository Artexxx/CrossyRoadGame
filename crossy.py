from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QWidget
from random import randint

shelf_size = 100


class drow(QWidget):
    def paintEvent(self, event):
        painter = QPainter(self)
        w = self.width()
        y = 0
        while y < h:
            y += shelf_size
            painter.drawLine(0, y, w, y)


class Box(QLabel):
    pass


def check_colision(hero, monst):
    x_b = hero.x()
    y_b = hero.y()
    x1_b = hero.x() + hero.width()
    y1_b = hero.y() + hero.height()

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


speed = 10


def move_hero(window, key):
    global speed
    x = window.hero.x()
    y = window.hero.y()
    hero = window.hero
    if key == Qt.Key_Left:
        hero.move(x - speed, y)
    elif key == Qt.Key_Up:
        hero.move(x, y - shelf_size)
    elif key == Qt.Key_Right:
        hero.move(x + speed, y)

    for monst in window.monsters:
        check_colision(hero, monst)

def move_monster(monst, key):

    x = monst.x()
    y = monst.y()
    # monst = window.monst
    speed = monst.speed
    if key == Qt.Key_Left:
        monst.move(x - speed, y)
    elif key == Qt.Key_Right:
        monst.move(x + speed, y)




class HeroWindow(QMainWindow):
    def keyPressEvent(self, event):
        hero = self.hero
        key = event.key()
        if key != Qt.Key_Down:
            hero.direction = key


def make_hero(window):
    hero = Box()
    hero.setFixedSize(100, 100)
    hero.move(int((window.width() - hero.width()) / 2), int((window.height() - hero.height())))
    hero.direction = Qt.Key_Up
    hero.setStyleSheet("background-color:  black")
    window.layout().addWidget(hero)
    window.hero = hero
    HeroWindow.hero = hero


def monster_direction_random():
    if randint(0, 1):
        return Qt.Key_Left
    return Qt.Key_Right


def make_monster(window):
    monst = Box()
    mnst_size = [randint(3, 10) * 10, randint(1, 10) * 10]
    monst.setFixedSize(mnst_size[0], mnst_size[1])
    monst.move(int((randint(-3, 15) * shelf_size - monst.width()) / 2),
               int((randint(-3, 15) * shelf_size - monst.height())))
    monst.direction = monster_direction_random()
    monst.speed = randint(15,40)
    monst.setStyleSheet("background-color:  red")
    window.layout().addWidget(monst)
    monst.timer = QTimer()

    timer = monst.timer
    timer.setInterval(266)
    timer.timeout.connect(lambda: move_monster(monst, monst.direction))
    timer.start()

    window.monsters.append(monst)


root = QApplication([])
window = HeroWindow()
window.resize(900, 600)
window.setStyleSheet("background-color:  #FF9E73")

window.monsters = []

shelf_number = window.height() // 100

pole = drow()
pole.resize(900, 600)
window.layout().addWidget(pole)

make_hero(window)
for i in range(15):
    make_monster(window)

timer = QTimer()
timer.timeout.connect(lambda: move_hero(window, HeroWindow.hero.direction))
timer.start(266)

window.show()
root.exec()
