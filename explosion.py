import pygame
import settings
from pygame import mixer

mixer.init()
explosion_noise = pygame.mixer.Sound('sound/explosion.mp3')
explosion_noise.set_volume(.07)


class Explosion(pygame.sprite.Sprite):
    # init the screen with the animation of the explosion once a grenade has been launched
    def __init__(self, x, y, scale):
        super().__init__()
        self.images = []
        for num in range(1, 11):
            img = pygame.image.load(f'images/explosion/{num}.png').convert_alpha()
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            self.images.append(img)
        self.frame_index = 0
        self.image = self.images[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0

    def update(self):

        # update explosion animation
        self.counter += 1
        if self.counter >= settings.EXPLOSION_SPEED:
            self.counter = 0
            self.frame_index += 1
            explosion_noise.play()
            # if the animation is complete then delete it
            if self.frame_index >= len(self.images):
                self.kill()

            else:
                self.image = self.images[self.frame_index]
