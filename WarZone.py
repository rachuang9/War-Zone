import pygame
import sys
import os
import random
import buttons
from pygame import mixer
import csv

# from character import Character
# from buttons import Button
# from background import Background, screen
# from settings import Settings


pygame.init()

SCREEN_WIDTH = 600
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("War Zone")

clock = pygame.time.Clock()
FPS = 60

bg_scroll = 0
GRAVITY = 0.75
SCROLL_THRESH = 200
ROWS = 16
COLS = 150
TILE_SIZE = 64
TILE_TYPES = 21
MAX_LEVEL = 2
screen_scroll = 0
level = 1
start_game = False
start_intro = False
moving_left = False
moving_right = False
shoot = False
grenade = False
grenade_thrown = False

# background

sand_img = pygame.image.load("images/background/city.png")
city_img = pygame.image.load('images/background/sand.png')

img_list = []

for x in range(TILE_TYPES):
    img = pygame.image.load(f"img/Tile {x}.png")
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img_list.append(img)

bullet_img = pygame.image.load('img/icons/bullet.png').convert_alpha()
grenade_img = pygame.image.load('img/icons/grenade.png').convert_alpha()
healthcrate_img = pygame.image.load('img/icons/health.png').convert_alpha()
ammocrate_img = pygame.image.load('img/icons/ammocrate.png').convert_alpha()

item_box = {
    'Health': healthcrate_img,
    'Ammo': ammocrate_img
}


def draw_background():
    screen.fill(255, 255, 255)
    width = city_img.get_width()
    for x in range(5):
        screen.blit(sand_img, ((x * width) - bg_scroll * 0.5, 0))
        screen.blit(city_img, ((x * width) - bg_scroll * 0.5, 0))


def reset_level():
    enemy_group.empty()
    bullet_group.empty()
    grenade_group.empty()
    explosion_group.empty()
    item_box_group.empty()
    decoration_group.empty()
    water_group.empty()
    exit_group.empty()

    data = []
    for row in range(ROWS):
        r = [-1] * COLS
        data.append(r)
    return data



class Solider(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.char_type = char_type
        self.speed = speed
        self.ammo = ammo
        self.start_ammo = ammo
        self.shoot_cooldown = 0
        self.gernades = gernades
        self.health = 100
        self.max_health = self.health
        self.direction = 1
        self.vel_y = 0
        self.flip = False
        self.jump = False
        self.in_air = True
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        self.move_counter = 0
        self.vision = pygame.Rect(0, 0, 250, 20)
        self.idling = False
        self.idling_counter = 0

        animation_types = ['walk', 'fall', 'jump']
        for animation in animation_types:
            temp_list = []
            num_of_frames = len(os.listdir(f'images/{self.char_type}/{animation}'))
            for i in range(num_of_frames):
                img = pygame.image.load(f'images/{self.char_type}/{animation}/{i}.png')
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
                self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def update(self):
        self.update_animations()
        self.check_alive()

        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    def move(self, moving_left, moving_right):

        screen_scroll = 0
        dx = 0
        dy = 0
        if moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
        if moving_right:
            dx = self.speed
            self.flip = False
            self.direction = 1

        if self.jump == True and self.in_air == False:
            self.vel_y = -11
            self.jump = False
            self.in_air = True

        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y
            dy += self.vel_y
        for tile in obstacle_list:
            if tile [1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
                if self.char_type == 'enemy':
                self.direction *= -1
                self.move_counter = 0
            #adding collision to pygame
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].top - self.rect.bottom
            elif self.vel_y >= 0:
                self.vel_y = 0
                self.in_air = False
                dy = tile[1].top - self.rect.bottom
        if pygame.sprite.spritecollide(self, water_group, False):
            self.health = 0

        level_complete = False
        if pygame.sprite.spritecollide(self, exit_group, False):
            level_complete = True

        if self.rect.bottom > SCREEN_HEIGHT:
            self.health = 0

        if self.char_type == 'player':
            if self.rect.left + dx < 0 or self.rect.right + dx > SCREEN_WIDTH:
                dx = 0
        self.rect.x += dx
        self.rect.y += dy
        

        #if self.rect.bottom + dy > 300:
            #dy = 300 - self.rect.bottom
            #self.in_air = False



    def update_animations(self):

        ANIMATION_COOLDOWN = 100
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0

    def update_action(self, new_action):
        if new_action != self.action:
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)


player = Solider('player', 200, 200, 3, 5)
enemy = Solider('enemy', 400, 200, 3, 5)

run = True
while run:
    clock.tick(FPS)

    # draw_background()

    player.update_animations()
    player.draw()
    enemy.draw()
    moving_left = False
    moving_right = False
    if player.alive:
        if player.in_air:
            player.update_action(0)
        elif moving_left or moving_right:
            player.update_action(0)
        else:
            player.update_action(1)
        player.move(moving_left, moving_right)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_w and player.alive:
                player.jump = True
            if event.key == pygame.K_ESCAPE:
                run = False
        if event.type == pygame.KEYUP:
            if event.type == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False
    pygame.display.flip()
    pygame.display.update()
pygame.quit()
