#!/usr/bin/env python2

import pygame
import random

BLACK = [0, 0, 0]; BLUE = [0, 0, 255]; WHITE = [255, 255, 255]; RED = [255, 0, 0]
RESOLUTION = [800, 600]
GAME_OVER = False
ROW = 10; COLUMN = 4
ALIEN_WIDTH = 30; ALIEN_HEIGHT = 40; SPACER = 20

pygame.init() # Initialise Pygame 
font = pygame.font.SysFont("Arial", 22)
screen = pygame.display.set_mode([RESOLUTION[0], RESOLUTION[1]])
clock = pygame.time.Clock() # Initialise a clock to limit FPS

pygame.display.set_caption('Pivaders - Press ESC to quit')
pygame.mouse.set_visible(False) # We don't need the mouse so hide it
# Load the graphical images we're using for the background
# courtesy of http://opengameart.org/users/rawdanitsu:  
background_image = pygame.image.load("Space-Background.jpg").convert()

#### CREATE GROUPS TO CONTROL COLLISSIONS ####
alien_list = pygame.sprite.Group() 
bullet_list = pygame.sprite.Group()
missile_list = pygame.sprite.Group()
barrier_list = pygame.sprite.Group()

#### GROUP TO CONTROL DRAWING OF ALL ACTORS ####
all_sprite_list = pygame.sprite.Group() 

##### PLAYER CLASS #####
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) # Initialise the Sprite class
        self.image = pygame.image.load("ship.png").convert() 
        self.image.set_colorkey(BLACK)
        self.size = (60, 55) # size of the image
        #self.rect = self.image.get_rect() - need to ditch self.size when possible...
        self.rect = pygame.rect.Rect([(RESOLUTION[0] / 2) - (self.size[0] /2), (RESOLUTION[1] - 90)], self.size)
        self.vector = 0
        self.speed = 7 # how many pixels the player moves each update
        self.wait = 350 # time in milliseconds between shots
        self.time = pygame.time.get_ticks()
        self.lives = 3
        self.score = 0
        self.defenses_breached = False

    def update(self):
        # stop the player from leaving either side of the screen
        self.rect.x += self.vector * self.speed
        if self.rect.x > RESOLUTION[0] - self.size[0]:
            self.rect.x = RESOLUTION[0] - self.size[0]
        elif self.rect.x < 0:
            self.rect.x = 0

    def control(self):
        global GAME_OVER, real_time
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                GAME_OVER = True # Quit if window close button is pressed
        self.keys = pygame.key.get_pressed()
        if self.keys[pygame.K_ESCAPE]:
            GAME_OVER = True
        if self.keys[pygame.K_LEFT]:
            player.vector = -1
        elif self.keys[pygame.K_RIGHT]:
            player.vector = 1
        else:
            player.vector = 0 
        if self.keys[pygame.K_SPACE]:
            if real_time - self.time > self.wait:
                make_bullet()
                self.time = real_time

player = Player()
all_sprite_list.add(player)

##### ALIEN CLASS #####
class Alien(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) # Initialise Sprite class
        #Credit: Skorpio & Wubitog http://opengameart.org/content/3-spaceships
        self.image = pygame.image.load("Spaceship16.png").convert() 
        self.image.set_colorkey(WHITE)
        self.size = (30, 40) # size of the image
        self.rect = self.image.get_rect()
        self.vector = [1, 1]
        self.moved = [0, 0] # iterated on as the sprite moves
        self.time = pygame.time.get_ticks()
        self.wait = 500 # time delay in milliseconds between movements
        self.travel = [(self.size[0] - 7), SPACER]

    def update(self):
        if current_time - self.time > self.wait:
            if self.moved[0] < 12: # if the aliens haven't moved right...
                self.rect.x += self.vector[0] * self.travel[0]
                self.moved[0] +=1
            else:
                if not self.moved[1]: # if the aliens haven't moved down...
                    self.rect.y += self.vector[1] * self.travel[1]
                self.vector[0] *= -1 # reverse the vector
                self.moved = [0, 0]
                self.wait -= 20
            self.time = current_time

#### GENERIC BLOCK CLASS ### used to make bullets, missiles and barriers  
class Blocks(pygame.sprite.Sprite): # This class handles bullets, missiles and barriers
    def __init__(self, color, width, height):
        pygame.sprite.Sprite.__init__(self) 
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect() 
        self.vector = 0
        self.speed = 0

    def update(self):
        self.rect.y += self.vector * self.speed
        if self.rect.y < 0 or self.rect.y > RESOLUTION[1]:
            self.kill()

