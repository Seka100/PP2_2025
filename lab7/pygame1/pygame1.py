import pygame
import math
import datetime
import sys

pygame.init()
screen = pygame.display.set_mode((1000, 1000))
pygame.display.set_caption("Mickey Clock")

clock = pygame.time.Clock()

mickey = pygame.image.load("base_micky.jpg").convert_alpha()
minute = pygame.image.load("minute.png").convert_alpha()
second = pygame.image.load("second.png").convert_alpha()

center = (500, 500)

while True:
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((255, 255, 255))

    screen.blit(mickey, (100, 50))

    n= datetime.datetime.now()
    minutes = n.minute
    seconds = n.second

    minute_a= -((minutes / 60) * 360) + 90
    second_a = -((seconds / 60) * 360) + 90

    _min = pygame.transform.rotate(minute, minute_a)
    _sec = pygame.transform.rotate(second, second_a)

    rect_m = _min.get_rect(center=center)
    rect_s= _sec.get_rect(center=center)

    screen.blit(_min, rect_m)
    screen.blit(_sec, rect_s)

    pygame.display.flip()
    clock.tick(30)
