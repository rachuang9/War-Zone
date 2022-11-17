import pygame

class Character:
    def __init__(self, ai_game):
        self.screen = ai_game
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        self.image = pygame.image.load("../player/walk/1.png")
        self.rect = self.image.get_rect()
        self.rect.left = self.screen_rect.left
        self.x = float(self.rect.x)
        self.moving_right = False
        self.moving_left = False

    def update(self):
        if self.moving_right and self.rect.right < self.screen.right:
            self.x += self.settings.character_speed
        if self.moving_left and self.rect.left > 0:
            self.x += self.settings.character_speed

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def center_character(self):
        self.rect.left = self.screen_rect.left
        self.x - float(self.rect.x)