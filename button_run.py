from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QWidget
from random import randint, choice

SHELF_SIZE = 50
SHELF_N = 20


class drow(QWidget):
    def paintEvent(self, event):
        painter = QPainter(self)
        w = self.width()
        h = self.height()
        y = 0
        while y <= h:
            y += SHELF_SIZE
            painter.drawLine(0, y, w, y)


class finish(QWidget):

    def paintEvent(self, event):
        qp = QPainter(self)
        col = QColor(200, 0, 0)  # рамка
        col.setNamedColor('#de2323')
        qp.setPen(col)

        x = 0
        y = 0
        SIZE_RECT = 25
        while x < window.width():
            qp.setBrush(QColor(200, 0, 0))
            qp.drawRect(x, y, SIZE_RECT, SIZE_RECT)

            qp.drawRect(x + SIZE_RECT, y + SIZE_RECT, SIZE_RECT, SIZE_RECT)
            x += 50


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
        if check_colision(window.hero, car):
            print("HI" * 100)
            car.setStyleSheet("background-color:  red")
            return True
        else:
            car.setStyleSheet("background-color:  brown")


def check_colision_with_tree(window):
    if window.y() != 0:
        return False
    for tree in window.trees:
        if check_colision(window.hero, tree):
            return True


# ___________________________________________________________Finish________________________________________

def move_game_window(window1, window2):
    global base_window, window
    for car in window1.cars:
        car.timer.stop()

    if window1.y() < base_window.height():
        window1.move(window1.x(), window1.y() + 10)
        window2.move(window2.x(), window2.y() + 10)
        window1.hero.move(window1.hero.x(), window1.hero.y() + 10)


    else:
        window1.timer.stop()
        window2.hero = window1.hero
        window = window2
    # window.hero.move(int((window.width() - SHELF_SIZE) / 2), int((window.height() - SHELF_SIZE)))
    # window.move(window.x(), -window.y())
    # base_window.hero.timer.stop()
    # base_window.hero.timer = QTimer()
    # timer = base_window.hero.timer
    # timer.timeout.connect(lambda: move_hero(window2, window.hero.direction))
    # timer.start(266)


def check_finish_line(window):
    global base_window
    if window.hero.y() < SHELF_SIZE and window.y() == 0:
        window2 = QMainWindow()
        window2.resize(900, 700)
        window2.setStyleSheet("background-color:  #FF9E73")
        window2.move(0, -window.height())
        base_window.layout().addWidget(window2)
        window.hero.setParent(None)
        base_window.layout().addWidget(window.hero)
        filling_the_window(window2)
        window.timer = QTimer()
        timer = window.timer
        timer.setInterval(16)
        timer.timeout.connect(lambda: move_game_window(window, window2))
        timer.start()
        # window.move(window.width(),0)


# ______________________________________________________________________________________________________

def blocking_hero_movement(hero):
    x = hero.x()
    y = hero.y()
    if (x < 0) or (y < 0) or (x >= window.width()) or (y >= window.height()):
        return True


def move_hero(key):
    global window
    check_colision_with_car(window)
    SPEED = int(SHELF_SIZE / 2)
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
    check_finish_line(window)
    if check_colision_with_tree(window) or blocking_hero_movement(hero):
        dict_direction = {Qt.Key_Left: Qt.Key_Right, Qt.Key_Down: Qt.Key_Up, Qt.Key_Right: Qt.Key_Left,
                          Qt.Key_Up: Qt.Key_Down}
        move_hero(dict_direction[key])


def transportation(car):
    x = car.x()
    y = car.y()
    if x < -car.width():
        car.move(x + window.width() + car.width(), y)
    elif x > window.width() + car.width():
        car.move(-car.width(), y)


def move_car(car):
    x = car.x()
    y = car.y()
    speed = car.speed
    if car.direction == Qt.Key_Left:
        car.move(x - speed, y)
    elif car.direction == Qt.Key_Right:
        car.move(x + speed, y)
    transportation(car)


