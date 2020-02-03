from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QWidget
from random import randint, choice

SHELF_SIZE = 100
SHELF_N = 10


class drow(QWidget):
    def paintEvent(self, event):
        painter = QPainter(self)
        w = self.width()
        h = self.height()
        y = 0
        while y <= h:
            y += SHELF_SIZE
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

    return ((s1 and s2) or (s3 and s4)) or ((s1 and s4) or (s3 and s2))


speed = 10


def move_hero(window, key):
    global speed
    x = window.hero.x()
    y = window.hero.y()
    hero = window.hero
    if key == Qt.Key_Left:
        hero.move(x - speed, y)
    elif key == Qt.Key_Up:
        hero.move(x, y - SHELF_SIZE)
    elif key == Qt.Key_Right:
        hero.move(x + speed, y)
    elif key == Qt.Key_Down:
        hero.move(x, y + SHELF_SIZE)

    for monst in window.monsters:
        if check_colision(hero, monst):
            monst.setStyleSheet("background-color:  red")
        else:
            monst.setStyleSheet("background-color:  brown")
    for tree in window.trees:
        if check_colision(hero, tree):
            tree.setStyleSheet("background-color:  red")
        else:
            tree.setStyleSheet("background-color:  blue")
        dict_direction = {Qt.Key_Left: Qt.Key_Right, Qt.Key_Down: Qt.Key_Up, Qt.Key_Right: Qt.Key_Left,
                          Qt.Key_Up: Qt.Key_Down}
        move_hero(window, dict_direction[key])


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
    global position_MONSTER
    monst = Box()
    mnst_size = [randint(3, 10) * 10, randint(1, 10) * 10]
    monst.setFixedSize(mnst_size[0], mnst_size[1])
    # monst.move(randint(-3, 15) * SHELF_SIZE ,int(randint(1, 8) * SHELF_SIZE ) - monst.height())   ---Random
    monst.move(randint(1, 8) * SHELF_SIZE,
               position_MONSTER.pop(randint(0, len(position_MONSTER) - 1)) * SHELF_SIZE - monst.height())

    monst.direction = monster_direction_random()
    monst.speed = randint(15, 40)
    monst.setStyleSheet("background-color:  brown")
    window.layout().addWidget(monst)
    monst.timer = QTimer()
    timer = monst.timer
    timer.setInterval(266)
    timer.timeout.connect(lambda: move_monster(monst, monst.direction))
    timer.start()

    window.monsters.append(monst)


def make_tree(line_coordinate, window):
    global position_TREE

    tree = Box()
    tree.setFixedSize(SHELF_SIZE, SHELF_SIZE)
    tree.move(position_TREE.pop(randint(0, len(position_TREE) - 1)) * SHELF_SIZE, line_coordinate)
    tree.setStyleSheet("background-color:  blue")
    window.layout().addWidget(tree)
    window.tree = tree
    window.trees.append(tree)
    HeroWindow.tree = tree


forest_coordinate = []


def make_forest(window):
    global forest_coordinate, position_FOREST
    forest = Box()
    forest.setFixedSize(window.width(), SHELF_SIZE)

    forest.move(0, position_FOREST.pop(randint(0, len(position_FOREST) - 1)) * SHELF_SIZE)
    # forest.move(0, int((randint(1, 10) * SHELF_SIZE)))
    forest_coordinate.append(forest.y())
    forest.setStyleSheet("background-color:  green")
    window.layout().addWidget(forest)
    HeroWindow.forest = forest


root = QApplication([])
window = HeroWindow()
window.resize(900, 600)
window.setStyleSheet("background-color:  #FF9E73")

window.monsters = []
window.trees = []

shelf_number = window.height() // 100

pole = drow()
pole.resize(900, 600)
window.layout().addWidget(pole)

position_FOREST = [1, 2, 3]
for i in range(3):
    make_forest(window)

print(forest_coordinate)
position_TREE = [1, 3, 6]
for i in range(2):
    for crd in forest_coordinate:
        make_tree(crd, window)
make_hero(window)

position_MONSTER = [4, 5]
for i in range(2):
    make_monster(window)

timer = QTimer()
timer.timeout.connect(lambda: move_hero(window, HeroWindow.hero.direction))
timer.start(266)

window.show()
root.exec()
