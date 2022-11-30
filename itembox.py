import pygame
import settings
from random import randint


class ItemBox(pygame.sprite.Sprite):
    def __init__(self, item_type):
        super().__init__()

        if item_type == 'Health':
            self.image = pygame.image.load('images/icons/healthcrate.png').convert_alpha()
        elif item_type == 'Ammo':
            self.image = pygame.image.load('images/icons/ammocrate.png').convert_alpha()
        elif item_type == 'Grenade':
            self.image = pygame.image.load('images/icons/ammocrate.png').convert_alpha()
        else:
            print(f"unsupported item type! {item_type}")
        self.item_type = item_type
        self.rect = self.image.get_rect()
        self.rect.centerx = randint(0, settings.SCREEN_WIDTH)
        self.rect.bottom = 300

    def update(self, player):
        # check if the player has picked up the box
        if pygame.sprite.collide_rect(self, player):
            # check what kind of box it was
            if self.item_type == 'Health':
                player.health += 25
                if player.health > player.max_health:
                    player.health = player.max_health
            elif self.item_type == 'Ammo':
                player.ammo += 15
            elif self.item_type == 'Grenade':
                player.num_grenades += 3
            # delete the item box
            self.kill()
