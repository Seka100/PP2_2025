import pygame
import sys

pygame.init()

#настройки окна
width, height = 800, 500
win = pygame.display.set_mode((width, height))
pygame.display.set_caption('simple paint')

#цвета
white = (245, 245, 245)
black = (20, 20, 20)
red = (230, 50, 70)
green = (60, 200, 80)
blue = (60, 120, 230)
yellow = (255, 220, 70)
purple = (150, 80, 200)

#параметры
current_color = black
brush_size = 5
tool = 'brush'
font = pygame.font.SysFont('arial', 20)

#функция интерфейса
def draw_ui():
    pygame.draw.rect(win, (210, 210, 210), (0, 0, width, 40))  #панель сверху
    info = font.render(f'инструмент: {tool}   цвет: {current_color}', True, black)
    win.blit(info, (10, 10))

#получение цвета по клавише
def get_color_key(key):
    return {
        pygame.K_r: red,
        pygame.K_g: green,
        pygame.K_b: blue,
        pygame.K_y: yellow,
        pygame.K_p: purple,
        pygame.K_k: black,
        pygame.K_w: white
    }.get(key, None)

#главная функция
def main():
    global current_color, tool
    win.fill(white)
    drawing = False
    start_pos = last_pos = None

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            #нажатие клавиши
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_1: tool = 'brush'   #кисть
                elif e.key == pygame.K_2: tool = 'rect'  #прямоугольник
                elif e.key == pygame.K_3: tool = 'circle'#круг
                elif e.key == pygame.K_4: tool = 'eraser'#ластик
                color = get_color_key(e.key)
                if color: current_color = color

            #нажатие мыши
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                drawing = True
                start_pos = last_pos = e.pos

            #отпускание мыши
            if e.type == pygame.MOUSEBUTTONUP and e.button == 1:
                if tool in ('rect', 'circle'):
                    x1, y1 = start_pos
                    x2, y2 = e.pos
                    if tool == 'rect':
                        pygame.draw.rect(win, current_color, (x1, y1, x2 - x1, y2 - y1), 2)
                    else:
                        radius = int(((x2 - x1)**2 + (y2 - y1)**2)**0.5)
                        pygame.draw.circle(win, current_color, start_pos, radius, 2)
                drawing = False

            #движение мыши при рисовании
            if e.type == pygame.MOUSEMOTION and drawing:
                if tool == 'brush':
                    pygame.draw.line(win, current_color, last_pos, e.pos, brush_size)
                elif tool == 'eraser':
                    pygame.draw.line(win, white, last_pos, e.pos, brush_size * 2)
                last_pos = e.pos

        draw_ui()
        pygame.display.update()

#запуск
if __name__ == '__main__':
    main()
