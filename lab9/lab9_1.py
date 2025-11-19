import pygame
import random
import sys

pygame.init()

# окно и основные параметры
w = 400
h = 600
win = pygame.display.set_mode((w, h))
pygame.display.set_caption("Racer")

white = (255, 255, 255)
gray = (60, 60, 60)
red = (220, 50, 50)
blue = (60, 120, 230)

clk = pygame.time.Clock()
fnt = pygame.font.SysFont('Arial', 24)

# параметры игрока
pw = 40
ph = 80
px = w // 2 - pw // 2
py = h - ph - 20
pspd = 6

# параметры врагов
ew = 40
eh = 80
espeed = 5
en = []

# параметры монет
csz = 22
cspeed = 4
cn = []
cc = 0  # количество собранных монет

# монеты разных типов
coin_types = [
    {"color": (200, 120, 20), "value": 1},  # бронза
    {"color": (230, 230, 230), "value": 2},  # серебро
    {"color": (255, 215, 0), "value": 3}     # золото
]

# ко сколько монетам увеличивать скорость врага
coins_for_level = 10
next_level_target = coins_for_level

# таймеры появления
st = 0
ct = 0

# простой коллайдер
def col(x1, y1, w1, h1, x2, y2, w2, h2):
    return (x1 < x2 + w2 and x1 + w1 > x2 and
            y1 < y2 + h2 and y1 + h1 > y2)


run = True

while run:
    clk.tick(60)
    win.fill(gray)

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            run = False

    # управление
    k = pygame.key.get_pressed()
    if k[pygame.K_LEFT] and px > 100:
        px -= pspd
    if k[pygame.K_RIGHT] and px < w - 100 - pw:
        px += pspd

    # появление врагов
    st += 1
    if st > 60:
        ex = random.randint(120, w - 120 - ew)
        en.append([ex, -eh, red])
        st = 0

    # появление монет разных типов
    ct += 1
    if ct > 90:
        cx = random.randint(120, w - 120 - csz)

        coin = random.choice(coin_types)     # случайный тип монеты
        coin_color = coin["color"]
        coin_value = coin["value"]

        # монета: x, y, цвет, ценность
        cn.append([cx, -csz, coin_color, coin_value])
        ct = 0

    # движение врагов
    for e in en:
        e[1] += espeed
    en = [e for e in en if e[1] < h + 50]

    # движение монет
    for c in cn:
        c[1] += cspeed
    cn = [c for c in cn if c[1] < h + 50]

    # проверяем столкновения с врагами
    for e in en:
        if col(px, py, pw, ph, e[0], e[1], ew, eh):
            pygame.quit()
            sys.exit()

    # проверяем сбор монет
    new_cn = []
    for c in cn:
        if col(px, py, pw, ph, c[0], c[1], csz, csz):
            cc += c[3]   # добавляем вес монеты
        else:
            new_cn.append(c)
    cn = new_cn

    # повышение сложности: ускоряем врагов
    if cc >= next_level_target:
        espeed += 1
        next_level_target += coins_for_level

    # рисуем разметку
    pygame.draw.rect(win, white, (100, 0, 5, h))
    pygame.draw.rect(win, white, (w - 105, 0, 5, h))

    # игрок
    pygame.draw.rect(win, blue, (px, py, pw, ph))

    # враги
    for e in en:
        pygame.draw.rect(win, e[2], (e[0], e[1], ew, eh))

    # монеты
    for c in cn:
        pygame.draw.circle(win, c[2], (c[0] + csz // 2, c[1] + csz // 2), csz // 2)

    # вывод счёта
    txt = fnt.render(f"Coins: {cc}", True, white)
    win.blit(txt, (w - 140, 10))

    pygame.display.flip()

pygame.quit()
