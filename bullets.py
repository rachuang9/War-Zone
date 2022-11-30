import pygame
import settings


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.speed = 10
        self.image = pygame.image.load('images/icons/bullet.png').convert_alpha()
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction

    def update(self):
        # move bullet
        self.rect.x += (self.direction * self.speed)
        if self.rect.right < 0 or self.rect.left > settings.SCREEN_WIDTH - 100:
            self.kill()
