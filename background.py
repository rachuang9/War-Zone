import pygame


SCREEN_WIDTH = 800
SCREEN_Height = int(SCREEN_WIDTH * 0.8)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_Height))
screen_rect = screen.get_rect()

GRAVITY = 0.55
TILE_SIZE = 40

# define colors
BG = (144, 201, 120)
RED = (255, 0, 0,)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# define font
font = pygame.font.SysFont('Futura', 30)

class Background:
    def draw_text(text, font, tet_col, x, y):
        img = font.render(text, True, tet_col)
        screen.blit(img, (x, y))


    def draw_bg():
        screen.fill(BG)
        pygame.draw.line(screen, RED, (0, 300), (SCREEN_WIDTH, 300))
        bg_img = pygame.image.load('images/background/city.png')

        tile_2 = pygame.image.load('images/tile/2.png')
        num_tiles = screen_rect.width // 40
        for x in range(num_tiles):
            screen.blit(tile_2, (x * 70, 300))

        screen.blit(bg_img, (0,1))
