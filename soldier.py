import pygame
import os
import settings
import random
from bullets import Bullet
from grenade import Grenade
from pygame import mixer
mixer.init()
bullet_noise = pygame.mixer.Sound('shot.mp3')
bullet_noise.set_volume(.04)

class Soldier(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed, ammo, num_grenades):
        super().__init__()
        self.moving_left = False
        self.moving_right = False
        self.shooting = False
        self.alive = True
        self.char_type = char_type
        self.speed = speed
        self.ammo = ammo
        self.start_ammo = ammo
        self.shoot_cooldown = 0
        self.num_grenades = num_grenades
        self.throwing_grenade = False
        self.grenade_thrown = False
        self.health = 100
        self.max_health = self.health
        self.direction = 1
        self.vel_y = 0
        self.jump = False
        self.in_air = True
        self.flip = False
        self.action = 0
        self.animation_list = []
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        # create ai specific varaibles
        self.move_counter = 0
        # self.vision = pygame.Rect(0, 0, 150, 20)
        # idling is random occurance
        self.idling = False
        self.idling_counter = 0

        animation_types = ['stand', 'walk', 'jump', 'fall']
        for animation in animation_types:
            temp_list = []
            num_of_frames = len(os.listdir(f'images/{self.char_type}/{animation}'))
            for i in range(num_of_frames):
                img = pygame.image.load(f'images/{self.char_type}/{animation}/{i}.png').convert_alpha()
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self, bullet_group, grenade_group):
        if self.in_air:
            self.update_action(2)  # make it jump
        elif self.moving_left or self.moving_right:
            self.update_action(1)  # make it walk
        else:
            self.update_action(0)  # make it stand

        self.update_animation()
        self.check_alive()
        self.move()

        # update cooldown
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        if self.shooting:
            self.shoot(bullet_group)
        if self.throwing_grenade and self.num_grenades > 0:
            self.throw_grenade(grenade_group)
            self.throwing_grenade = False


    def move(self):
        # reset movement variables
        dx = 0
        dy = 0
        # assign movement variables
        if self.moving_left:
            dx = -self.speed


        elif self.moving_right:
            dx = self.speed

        else:
            dx = 0  # don't move, neither is true

        if self.moving_left and self.moving_right:
            print(f"{self.char_type} wierd! both are true")

        if self.jump and not self.in_air:
            self.vel_y = -11
            self.jump = False
            self.in_air = True
        # giving the parabolic shape of the gravity

        self.vel_y += settings.GRAVITY
        dy += self.vel_y

        # check collison with floor (boundaries with floor)
        if self.rect.bottom + dy > 300:
            dy = 300 - self.rect.bottom
            self.in_air = False

        self.rect.x += dx
        self.rect.y += dy
        if self.rect.x <= 0:
            self.rect.x = 0
        if self.rect.right >= settings.SCREEN_WIDTH:
            self.rect.x = settings.SCREEN_WIDTH

    def shoot(self, bullet_group):
        if self.shoot_cooldown == 0 and self.ammo > 0:
            self.shoot_cooldown = 20
            direction = 1
            if self.moving_left:
                direction = -1
            bullet = Bullet(self.rect.centerx + (0.75 * self.rect.size[0] * direction),
                            self.rect.centery,
                            direction)
            bullet_group.add(bullet)
            # when it shoots it will reduce by 1
            self.ammo -= 1
            #recieved assistance from Riley Haugen
            if self.shoot:
                bullet_noise.play()


    def throw_grenade(self, grenade_group):
        self.grenade_thrown = True
        self.num_grenades -= 1
        grenade = Grenade(self.rect.centerx + (0.5 * self.rect.size[0] * self.direction),
                          self.rect.top,
                          self.direction)
        grenade_group.add(grenade)

    def ai(self, player, bullet_group):  # making zombies move by itself

        if self.alive and player.alive:
            if self.idling == False and random.randint(1, 200) == 1:
                self.update_action(0)
                self.idling = True
                self.idling_counter = 50
            # check if the ai is near the player
            if self.rect.colliderect(player.rect):
                # stop running and face the player
                self.update_action(0)
                self.shoot(bullet_group)

            else:
                if self.idling == False:
                    self.move()
                    # added boundaries for the zombies
                    if self.rect.right >= (settings.SCREEN_WIDTH - 15):
                        self.moving_left = True
                        self.moving_right = False
                    if self.rect.left <= 2:
                        self.moving_right = True
                        self.moving_left = False
                    self.update_action(1)  # 1: run
                    self.move_counter += 1
                else:
                    self.idling_counter -= 1
                    if self.idling_counter <= 0:
                        self.idling = False

    def update_animation(self):
        # time animation to move the picture

        ANIMATION_COOLDOWN = 100
        # update image depending on current frame
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0

    def update_action(self, new_action):
        # helps check if the new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
            # update the aniamation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.update_action(3)

    def draw(self, screen):
        screen.blit(pygame.transform.flip(self.image, self.moving_left, False), self.rect)
