import pygame
import settings




class HealthBar():
    def __init__(self, x, y, health, max_health):
        self.x = x
        self.y = y
        self.heath = health
        self.max_health = max_health

    def draw(self, health, screen):
        # updates with new health
        self.health = health
        # calculate the ratio so it updates the health
        ratio = self.health / self.max_health
        pygame.draw.rect(screen, settings.BLACK, (self.x - 2, self.y - 2, 154, 24))
        pygame.draw.rect(screen, settings.RED, (self.x, self.y, 150, 20))
        pygame.draw.rect(screen, settings.GREEN, (self.x, self.y, 150 * ratio, 20))
