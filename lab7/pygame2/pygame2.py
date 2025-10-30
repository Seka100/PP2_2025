import pygame
import sys

pygame.init()
s = pygame.display.set_mode((600, 300))
pygame.display.set_caption("Music")

playlist = ["1.mp3", "2.mp3", "3.mp3"]
c = 0

pygame.mixer.init()
pygame.mixer.music.load(playlist[c])

n = pygame.font.SysFont(None, 40)

def draw_text(text):
    s.fill((255, 255, 255))
    txt = n.render(text, True, (0, 0, 0))
    s.blit(txt, (60, 90))
    pygame.display.flip()

while True:
    draw_text(f"Playing: {playlist[c]}")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:  # play
                pygame.mixer.music.play()
            elif event.key == pygame.K_s:  # stop
                pygame.mixer.music.stop()
            elif event.key == pygame.K_n:  # next
                current = (c + 1) % len(playlist)
                pygame.mixer.music.load(playlist[c])
                pygame.mixer.music.play()
            elif event.key == pygame.K_b:  # back
                current = (c - 1) % len(playlist)
                pygame.mixer.music.load(playlist[c])
                pygame.mixer.music.play()
