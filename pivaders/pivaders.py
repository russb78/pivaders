#!/usr/bin/env python2

import pygame, random, os

pygame.init() # Initialise Pygame 
pygame.font.init()

BLACK = [0, 0, 0]; BLUE = [0, 0, 255]; WHITE = [255, 255, 255]; RED = [255, 0, 0]
RESOLUTION = [800, 600]
GAME_OVER = False
ROW = 10; COLUMN = 4
ALIEN_WIDTH = 30; ALIEN_HEIGHT = 40; SPACER = 20

game_font = pygame.font.Font(os.path.join('data', 'Orbitracer.ttf'), 28)
# From http://openfontlibrary.org courtesy of www.chrisdesign.wordpress.com
start_font = pygame.font.Font(os.path.join('data', 'Orbitracer.ttf'), 72)
screen = pygame.display.set_mode([RESOLUTION[0], RESOLUTION[1]])
clock = pygame.time.Clock() # Initialise a clock to limit FPS

at_start_screen = True

pygame.display.set_caption('Pivaders - Press ESC to quit')
pygame.mouse.set_visible(False) # We don't need the mouse so hide it
# Load the graphical images we're using for the background
# courtesy of http://opengameart.org/users/rawdanitsu:  
bg = pygame.image.load(
    os.path.join('data', 'Space-Background.jpg')).convert()
sc = pygame.image.load(
    os.path.join('data', 'start_screen.jpg')).convert()
#### CREATE GROUPS TO HOUSE SEPERATE GROUPS OF ACTORS ####
alien_group = pygame.sprite.Group() 
bullet_group = pygame.sprite.Group()
missle_group = pygame.sprite.Group()
barrier_group = pygame.sprite.Group()

#### GROUP TO ENCOMPASS ALL ACTORS ####
all_sprite_list = pygame.sprite.Group() 

##### PLAYER CLASS #####
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) # Initialise the Sprite class
        self.image = pygame.image.load(
            os.path.join("data", "ship.png")).convert() 
        self.image.set_colorkey(BLACK)
        self.size = (60, 55) # size of the image NEED TO GET RID OF THIS.
        self.rect = self.image.get_rect()
        self.rect.x = (RESOLUTION[0] / 2) - 30; self.rect.y = 510 #pygame.rect.Rect([430, 510], self.size)
        self.vector = 0
        self.speed = 7 # how many pixels the player moves each update
        self.wait = 350 # time in milliseconds between shots
        self.time = pygame.time.get_ticks()
        self.lives = 2
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
        global GAME_OVER, control_time, at_start_screen
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                GAME_OVER = True # Quit if window close button is pressed
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                at_start_screen = True
        self.keys = pygame.key.get_pressed()
        if self.keys[pygame.K_LEFT]:
            player.vector = -1
        elif self.keys[pygame.K_RIGHT]:
            player.vector = 1
        else:
            player.vector = 0 
        if self.keys[pygame.K_SPACE]:
            if control_time - self.time > self.wait:
                make_bullet()
                self.time = control_time

##### ALIEN CLASS #####
class Alien(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) # Initialise Sprite class
        #Credit: Skorpio & Wubitog http://opengameart.org/content/3-spaceships
        self.image = pygame.image.load(
            os.path.join("data", "Spaceship16.png")).convert() 
        self.image.set_colorkey(WHITE)
        self.size = (30, 40) # size of the image
        self.rect = self.image.get_rect()
        self.vector = [1, 1]
        self.moved = [0, 0] # iterated on as the sprite moves
        self.time = pygame.time.get_ticks()
        self.wait = 600 # time delay in milliseconds between movements
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
                if self.wait <= 100:
                    self.wait = 100
            self.time = current_time


