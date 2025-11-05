import pygame
import random
import sys

pygame.init()

w = 400   #ширина)
h = 600   #высота)
win = pygame.display.set_mode((w, h))   #создаём окно)
pygame.display.set_caption("Racer (stable colors)")  #заголовок) 

white = (255, 255, 255)   
gray = (60, 60, 60)        
red = (220, 50, 50)
yellow = (255, 220, 60)
blue = (60, 120, 230)

clk = pygame.time.Clock()     #таймер для FPS)
fnt = pygame.font.SysFont('Arial', 24)  #шрифт для текста)

pw = 40  #ширина игрока) 
ph = 80  #высота игрока)
px = w // 2 - pw // 2 #позиция игрока по х)
py = h - ph - 20  #позиция игрока по у)
pspd = 6  #скорость игрока)

ew = 40  #ширина врага)
eh = 80  #высота врага)
espd = 5 #скорость врага)
en = []  #список врагов)

cn = []  #список монет) 
csz = 20 #размер монеты) 
cspd = 4 #скорость падения монеты)
cc = 0   #счётчик собранных монет)

st = 0 #таймер появления врагов)
ct = 0 #таймер появления монет)

pclr = blue  #цвет игрока)

def col(x1, y1, w1, h1, x2, y2, w2, h2):  #проверка)
    return (x1 < x2 + w2 and x1 + w1 > x2 and y1 < y2 + h2 and y1 + h1 > y2)

run = True 

while run:
    clk.tick(60)        
    win.fill(gray)     

    for e in pygame.event.get():  
        if e.type == pygame.QUIT:  
            run = False

    k = pygame.key.get_pressed()  
    if k[pygame.K_LEFT] and px > 100:    
        px -= pspd
    if k[pygame.K_RIGHT] and px < w - 100 - pw:  
        px += pspd

    st += 1  #обновляем таймер врагов
    if st > 60:  #создаём нового врага раз 60 
        ex = random.randint(120, w - 120 - ew)  #координата врага по х
        en.append([ex, -eh, red])               #добавляем врага (красный)
        st = 0

    ct += 1  #обновляем таймер монет
    if ct > 90:  #создаём новую монету раз в 90
        cx = random.randint(120, w - 120 - csz)  #координата монеты по х
        cn.append([cx, -csz, yellow])            #добавляем монету (жёлтая)
        ct = 0

    for e in en:   #двигаем всех врагов вниз
        e[1] += espd
    en = [e for e in en if e[1] < h + 50]  #удаляем врагов, вышедших за экран

    for c in cn:   #двигаем монеты вниз
        c[1] += cspd
    cn = [c for c in cn if c[1] < h + 50]  #удаляем монеты за экраном

    #проверяем столкновения с врагами
    for e in en:
        if col(px, py, pw, ph, e[0], e[1], ew, eh):
            pygame.quit()
            sys.exit()

    new_cn = []  #новый список монет
    for c in cn:
        if col(px, py, pw, ph, c[0], c[1], csz, csz):  #если собрали монету
            cc += 1         #увеличиваем счётчик
        else:
            new_cn.append(c)
    cn = new_cn  #обновляем список монет

    #рисуем границы дороги
    pygame.draw.rect(win, white, (100, 0, 5, h))
    pygame.draw.rect(win, white, (w - 105, 0, 5, h))

    #рисуем игрока
    pygame.draw.rect(win, pclr, (px, py, pw, ph))

    #рисуем врагов
    for e in en:
        pygame.draw.rect(win, e[2], (e[0], e[1], ew, eh))

    #рисуем монеты
    for c in cn:
        pygame.draw.circle(win, c[2], (c[0] + csz // 2, c[1] + csz // 2), csz // 2)

    #выводим счёт
    txt = fnt.render(f"Coins: {cc}", True, white)
    win.blit(txt, (w - 130, 10))

    pygame.display.flip()  #обновляем экран

pygame.quit()  #выходим из игры

