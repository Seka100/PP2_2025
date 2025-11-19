import pygame
import random
import sys

pygame.init()

# параметры окна
w = 600
h = 400
s = 20   # размер квадрата

# цвета
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 200, 0)
red = (200, 0, 0)
yellow = (220, 220, 0)
orange = (255, 150, 50)

win = pygame.display.set_mode((w, h))
pygame.display.set_caption('Snake')

clk = pygame.time.Clock()
fnt = pygame.font.SysFont('arial', 24)


# генерация еды вне тела
def rnd_food(body):
    while True:
        x = random.randrange(0, w - s, s)
        y = random.randrange(0, h - s, s)
        if (x, y) not in body:
            return (x, y)


# вывод текста
def txt(t, x, y):
    win.blit(fnt.render(t, True, white), (x, y))


# завершение игры
def over(sc):
    win.fill(black)
    t = fnt.render(f'Игра окончена! Очки: {sc}', True, red)
    win.blit(t, (w // 2 - t.get_width() // 2, h // 2))
    pygame.display.update()
    pygame.time.wait(2000)
    pygame.quit()
    sys.exit()


# список видов еды: цвет, вес
food_types = [
    {"color": yellow, "value": 1},   # простая еда
    {"color": orange, "value": 2},   # средняя
    {"color": red,    "value": 3},   # редкая
]


# создаём новый кусок еды с таймером
def spawn_food(body):
    pos = rnd_food(body)
    info = random.choice(food_types)

    # таймер исчезновения (в тиках)
    timer = random.randint(120, 200)

    return {
        "pos": pos,
        "color": info["color"],
        "value": info["value"],
        "timer": timer
    }


def main():
    body = [(100, 100), (80, 100), (60, 100)]
    dir = 'RIGHT'

    food = spawn_food(body)

    sc = 0
    lvl = 1
    spd = 10

    while True:

        # обработка управления
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_UP and dir != 'DOWN':
                    dir = 'UP'
                elif e.key == pygame.K_DOWN and dir != 'UP':
                    dir = 'DOWN'
                elif e.key == pygame.K_LEFT and dir != 'RIGHT':
                    dir = 'LEFT'
                elif e.key == pygame.K_RIGHT and dir != 'LEFT':
                    dir = 'RIGHT'

        # движение змейки
        x, y = body[0]

        if dir == 'UP': y -= s
        elif dir == 'DOWN': y += s
        elif dir == 'LEFT': x -= s
        elif dir == 'RIGHT': x += s

        head = (x, y)

        # столкновение со стеной или собой
        if x < 0 or x >= w or y < 0 or y >= h or head in body:
            over(sc)

        body.insert(0, head)

        # проверяем, съели ли еду
        if head == food["pos"]:
            sc += food["value"]   # учитываем вес еды
            food = spawn_food(body)
        else:
            body.pop()

        # таймер исчезновения еды
        food["timer"] -= 1
        if food["timer"] <= 0:
            food = spawn_food(body)

        # повышение уровня
        if sc and sc % 4 == 0:
            lvl = sc // 4 + 1
            spd = 10 + lvl * 2

        # рисуем всё
        win.fill(black)

        # тело змейки
        for i in body:
            pygame.draw.rect(win, green, (i[0], i[1], s, s))

        # еда
        fx, fy = food["pos"]
        pygame.draw.rect(win, food["color"], (fx, fy, s, s))

        # интерфейс
        txt(f'Очки: {sc}   Уровень: {lvl}', 10, 10)

        pygame.display.update()
        clk.tick(spd)


if __name__ == '__main__':
    main()
