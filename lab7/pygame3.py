import pygame
import sys

pygame.init()
width, height = 500, 500
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Red Ball")

clock = pygame.time.Clock()

x, y = width// 2, height// 2
r= 20
s = 15

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and y - r > 0:
        y -= s
    if keys[pygame.K_DOWN] and y + r < height:
        y += s
    if keys[pygame.K_LEFT] and x - r > 0:
        x -= s
    if keys[pygame.K_RIGHT] and x + r < width:
        x += s

    screen.fill((255, 255, 255))
    pygame.draw.circle(screen, (255, 0, 0), (x, y), r)

    pygame.display.flip()
    clock.tick(30)
