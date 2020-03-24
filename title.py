import random
import time

from PyQt5 import QtWidgets
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow

SHELF_SIZE = 50
T = -5
V = 1
A = 1
X_V = 1


def start_animation(title, window, FUNC):
    title.timer = QTimer()
    timer = window.title.timer
    starting_cordinate_hero = [window.title.x(), window.title.y()]
    timer.timeout.connect(lambda: FUNC(starting_cordinate_hero, window.title))
    timer.start(29)


def change_img(obj, ARRAY_OF_IMG, index, H, W):
    pixmap = QPixmap(ARRAY_OF_IMG[index])
    pixmap = pixmap.scaledToHeight(H)
    pixmap = pixmap.scaledToWidth(W)
    obj.setPixmap(pixmap)


def animation_TO_RIGHT(starting_cordinate_hero, hero):
    global T, V, A
    start_y = starting_cordinate_hero[1]
    hero.move(hero.x() + T, start_y)
    if T > 25:
        T += 3
    else:
        T += 1

    if hero.x() >= window.width() // 2 - hero.width() // 2 + 10:
        hero.timer.stop()
        T = -15

        start_animation(title, window, animation_TO_LEFT)


def animation_TO_LEFT(starting_cordinate_hero, hero):
    global T, V, A
    start_y = starting_cordinate_hero[1]
    hero.move(hero.x() - T, start_y)
    if T > 15:
        T += 3
    else:
        T += 1
    if hero.x() <= -hero.width():
        hero.timer.stop()
        T = -5
        start_animation(title, window, animation_TO_RIGHT)


def go_to_CLICK(hand):
    global IMG_HANDS
    change_img(hand, IMG_HANDS, 0, 40, 40)
    IMG_HANDS = IMG_HANDS[::-1]


root = QApplication([])
window = QMainWindow()
bg_new = 'background-color: rgb(%d,%d,%d);' % (random.randint(1, 255), random.randint(1, 255), random.randint(1, 255))

window.setStyleSheet(bg_new)
window.resize(900, 600)

title = QtWidgets.QLabel(window)
title.setStyleSheet("background-color: rgba(0,0,0,0%)")
IMG_TITLE = [QPixmap("static/img/title")]
change_img(title, IMG_TITLE, 0, 330, 430)
title.resize(450, 300)
title.move(window.width() // 2 - title.width() // 2, window.height() // 2 - 272)
title.move(-123, window.height() // 2 - 272)
title.LableOpacity(0.2)
window.layout().addWidget(title)
window.title = title
window.setWindowOpacity(0.9)


hand = QtWidgets.QLabel(window)
IMG_HANDS = [QPixmap("static/img/hand0.png"), QPixmap("static/img/hand1.png")]
bg_new = 'background-color: rgb(%d,%d,%d);' % (random.randint(1, 255), random.randint(1, 255), random.randint(1, 255))
hand.setStyleSheet("background-color: rgba(0,0,0,0%)")
# hand.setStyleSheet(bg_new)
hand.resize(100, 90)

hand.move(window.width() // 2 - hand.width() // 2 + 10, window.height() // 2 + 150)
window.layout().addWidget(hand)
window.hand = hand

hand.timer = QTimer()
timer = window.hand.timer
timer.timeout.connect(lambda: go_to_CLICK(hand))
timer.start(400)

start_animation(title, window, animation_TO_RIGHT)

window.show()
root.exec()
