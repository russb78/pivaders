#!/usr/bin/env python2

import pygame
import random

BLACK = [0, 0, 0]; BLUE = [0, 0, 255]; WHITE = [255, 255, 255]; RED = [255, 0, 0]
RESOLUTION = [800, 600]
GAME_OVER = False
ROW = 10; COLUMN = 4
ALIEN_WIDTH = 40; ALIEN_HEIGHT = 30; SPACER = 20

pygame.init() # Initialise Pygame 
font = pygame.font.SysFont("Arial", 18)
screen = pygame.display.set_mode([RESOLUTION[0], RESOLUTION[1]])
clock = pygame.time.Clock() # Initialise a clock to limit FPS

pygame.display.set_caption('Pivaders - Press ESC to quit')
pygame.mouse.set_visible(False) # We don't need the mouse so hide it

# Load the graphical images we're using.
background_image = pygame.image.load("Space-Background.jpg").convert()

score = 0; shot = 0

##### PLAYER CLASS #####
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) # Initialise the Sprite class
        self.image = pygame.image.load("ship.png").convert() #87 x 80 (image size)
        self.image.set_colorkey(BLACK)
        self.size = (87, 80) # size of the image
        self.rect = pygame.rect.Rect([(RESOLUTION[0] / 2) - (self.size[0] /2), (RESOLUTION[1] - 90)], self.size)
        self.vector = 0
        self.speed = 7 # how many pixels the player moves each update
        self.wait = 350 # time in milliseconds between shots
        self.time = pygame.time.get_ticks()

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

##### ALIENS CLASS & BULLETS & BARRIERS BUILDER CLASSES #####
class Alien(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) # Initialise Sprite class
        self.image = pygame.image.load("invader.png").convert() 
        self.image.set_colorkey(BLACK)
        self.size = (40, 30) # size of the image
        self.rect = self.image.get_rect()
        self.vector = [1, 1]
        self.moved = [0, 0] # iterated on as the sprite moves
        self.time = pygame.time.get_ticks()
        self.wait = 500 # time delay in milliseconds between movements
        self.distance = [(ALIEN_WIDTH / 4) + (SPACER / 4), SPACER]
  
    def update(self):
        if current_time - self.time > self.wait:
            if self.moved[0] < 12: # if the aliens haven't moved right...
                self.rect.x += self.vector[0] * self.distance[0]
                self.moved[0] +=1
            else:
                if not self.moved[1]: # if the aliens haven't moved down...
                    self.rect.y += self.vector[1] * self.distance[1]
                self.vector[0] *= -1 # reverse the vector
                self.moved = [0, 0]
                self.wait -= 25
            self.time = current_time

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
        if self.rect.y < 0 or self.rect.y > RESOLUTION[1]: # if the bullet goes off the screen, remove it from all groups
            self.kill()

#### FUNCTIONS TO CREATE BULLETS, MISSILES & BARRIERS ####
def make_bullet():
    bullet = Blocks(BLUE, 5, 15)
    bullet.rect.x = player.rect.x + 40
    bullet.rect.y = player.rect.y + 10
    bullet.vector = -1
    bullet.speed = 26
    bullet_list.add(bullet)
    all_sprite_list.add(bullet)

def make_missile():
    if len(alien_list) > 0:
        missile = Blocks(RED, 5, 5)
        alien = random.choice(list(alien_list))
        missile.rect.x = alien.rect.x + 15
        missile.rect.y = alien.rect.y + 40
        missile.vector = +1
        missile.speed = 10
        missile_list.add(missile)
        all_sprite_list.add(missile)

def make_barriers(barrier_spacer):
    for column in range(3):
        for row in range(9):
            barrier = Blocks(WHITE, 10, 10)
            barrier.rect.x = 55 + (200 * barrier_spacer) + (row * 10)
            barrier.rect.y = 425 + (column * 10)
            barrier_list.add(barrier)
            all_sprite_list.add(barrier)
        barrier_list.add(barrier)
        all_sprite_list.add(barrier)
    return barrier_list

#### CREATE GROUPS TO CONTROL COLLISSIONS AND DRAWING ####
alien_list = pygame.sprite.Group() # list of sprites (to help with management)
bullet_list = pygame.sprite.Group()
missile_list = pygame.sprite.Group()
barrier_list = pygame.sprite.Group()
all_sprite_list = pygame.sprite.Group() # list of everything (to help with management)

#### CREATE A PLAYER ####
player = Player()
all_sprite_list.add(player) 

#### CREATE A STANDARD SET OF BARRIERS ####
for spacing in range(4): # for four barriers
    make_barriers(spacing)
    spacing += 1

#### CREATE A STANDARD WAVE OF ALIENS ####
for column in range(COLUMN):
    for row in range(ROW):
        alien = Alien()
        alien.rect.y = SPACER + (column * (ALIEN_HEIGHT + SPACER))
        alien.rect.x = SPACER + (row * (ALIEN_WIDTH + SPACER))
        alien_list.add(alien) # add the aliens to the list we created just now
        all_sprite_list.add(alien) # and also add them to the overall list

###### MAIN GAME LOOP ######## 


while not GAME_OVER: 
    current_time = pygame.time.get_ticks()
    real_time = pygame.time.get_ticks()

    player.control() # control the player
    player.update() # move the player on screen

    for bullet in bullet_list:
        bullet.update() # move the bullets on screen

    for alien in alien_list:
        alien.update() # move the aliens on screen

    shoot =  random.randrange(100)
    if shoot in [1, 20, 40, 60, 80, 99]:
        make_missile()

    for missile in missile_list:
        missile.update()

    ######## SORT THROUGH THE COLLISSION LISTS #########

    for bullet in bullet_list: # see if a bullet has collided with an alien:
        bullet_hit_list = pygame.sprite.spritecollide(bullet, alien_list, True)
                               # see if a bullet has collided with a barrier:
        bullet_barrier_list = pygame.sprite.spritecollide(bullet, barrier_list, True)

        for alien in bullet_hit_list: # if so, kill the bullet (alien is auto killed)
            bullet.kill()
            shot += 1
            print "You've shot", shot, "alien(s)!"

        for barrier in bullet_barrier_list: # if so, kill the bullet (barrier is auto killed)
            bullet.kill()
            
    for missile in missile_list:
        missile_hit_list = pygame.sprite.spritecollide(player, missile_list, True)
        missile_barrier_list = pygame.sprite.spritecollide(missile, barrier_list, True)

        for missile in missile_hit_list:
            #player.kill() --- THIS WILL NEED TO HAPPEN!
            score += 1
            print "You've been shot! Arggg!"

        for barrier in missile_barrier_list:
            missile.kill()

    # see if the player has collided with an alien
    alien_hit_list = pygame.sprite.spritecollide(player, alien_list, True)

    # check the list of collisions between player and aliens to see if a life has been lost:
    if len(alien_hit_list) > 0:
        score += 1
        print "Oops - you're dead!"
    
    if len(alien_list) < 1:
        print "You Win!"
    # Update the background then the players' position on the screen
    screen.blit(background_image, [0, 0])
    # draw the sprite list to the screen
    screen.blit(font.render("fps: " + str(clock.get_fps()), 1, WHITE), (0,0))
    all_sprite_list.draw(screen) # draw all actors with a single draw command!
    pygame.display.flip() # Refresh the screen
    clock.tick(20) # Force frame-rate to desired figure

pygame.quit () # Game quits gracefully when 'game_over' turns True