class Bullet(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        pygame.sprite.Sprite.__init__(self) 
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect() 
        self.vector = -1
        self.speed = 26

    def update(self):
        self.rect.y += self.vector * self.speed
        if self.rect.y < 0 or self.rect.y > RESOLUTION[1]:
            self.kill()

class Missile(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        pygame.sprite.Sprite.__init__(self) 
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect() 
        self.vector = +1
        self.speed = 9

    def update(self):
        self.rect.y += self.vector * self.speed
        if self.rect.y < 0 or self.rect.y > RESOLUTION[1]:
            self.kill()

#### GENERIC BLOCK CLASS ### used to make bullets, missiles and barriers  
class Barrier(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        pygame.sprite.Sprite.__init__(self) 
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect() 

#### FUNCTIONS TO CREATE BULLETS, MISSILES & BARRIERS ####
def make_bullet():
    bullet = Bullet(BLUE, 5, 15)
    bullet.rect.x = player.rect.x + 30
    bullet.rect.y = player.rect.y + 10
    bullet_group.add(bullet)
    all_sprite_list.add(bullet)

def make_missile(alien, missile_speed):
    shoot = random.randrange(50)
    if shoot in [16, 33, 49]:
        missile = Missile(RED, 5, 5)
        missile.rect.x = alien.rect.x + 15
        missile.rect.y = alien.rect.y + 40
        missile.speed += missile_speed
        missle_group.add(missile)
        all_sprite_list.add(missile)
        print "Missile speed:", missile.speed
        
def make_barrier(columns, rows, barrier_spacer):
    for column in range(columns):
        for row in range(rows):
            barrier = Barrier(WHITE, 10, 10)
            barrier.rect.x = 55 + (200 * barrier_spacer) + (row * 10)
            barrier.rect.y = 450 + (column * 10)
            barrier_group.add(barrier)
            all_sprite_list.add(barrier)

def defenses_breached():
    for alien in alien_group:
        if alien.rect.y > 405:
            screen.blit(game_font.render(
            "The aliens have breached our defenses!", 1, RED), (250, 10))
            draw_screen()
            pygame.time.delay(2000)
            return True

def kill_all():
    for items in [
    bullet_group, missle_group, alien_group, barrier_group]:
        for i in items:
                i.kill()
    player.kill()

def is_dead():
    if player.lives < 0:
        screen.blit(game_font.render(
        "Game Over! You scored: " + str(player.score), 1, RED), (275, 10))
        draw_screen()
        pygame.time.delay(2000)
        return True

def win_round():
    if len(alien_group) < 1 and at_start_screen == False:
        screen.blit(game_font.render(
        "You won the round!", 1, RED), (325, 10))
        return True

#### FUCTION TO CREATE A WAVE OF ALIENS ####
def make_aliens(speed):
    for column in range(COLUMN):
        for row in range(ROW):
            alien = Alien()
            alien.rect.y = 55 + (column * (ALIEN_HEIGHT + SPACER))
            alien.rect.x = SPACER + (row * (ALIEN_WIDTH + SPACER))
            alien_group.add(alien) # add the aliens to the list we created just now
            all_sprite_list.add(alien) # and also add them to the overall list
            alien.wait -= speed
        print "Alien speed: ", alien.wait

#### FUNCTION TO CREATE A SET OF BARRIERS ####
def make_defenses():
    for spacing, spacing in enumerate(xrange(4)):
        make_barrier(3, 9, spacing)

def start_screen():
    global GAME_OVER, at_start_screen 
    while at_start_screen:
        kill_all()
        screen.blit(sc, [0, 0])
        screen.blit(start_font.render(
        "PIVADERS", 1, WHITE), (265, 120))
        screen.blit(game_font.render(
            "PRESS SPACE TO PLAY", 1, WHITE), (274, 191))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                GAME_OVER = True # Quit if window close button is pressed
                at_start_screen = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                GAME_OVER = True
                at_start_screen = False
                kill_all()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                at_start_screen = False
                main_loop()
### DRAW ALL ACTORS ###
def draw_screen():
    all_sprite_list.draw(screen) # draw all the sprites in one go
    screen.blit(game_font.render(
        "SCORE " + str(player.score), 1, WHITE), (12, 10))
    screen.blit(game_font.render(
        "LIVES " + str(player.lives + 1), 1, RED), (355, 570))
    #screen.blit(game_font.render(
        #"FPS: " + str(clock.get_fps()), 1, WHITE), (10, 45))
    pygame.display.flip() # refresh the screen
    screen.blit(bg, [0, 0]) # clear the screen
    clock.tick(20) # Force frame-rate to desired number

###### MAIN GAME LOOP ######## 
def main_loop():
    global GAME_OVER, current_time, control_time, at_start_screen, player
    
    level_up = 100; missile_speed = 1
    player = Player()
    all_sprite_list.add(player)

    make_aliens(0)
    make_defenses() 

    while not GAME_OVER: # keep going until GAME_OVER turns True
        if at_start_screen:
            start_screen()

        current_time = pygame.time.get_ticks()
        control_time = pygame.time.get_ticks()

        #### UPDATE THE POSITIONS OF ALL ACTORS ####
        player.control() # control the player
        player.update()

        for item in [alien_group, bullet_group, missle_group]:
            for i in item:
                i.update()

        if len(alien_group): # if there are aliens on screen...
            shooter = random.choice([alien for alien in alien_group])
            make_missile(shooter, missile_speed) # ...pick a random alien and have them shoot

        ######## SORT THROUGH THE COLLISSION LISTS #########
        for bullet in bullet_group: # see if a bullet has collided with an alien:
            bullet_hit_list = pygame.sprite.spritecollide(
                bullet, alien_group, True)
            # see if a bullet has collided with a barrier:
            bullet_barrier_group = pygame.sprite.spritecollide(
                bullet, barrier_group, True)

            for alien in bullet_hit_list: # iterate over the aliens
                bullet.kill()
                player.score += 10

            for barrier in bullet_barrier_group: # iterate over the barriers
                bullet.kill()

        for missile in missle_group: # then do the same with the missiles
            missile_hit_list = pygame.sprite.spritecollide(
                player, missle_group, True)
            missile_barrier_group = pygame.sprite.spritecollide(
                missile, barrier_group, True)

            for missile in missile_hit_list:
                player.lives -= 1

            for barrier in missile_barrier_group:
                missile.kill()

        #### ITERATE OVER GAMEOVER CONDITIONS & DRAW SCREEN ####
        if defenses_breached() or is_dead():
            at_start_screen = True

        if win_round():
            draw_screen()
            pygame.time.wait(2000)
            make_aliens(level_up)
            make_defenses()
            missile_speed += 1
            level_up += 100
        draw_screen()

    pygame.quit()

if __name__ == '__main__':
    main_loop()
