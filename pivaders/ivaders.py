#!/usr/bin/env python2

import pygame, random, os

### CONSTANTS ###
RES = [800, 600]
BLACK = [0, 0, 0]; BLUE = [0, 0, 255]; WHITE = [255, 255, 255]; RED = [255, 0, 0]
BARRIER_ROW = 10; BARRIER_COLUMN = 4
ALIEN_WIDTH = 40; ALIEN_HEIGHT = 30; ALIEN_SPACER = 20
PLAYER_HEIGHT = 60; PLAYER_WIDTH = 55


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) # Initialise the Sprite class
        self.image = pygame.image.load(
            os.path.join("data", "ship.png")).convert() 
        self.image.set_colorkey(BLACK)
        self.size = (60, 55)
        self.rect = self.image.get_rect()
        self.rect.x = (RES[0] / 2) - (self.size[0] / 2)
        self.rect.y = 510
        self.vector = 0
        self.travel = 7 # how many pixels the player moves each update
        self.speed = 350 # time in milliseconds between shots
        self.time = pygame.time.get_ticks()
        self.lives = 2


    def update(self):
        # stop the player from leaving either side of the screen
        self.rect.x += self.vector * self.travel
        if self.rect.x > RES[0] - self.size[0]:
            self.rect.x = RES[0] - self.size[0]
        elif self.rect.x < 0:
            self.rect.x = 0

    def control(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # app local GAME_OVER
                pass
            if event.type == pygame.KEYDOWN \
            and event.key == pygame.K_ESCAPE:
                # go to start screen
                pass

        self.keys = pygame.key.get_pressed()
        if self.keys[pygame.K_LEFT]:
            self.vector = -1 # set the vector heading left
        elif self.keys[pygame.K_RIGHT]:
            self.vector = 1 # set the vector heading right
        else:
            self.vector = 0 # if not left or right, then stop
        if self.keys[pygame.K_SPACE]:
            if event.type == pygame.KEYUP: # only shoot once the key is up!
                #if game.time - self.time > self.speed: << shouldn't need this
                #make_bullet()
                #self.time = game.time << or this
                pass


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
        self.has_moved = [0, 0] # iterated on as the sprite moves
        self.time = pygame.time.get_ticks()
        self.speed = 600 # time delay in milliseconds between movements
        self.travel = [(self.size[0] - 7), SPACER]

    def update(self):
        if game.time - self.time > self.speed:
            if self.has_moved[0] < 12: # if the aliens haven't has_moved right...
                self.rect.x += self.vector[0] * self.travel[0]
                self.has_moved[0] +=1
            else:
                if not self.has_moved[1]: # if the aliens haven't has_moved down...
                    self.rect.y += self.vector[1] * self.travel[1]
                self.vector[0] *= -1 # reverse the vector
                self.has_moved = [0, 0]
                
                self.speed -= 20
                if self.speed <= 100:
                    self.speed = 100
            self.time = game.time


class Ammo(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        pygame.sprite.Sprite.__init__(self) 
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect() 
        self.vector = 0
        self.speed = 0
        self.shoot = random.randrange(50)

    def update(self):
        self.rect.y += self.vector * self.speed
        if self.rect.y < 0 or self.rect.y > RES[1]:
            self.kill() # destroy if it exits the top or bottom of the screen


class Block(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        pygame.sprite.Sprite.__init__(self) 
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()


class Game(object):
    def __init__(self):
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption('Pivaders - Press ESC to quit')
        pygame.mouse.set_visible(False) # We don't need the mouse so hide it
        self.end_game = False
        self.goto_intro = True
        self.font = pygame.font.Font(os.path.join('data', 'Orbitracer.ttf'), 28)
        self.screen = pygame.display.set_mode([RES[0], RES[1]])
        self.clock = pygame.time.Clock() # Initialise a clock to limit FPS
        self.refresh_rate = 0
        # Load the graphical images we're using for the background
        # courtesy of http://opengameart.org/users/rawdanitsu:  
        self.intro_screen = pygame.image.load(
            os.path.join('data', 'start_screen.jpg')).convert()
        self.background = pygame.image.load(
            os.path.join('data', 'Space-Background.jpg')).convert()

    def splash_screen(self):
        while self.goto_intro:
            self.screen.blit(self.intro_screen, [0, 0])
            self.screen.blit(self.font.render(
            "PIVADERS", 1, WHITE), (265, 120))
            self.screen.blit(self.font.render(
                "PRESS SPACE TO PLAY", 1, WHITE), (274, 191))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.end_game = True # Quit if window close button is pressed
                    self.goto_intro = False

                if event.type == pygame.KEYDOWN: 
                    if event.key == pygame.K_ESCAPE:
                        self.end_game = True
                        self.goto_intro = False
                        self.kill_all()

                    elif event.key == pygame.K_SPACE:
                        self.goto_intro = False
                        self.game_loop()

    def refresh_screen(self, refresh_rate):
        """
        Draw everything to the screen. refresh_rate
        sets the FPS for the entire game
        """
        self.all_sprites.draw(screen) # draw all the sprites in one go
        self.refresh_scores(True)
        pygame.display.flip() # refresh the screen
        self.screen.blit(self.background, [0, 0]) # clear the screen
        self.clock.tick(refresh_rate) # Force frame-rate to desired number

    def refresh_scores(self, show_FPS = False):
        self.screen.blit(self.font.render(
            "SCORE " + str(player.score), 1, WHITE), (12, 10))
        self.screen.blit(self.font.render(
            "LIVES " + str(player.lives + 1), 1, RED), (355, 570))
        if show_FPS:
            self.screen.blit(self.font.render(
                "FPS: " + str(clock.get_fps()), 1, WHITE), (12, 45))

    def kill_all(self):
        """
        Clear the screen of all actors
        """
        pass

    def game_loop(self):
        """
        This is the main game loop of the game. 
        """
        pass

    def defenses_breached(self):
        """
        If alien touches either the player, a barrier 
        # or goes beyond end of screen it's game over.
        return True if any of these conditions are met.
        """
        pass


### app class variables 
    """
    quit_game, game_time, start_screen, defenses_breached, is_dead, 
    score, level_up (change alien speed & missile_speed / regularity) 
    """

### app class functions:
    """
    make_lazer, make_missile, 
    """

    # laser = 26 speed / -1 vector
    # missile = 10 speed / +1 vector