#### FUNCTIONS TO CREATE BULLETS, MISSILES & BARRIERS ####
def make_bullet():
    bullet = Blocks(BLUE, 5, 15)
    bullet.rect.x = player.rect.x + (player.size[0] / 2)
    bullet.rect.y = player.rect.y + 10
    bullet.vector = -1
    bullet.speed = 26
    bullet_list.add(bullet)
    all_sprite_list.add(bullet)

def make_missile(alien):
    shoot = random.randrange(50)
    if shoot in [16, 33, 49]:
        missile = Blocks(RED, 5, 5)
        missile.rect.x = alien.rect.x + 15
        missile.rect.y = alien.rect.y + 40
        missile.vector = +1
        missile.speed = 10
        missile_list.add(missile)
        all_sprite_list.add(missile)

def make_barrier(columns, rows, barrier_spacer):
    for column in range(columns):
        for row in range(rows):
            barrier = Blocks(WHITE, 10, 10)
            barrier.rect.x = 55 + (200 * barrier_spacer) + (row * 10)
            barrier.rect.y = 450 + (column * 10)
            barrier_list.add(barrier)
            all_sprite_list.add(barrier)

def draw_screen():
    all_sprite_list.draw(screen) # draw all the sprites in one go
    screen.blit(font.render("SCORE: " + str(player.score), 1, WHITE), (10, 5))
    screen.blit(font.render("LIVES: " + str(player.lives), 1, WHITE), (10, 25))
    screen.blit(font.render("FPS: " + str(clock.get_fps()), 1, WHITE), (10, 45))
    pygame.display.flip() # refresh the screen
    screen.blit(background_image, [0, 0]) # clear the screen
    clock.tick(20) # Force frame-rate to desired number

def is_game_over():
    global GAME_OVER

    if player.lives < 0:
        screen.blit(font.render("Game Over! You scored: " + str(player.score), 1, RED), (275, 10))
        GAME_OVER = True

    elif player.defenses_breached:
        screen.blit(font.render("The aliens have breached our defenses!", 1, RED), (250, 10)) 
        GAME_OVER = True

    elif len(alien_list) < 1:
        screen.blit(font.render("You Win!", 1, RED), (275, 10))
        GAME_OVER = True
    return GAME_OVER

#### FUCTION TO CREATE A WAVE OF ALIENS ####
def make_aliens():
    for column in range(COLUMN):
        for row in range(ROW):
            alien = Alien()
            alien.rect.y = 55 + (column * (ALIEN_HEIGHT + SPACER))
            alien.rect.x = SPACER + (row * (ALIEN_WIDTH + SPACER))
            alien_list.add(alien) # add the aliens to the list we created just now
            all_sprite_list.add(alien) # and also add them to the overall list

#### FUNCTION TO CREATE A SET OF BARRIERS ####
def make_defenses():
    for spacing, spacing in enumerate(xrange(4)):
        make_barrier(2, 9, spacing)

###### MAIN GAME LOOP ######## 
def main_loop():
    global GAME_OVER, current_time, real_time

    make_aliens()
    make_defenses()

    while not GAME_OVER: # keep going until GAME_OVER turns True

        current_time = pygame.time.get_ticks()
        real_time = pygame.time.get_ticks()

        #### UPDATE THE POSITIONS OF ALL ACTORS ####
        player.control() # control the player
        player.update() # move the player on screen

        for alien in alien_list:
            alien.update() # move the aliens on screen
            if alien.rect.y > 405:
                player.defenses_breached = True

        if len(alien_list): # if there are aliens on screen:
            shooter = random.choice([alien for alien in alien_list])
            make_missile(shooter) # pick a random alien and have them shoot

        for missile in missile_list:
            missile.update()

        for bullet in bullet_list:
            bullet.update()
            
        ######## SORT THROUGH THE COLLISSION LISTS #########
        for bullet in bullet_list: # see if a bullet has collided with an alien:
            bullet_hit_list = pygame.sprite.spritecollide(bullet, alien_list, True)
                                   # see if a bullet has collided with a barrier:
            bullet_barrier_list = pygame.sprite.spritecollide(bullet, barrier_list, True)

            for alien in bullet_hit_list: # iterate over the aliens
                bullet.kill()
                player.score += 10

            for barrier in bullet_barrier_list: # iterate over the barriers
                bullet.kill()

        for missile in missile_list: # then do the same with the missiles
            missile_hit_list = pygame.sprite.spritecollide(player, missile_list, True)
            missile_barrier_list = pygame.sprite.spritecollide(missile, barrier_list, True)

            for missile in missile_hit_list:
                player.lives -= 1

            for barrier in missile_barrier_list:
                missile.kill()

        #### ITERATE OVER GAMEOVER CONDITIONS & DRAW SCREEN ####
        is_game_over()
        draw_screen()

    pygame.time.wait(2500) # give people time to see the 'game over message'
    pygame.quit () # Game quits gracefully when 'game_over' is True

main_loop()