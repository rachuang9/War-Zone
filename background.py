import pygame
from settings import Settings
TILE_SIZE = 64
WINDOW_SIZE = 10 * TILE_SIZE
clock = pygame.time.Clock()
FPS = 60
pygame.init()

screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("War Zone")
sand = pygame.image.load("images/tileSand1.png")
view = pygame.image.load('images/background.png')
sand_rect = sand.get_rect()
screen_rect = screen.get_rect()

num_tiles = screen_rect.width // sand_rect.width

class Background:
    def __init__(self):
        self.settings = Settings
        self.view = pygame.image.load('images/background.png')
        self.rect = self.view.get_rect()
        self.rect.top = self.screen_rect.top
        self.BG = (144,201,120)
    def draw_background(self):
        width = pygame.image.load('images/background.png')
        for y in range(num_tiles):
            for x in range(num_tiles):
                screen.blit(sand, (x * sand_rect.width, y * sand_rect.height))
        for x in range(5):
            screen.blit(self.veiw, ((x * width) - bg_scroll 0.5, 0))






