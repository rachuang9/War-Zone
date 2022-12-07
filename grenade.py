import pygame
import settings
from explosion import Explosion


class Grenade(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        # set the grenade timer
        self.timer = 100
        # sets the velocity for the grenade
        self.vel_y = -11
        self.speed = 7

        # loads the image
        self.image = pygame.image.load('images/icons/grenade.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction

    def update(self, player, explosion_group, enemy_group):
        self.vel_y += settings.GRAVITY
        dx = self.direction * self.speed
        dy = self.vel_y

        # collision with floor
        if self.rect.bottom + dy > 300:
            dy = 300 - self.rect.bottom
            self.speed = 0
        # check collision with walls
        if self.rect.left + dx < 0 or self.rect.right + dx > settings.SCREEN_WIDTH:
            self.direction *= -1
            dx = self.direction * self.speed
        # update num_grenades position
        self.rect.x += dx
        self.rect.y += dy

        # countdown timer so it won't shoot to many grenades at once
        self.timer -= 1
        if self.timer <= 0:
            self.kill()
            explosion = Explosion(self.rect.x, self.rect.y, 0.5)
            explosion_group.add(explosion)
            # do damage to the nearby
            if abs(self.rect.centerx - player.rect.centerx) < settings.TILE_SIZE * 2 and \
                    abs(self.rect.centery - player.rect.centery) < settings.TILE_SIZE * 2:
                player.health -= 50
            for enemy in enemy_group:
                if abs(self.rect.centerx - enemy.rect.centerx) < settings.TILE_SIZE * 2 and \
                        abs(self.rect.centery - enemy.rect.centery) < settings.TILE_SIZE * 2:
                    enemy.health -= 50
