import pygame
import os

pygame.init()

SCREEN_WIDTH = 800
SCREEN_Height = int(SCREEN_WIDTH * 0.8)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_Height))
pygame.display.set_caption('War Zone')

# set frame rate
clock = pygame.time.Clock()
FPS = 60

# define game varaibles

GRAVITY = 0.55

# load images:
bullet_img = pygame.image.load('images/icons/bullet.png').convert_alpha()
# define player action variables:

moving_left = False
moving_right = False
shoot = False

# define colors
BG = (144, 201, 120)
RED = (255, 0, 0,)


def draw_bg():
    screen.fill(BG)
    pygame.draw.line(screen, RED, (0, 300), (SCREEN_WIDTH, 300))


class Soldiers(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed, ammo):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.char_type = char_type
        self.speed = speed
        self.ammo = ammo
        self.start_ammo = ammo
        self.shoot_cooldown = 0
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
    def update(self):
        self.update_animation()
        self.check_alive()
        #update cooldown
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    def move(self, moving_left, moving_right):
        # reset movement variables
        dx = 0
        dy = 0

        # assign movement variables
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
        # giving the parabolic shape of the gravity

        self.vel_y += GRAVITY
        if self.vel_y > 5:
            self.vel_y
        dy += self.vel_y

        # check collison with floor
        if self.rect.bottom + dy > 300:
            dy = 300 - self.rect.bottom
            self.in_air = False

        self.rect.x += dx
        self.rect.y += dy

    def shoot(self):
        if self.shoot_cooldown == 0 and self.ammo > 0:
            self.shoot_cooldown = 20
            bullet = Bullet(self.rect.centerx + (0.6 * self.rect.size[0] * self.direction), self.rect.centery,self.direction)
            bullet_group.add(bullet)
            #when it shoots it will reduce by 1
            self.ammo -= 1

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

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
        if pygame.sprite.spritecollide(player, bullet_group, False):
            if player.alive:
                self.kill()


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction
    def update(self):
        #move bullet
        self.rect.x += (self.direction * self.speed)
        if self.rect.right <0 or self.rect.left > SCREEN_WIDTH - 100 :
             self.kill()

        if pygame.sprite.spritecollide(player, bullet_group, False):
            if player.alive:
                player.health -= 5
                self.kill()
        if pygame.sprite.spritecollide(enemy, bullet_group, False):
            if enemy.alive:
                enemy.health -= 25
                self.kill()



# create sprite groups

bullet_group = pygame.sprite.Group()


player = Soldiers('player', 200, 200, 1, 5, 20)
enemy = Soldiers('enemy', 400, 200, 1, 5, 20)
run = True
while run:

    clock.tick(FPS)
    draw_bg()
    player.update()
    player.draw()

    enemy.update()
    enemy.draw()
    #update and draw groups

    bullet_group.update()
    bullet_group.draw(screen)

    # update player actions
    if player.alive:
        if shoot:
            player.shoot()
        if player.in_air:
            player.update_action(2)  # make it jump
        elif moving_left or moving_right:
            player.update_action(1)  # make it walk
        else:
            player.update_action(0)  # make it stand

    player.move(moving_left, moving_right)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                moving_left = True
            if event.key == pygame.K_RIGHT:
                moving_right = True
            if event.key == pygame.K_SPACE:
                shoot = True
            if event.key == pygame.K_UP and player.alive:
                player.jump = True
            if event.key == pygame.K_ESCAPE:
                run = False

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                moving_left = False
            if event.key == pygame.K_RIGHT:
                moving_right = False
            if event.key == pygame.K_SPACE:
                shoot = False

    pygame.display.update()

pygame.quit()
