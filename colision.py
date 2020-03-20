from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from hero_jump import jump_to_down, jump_to_left, jump_to_right, jump_to_up


class Box(QLabel):
    pass


def make_monster(window):
    monst = Box()
    monst.setFixedSize(50, 77)
    monst.move((window.width() - 300) / 2, window.height() / 2)
    # monst.setStyleSheet("colorcolorcolor:trunsparent")
    # monst.setAutoFillBackground(False)
    monst.setStyleSheet("background-color: rgba(0,0,0,0%)")
    change_img(monst, TREE_IMG, 2)
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


def change_img(obj, ARRAY_OF_IMG, index):
    pixmap = QPixmap(ARRAY_OF_IMG[index])
    pixmap = pixmap.scaledToHeight(77)
    # pixmap = pixmap.scaledToWidth(55)
    obj.setPixmap(pixmap)


def make_button(window, x, y):
    hero = Box()
    hero.setFixedSize(50, 50)
    hero.move(x, y)
    hero.jump_timer = "Stop"
    hero.direction = Qt.Key_Up
    hero.setStyleSheet("background-color:  black")
    window.layout().addWidget(hero)
    window.hero = hero
    HeroWindow.hero = hero


def start_jump_hero(hero, function_direction_jump: 'function'):
    if hero.jump_timer == "Stop":
        hero.jump_timer = QTimer()
        timer = window.hero.jump_timer
        starting_cordinate_hero = [window.hero.y(), window.hero.x()]
        timer.timeout.connect(lambda: function_direction_jump(starting_cordinate_hero, hero))
        timer.start(30)

def move_button(window, key):
    check_colision(window)

    if key == Qt.Key_Left:
        start_jump_hero(window.hero, jump_to_left)
    elif key == Qt.Key_Up:
        start_jump_hero(window.hero, jump_to_up)
    elif key == Qt.Key_Right:
        start_jump_hero(window.hero, jump_to_right)
    elif key == Qt.Key_Down:
        start_jump_hero(window.hero, jump_to_down)

    check_colision(window)


class HeroWindow(QMainWindow):
    def keyPressEvent(self, event):
        key = event.key()
        move_button(window, key)


root = QApplication([])
window = HeroWindow()
window.resize(900, 600)
window.setStyleSheet("background-color:  #FF9E73")

tree_img_names = ['small.png', 'medium.png', 'large.png']
TREE_IMG = [QPixmap("static/img/tree-" + img_name) for img_name in tree_img_names]

make_button(window, 300, 300)
make_monster(window)

move_button(window, HeroWindow.hero.direction)

window.show()
root.exec()
