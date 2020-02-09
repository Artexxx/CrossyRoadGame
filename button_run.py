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

# ____________________________________________________________COLISION_________________________________

def check_colision(hero, car):
    x_b = hero.x()
    y_b = hero.y()
    x1_b = hero.x() + hero.width()
    y1_b = hero.y() + hero.height()

    x_m = car.x()
    y_m = car.y()
    x1_m = car.x() + car.width()
    y1_m = car.y() + car.height()

    return (x1_b > x_m) and (x_b < x1_m) and (y1_b > y_m) and (y_b < y1_m)


def check_colision_with_car(window):
    for car in window.cars:
        transportation(car)
        if check_colision(window.hero, car):
            car.setStyleSheet("background-color:  red")
        else:
            car.setStyleSheet("background-color:  brown")


def check_colision_with_tree(window):
    for tree in window.trees:
        if check_colision(window.hero, tree):
            return True


# ______________________________________________________________________________________________________


def move_hero(window, key):
    SPEED = 50
    x = window.hero.x()
    y = window.hero.y()
    hero = window.hero
    if key == Qt.Key_Left:
        hero.move(x - SPEED, y)
    elif key == Qt.Key_Up:
        hero.move(x, y - SHELF_SIZE)
    elif key == Qt.Key_Right:
        hero.move(x + SPEED, y)
    elif key == Qt.Key_Down:
        hero.move(x, y + SHELF_SIZE)

    check_colision_with_car(window)
    if check_colision_with_tree(window):
        dict_direction = {Qt.Key_Left: Qt.Key_Right, Qt.Key_Down: Qt.Key_Up, Qt.Key_Right: Qt.Key_Left,
                          Qt.Key_Up: Qt.Key_Down}
        move_hero(window, dict_direction[key])


def move_car(car, key):
    x = car.x()
    y = car.y()
    speed = car.speed
    if key == Qt.Key_Left:
        car.move(x - speed, y)
    elif key == Qt.Key_Right:
        car.move(x + speed, y)


def transportation(car):
    x = car.x()
    y = car.y()
    if x < 0:
        car.move(x + window.width(), y)
    elif y < 0:
        car.move(x, y + window.height())
    elif x > window.width():
        car.move(0, y)
    elif y > window.height():
        car.move(x, 0)


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


def car_direction_random():
    if randint(0, 1):
        return Qt.Key_Left
    return Qt.Key_Right


def make_car(position_road, TYPE_CAR, window):
    car = Box()
    car.setFixedSize(TYPE_CAR["W"], SHELF_SIZE)
    car.move(position_road * SHELF_SIZE, position_road * SHELF_SIZE)
    car.speed = 10
    car.direction = car_direction_random()
    car.setStyleSheet("background-color:  brown")
    window.layout().addWidget(car)
    car.timer = QTimer()
    timer = car.timer
    timer.setInterval(TYPE_CAR["V"])
    timer.timeout.connect(lambda: move_car(car, car.direction))
    timer.start()

    window.cars.append(car)


def make_tree(position_tree, position_forest, window):
    tree = Box()
    tree.setFixedSize(SHELF_SIZE, SHELF_SIZE)
    tree.move(position_tree * SHELF_SIZE, position_forest * SHELF_SIZE)
    tree.setStyleSheet("background-color:  blue")
    window.layout().addWidget(tree)
    window.tree = tree
    window.trees.append(tree)
    HeroWindow.tree = tree


def make_forest(forest_coordinate, window):
    forest = Box()
    forest.setFixedSize(window.width(), SHELF_SIZE)
    forest.move(0, forest_coordinate * SHELF_SIZE)
    forest.setStyleSheet("background-color:  green")
    window.layout().addWidget(forest)
    HeroWindow.forest = forest


def make_road(road_coordinate, window):
    road = Box()
    road.setFixedSize(window.width(), SHELF_SIZE)
    road.move(0, road_coordinate * SHELF_SIZE)
    road.setStyleSheet("background-color:  #877474")
    window.layout().addWidget(road)
    HeroWindow.forest = road


root = QApplication([])
window = HeroWindow()
window.resize(900, 600)
window.setStyleSheet("background-color:  #FF9E73")

window.cars = []
window.trees = []

shelf_number = window.height() // 100

pole = drow()
pole.resize(900, 600)
window.layout().addWidget(pole)

# ____________________________________________________________FOREST_________________________________
DATA_FOREST = {0: [0, 4, 6], 4: [1, 5]}

for forest_coordinate in DATA_FOREST.keys():
    make_forest(forest_coordinate, window)
    for tree_coordinate in DATA_FOREST[forest_coordinate]:
        make_tree(tree_coordinate, forest_coordinate, window)

# ____________________________________________________________ROAD_________________________________
car1 = {"V": 166, "W": 100, }
car2 = {"V": 36, "W": 50, }

DATA_CARS = {2: [car1], 3: [car2]}
for position_road in DATA_CARS.keys():
    make_road(position_road, window)

    for key in DATA_CARS[position_road]:
        make_car(position_road, key, window)
# ___________________________________________________________________________________________________


make_hero(window)

timer = QTimer()
timer.timeout.connect(lambda: move_hero(window, HeroWindow.hero.direction))
timer.start(266)

window.show()
root.exec()
