import pygame
import random
import sys

pygame.init()

w = 600 #ширина 
h = 400 #высота 
s = 20  #размер 

black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 200, 0)
red = (200, 0, 0)

win = pygame.display.set_mode((w, h))
pygame.display.set_caption('Snake')

clk = pygame.time.Clock()
fnt = pygame.font.SysFont('arial', 24)

def rnd_food(body):  
    while True:
        x = random.randrange(0, w - s, s)
        y = random.randrange(0, h - s, s)
        if (x, y) not in body:
            return (x, y)

def txt(t, x, y):  
    win.blit(fnt.render(t, True, white), (x, y))

def over(sc):  #конец игры
    win.fill(black)
    t = fnt.render(f'Игра окончена! Счёт: {sc}', True, red)
    win.blit(t, (w//2 - t.get_width()//2, h//2))
    pygame.display.update()
    pygame.time.wait(2000)
    pygame.quit()
    sys.exit()

def main():
    body = [(100, 100), (80, 100), (60, 100)]  #начальное тело
    dir = 'RIGHT'#направление
    food = rnd_food(body)
    sc = 0#счёт
    lvl = 1#уровень
    spd = 10#скорость

    while True:
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

        x, y = body[0]
        if dir == 'UP': y -= s
        elif dir == 'DOWN': y += s
        elif dir == 'LEFT': x -= s
        elif dir == 'RIGHT': x += s
        head = (x, y)

        
        if x < 0 or x >= w or y < 0 or y >= h or head in body:
            over(sc)

        body.insert(0, head)

        if head == food:
            sc += 1
            food = rnd_food(body)
        else:
            body.pop()

        # уровни
        if sc and sc % 4 == 0:
            lvl = sc // 4 + 1
            spd = 10 + lvl * 2

        # рисуем всё
        win.fill(black)
        for i in body:
            pygame.draw.rect(win, green, (i[0], i[1], s, s))
        pygame.draw.rect(win, red, (food[0], food[1], s, s))
        txt(f'Очки: {sc}   Уровень: {lvl}', 10, 10)

        pygame.display.update()
        clk.tick(spd)

if __name__ == '__main__':
    main()

