import pygame

TILE_SIZE = 64
WINDOW_SIZE = 10 * TILE_SIZE
clock = pygame.time.Clock()
FPS = 60
pygame.init()

screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("War Zone")
sand = pygame.image.load("images/tileSand1.png")
sand_rect = sand.get_rect()
screen_rect = screen.get_rect()

num_tiles = screen_rect.width // sand_rect.width

class Background:
    def __init__(self):
        self.image = pygame.image.load('images/background.png')
        self.rect = self.image.get_rect()
        self.rect.top = self.screen_rect.top
    def draw_background(self):
        



#def draw_background():
    #for y in range(num_tiles):
        #for x in range(num_tiles):
            #screen.blit(sand, (x * sand_rect.width, y * sand_rect.height))


