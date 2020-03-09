SHELF_SIZE = 50
T = 0
V = 10
A = 2
X_V = 2


def jump_to_right(starting_cordinate_hero, hero):
    global T, V, A
    start_y = starting_cordinate_hero[0]
    Y = (-V) * T + A * T * T / 2
    hero.move(hero.x() + X_V, start_y + Y)
    T = T + 1
    if hero.y() > start_y:
        hero.move(starting_cordinate_hero[1] + 25, start_y)
        T = 0
        hero.jump_timer = "Stop"


def jump_to_left(starting_cordinate_hero, hero):
    global T, V, A
    start_y = starting_cordinate_hero[0]
    Y = (-V) * T + A * T * T / 2
    hero.move(hero.x() - X_V, start_y + Y)
    T = T + 1
    if hero.y() > start_y:
        hero.move(starting_cordinate_hero[1] - 25, start_y)
        T = 0
        hero.jump_timer = "Stop"


def jump_to_down(starting_cordinate_hero, hero):
    global T, V, A
    start_y = starting_cordinate_hero[0]
    Y = (V - 11) * T + A * T * T / 2
    hero.move(hero.x(), start_y + Y)
    T = T + 1
    if hero.y() > start_y + SHELF_SIZE:
        hero.move(hero.x(), start_y + SHELF_SIZE)
        T = 0
        hero.jump_timer = "Stop"


def jump_to_up(starting_cordinate_hero, hero):
    global T, V, A
    start_y = starting_cordinate_hero[0]
    Y = (-V - 11) * T + A * T * T / 2  # если 10, то недопрыгнит
    hero.move(hero.x(), start_y + Y)
    T = T + 1
    if hero.y() < start_y - SHELF_SIZE:
        hero.move(hero.x(), start_y - SHELF_SIZE)
        T = 0
        hero.jump_timer = "Stop"
