import pygame
import sys

TILE_SIZE = 64
WINDOW_SIZE = 10 * TILE_SIZE
pygame.init()

screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("War Zone")
sand = pygame.image.load("images/tileSand1.png")
sand_rect = sand.get_rect()
screen_rect = screen.get_rect()


num_tiles = screen_rect.width // sand_rect.width


def draw_background():
    for y in range(num_tiles):
        for x in range(num_tiles):
            screen.blit(sand, (x * sand_rect.width, y * sand_rect.height))

coordinate = (0,0)

clock = pygame.time.Clock()
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    draw_background()
    pygame.display.flip()
    clock.tick(60)

