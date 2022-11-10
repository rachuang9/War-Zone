import pygame

class Character:
    def __init__(self, ai_game):
        self.screen = ai_game
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        self.image = pygame.image.load("../player/tank_huge.png")
        self.rect = self.image.get_rect()
        self.rect.left = self.screen_rect.left
        self.x = float(self.rect.x)
        self.moving_right = False
        self.moving_left = False