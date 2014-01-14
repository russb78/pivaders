#!/usr/bin/env python2

import pygame, random, os

RES = [800, 600]
BLACK = [0, 0, 0]; BLUE = [0, 0, 255]; WHITE = [255, 255, 255]; RED = [255, 0, 0]
BARRIER_ROW = 10; BARRIER_COLUMN = 4; BARRIER_SPACER = 0
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
        self.score = 0

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
                pv.end_game = True
            if event.type == pygame.KEYDOWN \
            and event.key == pygame.K_ESCAPE:
                pv.goto_intro = True

        self.keys = pygame.key.get_pressed()
        if self.keys[pygame.K_LEFT]:
            self.vector = -1 # set the vector heading left
        elif self.keys[pygame.K_RIGHT]:
            self.vector = 1 # set the vector heading right
        else:
            self.vector = 0 # if not left or right, then stop
        if self.keys[pygame.K_SPACE]:
            #if event.type == pygame.KEYUP: # only shoot once the key is up!
                #if game.time - self.time > self.speed: << shouldn't need this
            Game.make_bullet()
                #self.time = game.time << or this


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
        self.travel = [(self.size[0] - 7), ALIEN_SPACER]

    def update(self):
        if pv.game_time - self.time > self.speed:
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
            self.time = pv.game_time


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
        self.clock = pygame.time.Clock()
        pygame.mouse.set_visible(False) # We don't need the mouse so hide it
        self.end_game = False
        self.goto_intro = True
        self.font = pygame.font.Font(os.path.join('data', 'Orbitracer.ttf'), 28)
        self.screen = pygame.display.set_mode([RES[0], RES[1]])
        # Initialise a clock to limit FPS
        self.game_time = pygame.time.get_ticks()
        self.control_time = pygame.time.get_ticks()
        self.refresh_rate = 30
        self.missile_booster = 1
        self.alien_group = pygame.sprite.Group()
        self.bullet_group = pygame.sprite.Group()
        self.missle_group = pygame.sprite.Group()
        self.barrier_group = pygame.sprite.Group()
        self.all_sprite_list = pygame.sprite.Group()
        # Load the graphical images we're using for the background
        # courtesy of http://opengameart.org/users/rawdanitsu:  
        self.intro_screen = pygame.image.load(
            os.path.join('data', 'start_screen.jpg')).convert()
        self.background = pygame.image.load(
            os.path.join('data', 'Space-Background.jpg')).convert()
        self.level_up = 100; missile_booster = 1

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
                        #self.kill_all()

                        return self.make_player(), self.make_defenses(), self.alien_wave(0)

    def make_player(self):
        self.player = Player()
        self.all_sprite_list.add(self.player)
        return self.player

    def refresh_screen(self):
        """
        Draw everything to the screen. refresh_rate
        sets the FPS for the entire game
        """
        self.all_sprite_list.draw(self.screen) # draw all the sprites in one go
        self.refresh_scores()
        pygame.display.flip() # refresh the screen
        self.screen.blit(self.background, [0, 0]) # clear the screen
        self.clock.tick(self.refresh_rate) # Force frame-rate to desired number

    def refresh_scores(self):
        self.screen.blit(self.font.render(
            "SCORE " + str(self.player.score), 1, WHITE), (12, 10))
        self.screen.blit(self.font.render(
            "LIVES " + str(self.player.lives + 1), 1, RED), (355, 570))
        self.screen.blit(self.font.render(
            "FPS: " + str(self.clock.get_fps()), 1, WHITE), (12, 45))

    def alien_wave(self, speed):
        for column in range(BARRIER_COLUMN):
            for row in range(BARRIER_ROW):
                alien = Alien()
                alien.rect.y = 55 + (column * (ALIEN_HEIGHT + ALIEN_SPACER))
                alien.rect.x = ALIEN_SPACER + (row * (ALIEN_WIDTH + ALIEN_SPACER))
                self.alien_group.add(alien) # add the aliens to the list we created just now
                self.all_sprite_list.add(alien) # and also add them to the overall list
                alien.speed -= speed
        return self.alien_group

    def make_bullet(self):
        bullet = Ammo(BLUE, 5, 15)
        bullet.rect.x = self.player.rect.x + 30
        bullet.rect.y = self.player.rect.y + 10
        self.bullet_group.add(bullet)
        self.all_sprite_list.add(bullet)
        return self.bullet_group

    def make_missile(self, alien, missile_booster):
        shoot = random.randrange(50)
        self.missile_booster = missile_booster
        if len(self.alien_group): # if there are aliens on screen...
            shooter = random.choice([alien for alien in self.alien_group])
            #make_missile(shooter, missile_booster)
        if shoot in [16, 33, 49]:
            missile = Ammo(RED, 5, 5)
            missile.rect.x = alien.rect.x + 15
            missile.rect.y = alien.rect.y + 40
            missile.speed += self.missile_booster
            self.missle_group.add(missile)
            self.all_sprite_list.add(missile)
            return self.missile_group

    def make_barrier(self, columns, rows, barrier_spacer):
        for column in range(columns):
            for row in range(rows):
                barrier = Block(WHITE, 10, 10)
                barrier.rect.x = 55 + (200 * barrier_spacer) + (row * 10)
                barrier.rect.y = 450 + (column * 10)
                self.barrier_group.add(barrier)
                self.all_sprite_list.add(barrier)
        return self.barrier_group

    def make_defenses(self):
        for spacing, spacing in enumerate(xrange(4)):
            self.make_barrier(3, 9, spacing)

    def kill_all(self):
        """
        Clear the screen of all actors
        """
        for items in [
        self.bullet_group, self.missle_group, self.alien_group, self.barrier_group]:
            for i in items:
                i.kill()
        self.player.kill()

    def is_dead(self):
        if player.lives < 0:
            screen.blit(game_font.render(
            "Game Over! You scored: " + str(player.score), 1, RED), (275, 10))
            self.refresh_screen()
            pygame.time.delay(2000)
            return True

    def win_round(self):
        if len(self.alien_group) < 1 and at_start_screen == False:
            screen.blit(game_font.render(
            "You won the round!", 1, RED), (325, 10))
            return True

    def defenses_breached(self):
        """
        If alien touches either the player, a barrier 
        # or goes beyond end of screen it's game over.
        return True if any of these conditions are met.
        """
        for alien in self.alien_group:
            if alien.rect.y > 405:
                screen.blit(game_font.render(
                "The aliens have breached our defenses!", 1, RED), (250, 10))
                self.refresh_screen()
                pygame.time.delay(2000)
                return True

    def main_loop(self):

        while not self.end_game:
            while not self.goto_intro:

                self.player.control()
                self.player.update()

                for alien in self.alien_group: # self.bullet_group, self.missle_group]:
                    alien.update()

                for missile in self.missile_group:
                    missile.update(missile)

                if len(alien_group): # if there are aliens on screen...
                    shooter = random.choice([alien for alien in self.alien_group])
                    self.make_missile(shooter, self.missile_booster)

                self.refresh_screen()
            self.splash_screen()
        pygame.quit()

pv = Game()
pv.main_loop()

### app class variables:
"""
    quit_game, game_time, start_screen, defenses_breached, is_dead, 
    score, level_up (change alien speed & missile_speed / regularity) 
"""

 