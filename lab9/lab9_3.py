import pygame
import sys

pygame.init()

# окно
width, height = 800, 500
win = pygame.display.set_mode((width, height))
pygame.display.set_caption('simple paint')

# цвета
white = (245, 245, 245)
black = (20, 20, 20)
red = (230, 50, 70)
green = (60, 200, 80)
blue = (60, 120, 230)
yellow = (255, 220, 70)
purple = (150, 80, 200)

# параметры инструмента
current_color = black
brush_size = 5
tool = 'brush'
font = pygame.font.SysFont('arial', 20)

# панель интерфейса
def draw_ui():
    pygame.draw.rect(win, (210, 210, 210), (0, 0, width, 40))
    info = font.render(f'инструмент: {tool}   цвет: {current_color}', True, black)
    win.blit(info, (10, 10))


# выбор цвета по клавише
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


# рисование квадрата
def draw_square(pos1, pos2, color):
    x1, y1 = pos1
    x2, y2 = pos2

    side = min(abs(x2 - x1), abs(y2 - y1))
    if x2 < x1: side = -side

    pygame.draw.rect(win, color, (x1, y1, side, side), 2)


# прямоугольный треугольник
def draw_right_triangle(pos1, pos2, color):
    x1, y1 = pos1
    x2, y2 = pos2

    p1 = pos1
    p2 = (x2, y1)
    p3 = pos2

    pygame.draw.polygon(win, color, [p1, p2, p3], 2)


# равносторонний треугольник
def draw_equilateral_triangle(pos1, pos2, color):
    x1, y1 = pos1
    x2, y2 = pos2

    side = abs(x2 - x1)

    # три вершины равностороннего треугольника
    p1 = (x1, y1)
    p2 = (x1 + side, y1)
    height_tri = int((3 ** 0.5) / 2 * side)
    p3 = (x1 + side // 2, y1 - height_tri)

    pygame.draw.polygon(win, color, [p1, p2, p3], 2)


# ромб
def draw_rhombus(pos1, pos2, color):
    x1, y1 = pos1
    x2, y2 = pos2

    cx = (x1 + x2) // 2
    cy = (y1 + y2) // 2

    p1 = (cx, y1)    # верх
    p2 = (x2, cy)    # право
    p3 = (cx, y2)    # низ
    p4 = (x1, cy)    # лево

    pygame.draw.polygon(win, color, [p1, p2, p3, p4], 2)


# основная функция
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

            # выбор инструментов
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_1: tool = 'brush'
                elif e.key == pygame.K_2: tool = 'rect'
                elif e.key == pygame.K_3: tool = 'circle'
                elif e.key == pygame.K_4: tool = 'eraser'
                elif e.key == pygame.K_5: tool = 'square'
                elif e.key == pygame.K_6: tool = 'right_triangle'
                elif e.key == pygame.K_7: tool = 'equilateral_triangle'
                elif e.key == pygame.K_8: tool = 'rhombus'

                color = get_color_key(e.key)
                if color: current_color = color

            # начало рисования мышью
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                drawing = True
                start_pos = last_pos = e.pos

            # окончание рисования
            if e.type == pygame.MOUSEBUTTONUP and e.button == 1:
                x1, y1 = start_pos
                x2, y2 = e.pos

                # фигуры рисуются по отпусканию мыши
                if tool == 'rect':
                    pygame.draw.rect(win, current_color, (x1, y1, x2 - x1, y2 - y1), 2)

                elif tool == 'circle':
                    r = int(((x2 - x1)**2 + (y2 - y1)**2)**0.5)
                    pygame.draw.circle(win, current_color, start_pos, r, 2)

                elif tool == 'square':
                    draw_square(start_pos, e.pos, current_color)

                elif tool == 'right_triangle':
                    draw_right_triangle(start_pos, e.pos, current_color)

                elif tool == 'equilateral_triangle':
                    draw_equilateral_triangle(start_pos, e.pos, current_color)

                elif tool == 'rhombus':
                    draw_rhombus(start_pos, e.pos, current_color)

                drawing = False

            # кисть,ластик
            if e.type == pygame.MOUSEMOTION and drawing:
                if tool == 'brush':
                    pygame.draw.line(win, current_color, last_pos, e.pos, brush_size)
                elif tool == 'eraser':
                    pygame.draw.line(win, white, last_pos, e.pos, brush_size * 2)
                last_pos = e.pos

        draw_ui()
        pygame.display.update()


if __name__ == '__main__':
    main()
