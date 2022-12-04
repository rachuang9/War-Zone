import pygame
import settings
from soldier import Soldier
from healthbar import HealthBar
from itembox import ItemBox
from random import randint, choice
from pygame import mixer
import gameover
import buttons

mixer.init()
pygame.init()

mixer.music.load('instinct.mp3')
mixer.music.set_volume(1)
mixer.music.play()

SCREEN_Height = int(settings.SCREEN_WIDTH * 0.8)

screen = pygame.display.set_mode((settings.SCREEN_WIDTH, SCREEN_Height))
screen_rect = screen.get_rect()
pygame.display.set_caption('War Zone')

# set frame rate
clock = pygame.time.Clock()

# define player action variables:

shoot = False
grenade = False
grenade_thrown = False
clicked = False
start_game = False
start_intro = False

player = Soldier('player', 200, 200, 0.6, 5, 20, 5)
# define font
font = pygame.font.SysFont('Futura', 30)

#loading the images for the buttons
start_img = pygame.image.load('images/button_start.png')
exit_img = pygame.image.load('images/button_exit.png')
instruction_img = pygame.image.load('images/button_instruction.png')
Mainmenu_title = pygame.image.load('images/war-zone.png').convert_alpha()


def draw_text(text, font, tet_col, x, y):
    img = font.render(text, True, tet_col)
    screen.blit(img, (x, y))


def draw_bg():
    screen.fill(settings.BG)
    bg_img = pygame.image.load('images/background/city.png')
    tile_2 = pygame.image.load('images/tile/2.png')
    num_tiles = screen_rect.width // 40
    for x in range(num_tiles):
        screen.blit(tile_2, (x * 70, 300))

    screen.blit(bg_img, (0, 1))


# create sprite group

enemy_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
grenade_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()
itembox_group = pygame.sprite.Group()

# create item boxes randomly

for i in range(randint(2, 5)):
    itembox = ItemBox(choice(['Health', 'Ammo', 'Grenade']))
    itembox_group.add(itembox)

#
enemy = Soldier('enemy', 500, 200, 0.6, 1.5, 20, 0)
enemy.moving_right = True
enemy.moving_left = False

enemy2 = Soldier('enemy', 600, 200, 0.6, 1.5, 20, 0)
enemy2.moving_left = True
enemy2.moving_right = False

enemy_group.add(enemy2)
enemy_group.add(enemy)
health_bar = HealthBar(10, 10, player.health, player.health)

# creating the button giving the width, height, image and the scale
start_button = buttons.Button(settings.SCREEN_WIDTH // 2 - 60, SCREEN_Height // 2 - 20, start_img, .6)
exit_button = buttons.Button(settings.SCREEN_WIDTH // 2 - 60, SCREEN_Height // 2 + 60, exit_img, .6)
instruction_button = buttons.Button(settings.SCREEN_WIDTH // 3 + 66, SCREEN_Height // 2.5 - 30, instruction_img, .6)

run = True
mouse_pressed = False
while run:

    # check for user input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.moving_left = True
            if event.key == pygame.K_RIGHT:
                player.moving_right = True

            if event.key == pygame.K_SPACE:
                player.shooting = True
            if event.key == pygame.K_UP and player.alive:
                player.jump = True
            if event.key == pygame.K_ESCAPE:
                run = False

        # assume we aren't throwing a grenade this frame
        player.throwing_grenade = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            # oops, we are, the mouse was clicked
            player.throwing_grenade = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player.moving_left = False
            if event.key == pygame.K_RIGHT:
                player.moving_right = False
            if event.key == pygame.K_SPACE:
                player.shooting = False

    # making the main menu
    if start_game == False:
        screen.fill(settings.BG)
        screen.blit(Mainmenu_title, (290, 100))
        if start_button.draw(screen):
            start_game = True
            start_intro = True
        if exit_button.draw(screen):
            run = False
        if instruction_button.draw(screen): #cannot click on button to show the message
            text = font.render('Instructions: Using the left and right keys to move left and right'
                               'Use the upper arrow key to jump. Use the space bar to shoot bullet. Click on the '
                               'mouse to launch grenades', True, settings.RED, settings.BLUE)
            textRect = text.get_rect()
            textRect.center = (settings.SCREEN_WIDTH // 2, SCREEN_Height // 2)




    else:
        draw_bg()
        draw_text(f'Ammo:{player.ammo} ', font, settings.WHITE, 10, 35)
        draw_text('Grenade: ', font, settings.WHITE, 10, 60)
        # shows grenades in pictures rather than in numbers
        for x in range(player.num_grenades):
            screen.blit(pygame.image.load('images/icons/grenade.png').convert_alpha(),
                        (110 + (x * 13), 55))

        if randint(0, 5000) < 10:
            itembox_group.add(ItemBox('Ammo'))
            itembox_group.add(ItemBox('Health'))
            itembox_group.add(ItemBox('Grenade'))

        # update game objects
        bullet_group.update()
        grenade_group.update(player, explosion_group, enemy_group)
        explosion_group.update()
        itembox_group.update(player)
        player.update(bullet_group, grenade_group)

        for enemy in enemy_group:
            enemy.ai(player, bullet_group)
            enemy.update(bullet_group, 0)

        # draw the game screen

        health_bar.draw(player.health, screen)
        player.draw(screen)
        enemy_group.draw(screen)
        bullet_group.draw(screen)
        grenade_group.draw(screen)
        explosion_group.draw(screen)
        itembox_group.draw(screen)

    pygame.display.flip()
    clock.tick(settings.FPS)

    # once collide with player, player will lose their life
    #fix to display message and make a restart button along with it
    if pygame.sprite.spritecollide(player, bullet_group, True):
        if player.alive:
            player.health -= 10
        if player.alive == 0:
            run = False
            win = True
            gameover.end.display_lose_message()

    # once the enemy is collided with the bullet of a num_grenades it will die
    for enemy in enemy_group:
        if pygame.sprite.spritecollide(enemy, bullet_group, True):
            if enemy.alive:
                enemy.health -= 25
            if enemy.alive == 0:
                run = False
                win = False
                gameover.end.display_win_message()

pygame.quit()
