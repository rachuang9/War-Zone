import pygame
import settings
from soldier import Soldier
from random import randint



#images of the box
health_box_img = pygame.image.load('images/icons/healthcrate.png').convert_alpha()
ammo_box_img = pygame.image.load('images/icons/ammocrate.png').convert_alpha()
grenade_box_img = pygame.image.load('images/icons/ammocrate.png').convert_alpha()

item_boxes = {
    'Health': health_box_img,
    'Ammo': ammo_box_img,
    'Grenade': grenade_box_img

}

player = Soldier('player', 200, 200, 0.6, 5, 20, 5)

class ItemBox(pygame.sprite.Sprite):
    def __init__(self, item_type, x, y):
        super().__init__()
        self.item_type = item_type
        self.image = item_boxes[self.item_type]
        self.rect = self.image.get_rect()
        self.rect.midtop = randint(x + settings.TILE_SIZE // 2, y + settings.TILE_SIZE - self.image.get_height())


    def update(self):
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