class HeroWindow(QMainWindow):
    def keyPressEvent(self, event):
        hero = self.hero
        key = event.key()
        hero.direction = key


def make_hero(window, base_window):
    hero = Box()
    hero.setFixedSize(SHELF_SIZE, SHELF_SIZE)
    hero.move(int((window.width() - hero.width()) / 2), int((window.height() - hero.height())))
    hero.direction = Qt.Key_Down
    hero.setStyleSheet("background-color:  black")
    base_window.layout().addWidget(hero)
    window.hero = hero
    base_window.hero = hero


def make_car(position_road, position_car, TYPE_CAR, window):
    car = Box()
    car.setFixedSize(TYPE_CAR["Width"], SHELF_SIZE)
    car.move(position_car * SHELF_SIZE, position_road * SHELF_SIZE)
    car.speed = 5
    car.direction = TYPE_CAR["Direction"]
    car.setStyleSheet("background-color:  brown")
    window.layout().addWidget(car)
    car.timer = QTimer()
    timer = car.timer
    timer.setInterval(TYPE_CAR["V"])
    timer.timeout.connect(lambda: move_car(car))
    timer.start()

    window.cars.append(car)


def make_tree(position_tree, position_forest, window):
    tree = Box()
    tree.setFixedSize(SHELF_SIZE, SHELF_SIZE)
    tree.move(position_tree * SHELF_SIZE, position_forest * SHELF_SIZE)
    tree.setStyleSheet("background-color:  #502D0C")
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
    road.setFixedSize(window.width(), SHELF_SIZE - 1)
    road.move(0, road_coordinate * SHELF_SIZE + 1)
    road.setStyleSheet("background-color:  #877474")
    window.layout().addWidget(road)
    HeroWindow.forest = road


def make_finish_line(window):
    pole = finish()
    pole.setFixedSize(window.width(), SHELF_SIZE)

    window.layout().addWidget(pole)


def filling_the_window(window):
    window.cars = []
    window.trees = []

    # ____________________________________________________________FOREST_________________________________
    DATA_FOREST = {1: [i for i in range(0, 18, randint(2, 4))],
                   4: [i for i in range(0, 18, randint(2, 4))],
                   5: [i for i in range(0, 18, randint(2, 4))],
                   8: [i for i in range(0, 18, randint(2, 4))],
                   11: [i for i in range(0, 18, 5)], }
    for forest_coordinate in DATA_FOREST.keys():
        make_forest(forest_coordinate, window)
        for tree_coordinate in DATA_FOREST[forest_coordinate]:
            make_tree(tree_coordinate, forest_coordinate, window)

    # ____________________________________________________________ROAD_________________________________
    car1 = {"V": 60, "Width": 100, "Direction": Qt.Key_Left, }
    car2 = {"V": 15, "Width": 50, "Direction": Qt.Key_Right, }

    DATA_CARS = {2: [car1, car1, car1, car1], 3: [car2, car2, car2, car2],
                 6: [car1, car1, car1], 7: [car2, car2, car2, car2],
                 9: [car1, car1, car1, car1], 10: [car2, car2], }
    for position_road in DATA_CARS.keys():
        make_road(position_road, window)

        position_car = 0
        n = SHELF_N // len(DATA_CARS[position_road])
        for data_car in DATA_CARS[position_road]:
            position_car += n
            make_car(position_road, position_car, data_car, window)
    # ___________________________________________________________________________________________________
    make_finish_line(window)


root = QApplication([])
window = QMainWindow()
window.resize(900, 600)
window.setStyleSheet("background-color:  #FF9E73")


base_window = HeroWindow()
base_window.resize(900, 600)

base_window.setStyleSheet("background-color:  #123E73")
base_window.layout().addWidget(window)

pole = drow()
pole.resize(900, 600)
window.layout().addWidget(pole)

filling_the_window(window)
make_hero(window, base_window)

base_window.hero.timer = QTimer()
timer = base_window.hero.timer
timer.timeout.connect(lambda: move_hero(window.hero.direction))
timer.start(266)

base_window.show()
root.exec()
