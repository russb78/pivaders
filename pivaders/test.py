#!/usr/bin/env python2

# This is the dev branch

import pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RES = (800, 600)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) 
        self.size = (61, 60)
        self.rect = self.image.get_rect()
        self.rect.x = (RES[0] / 2) - (self.size[0] / 2)
        self.rect.y = 520
        self.travel = 7
        self.speed = 350
        self.time = pygame.time.get_ticks()
        self.vector = 0
    
    def update(self):
        self.rect.x += self.vector * self.travel
        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.x > RES[0] - self.size[0]:
            self.rect.x = RES[0] - self.size[0]

class Game(object):
    def __init__(self):
        pygame.init()
        pygame.font.init()
        pygame.mixer.init()
        self.clock = pygame.time.Clock()
        self.game_font = pygame.font.Font(
        'data/Orbitracer.ttf', 28)
        self.screen = pygame.display.set_mode([RES[0], RES[1]])
        self.time = pygame.time.get_ticks()
        self.refresh_rate = 20
        self.background = pygame.image.load(
        'data/graphics/Space-Background-5.jpg').convert()
        pygame.display.set_caption('Pivaders - ESC to exit')
        pygame.mouse.set_visible(False) 
        self.end_game = False

        self.ship_sheet = pygame.image.load(
        'data/graphics/ship_sheet_new.png').convert()
        self.ship_sheet.set_colorkey(BLACK)
        Player.image = self.ship_sheet.subsurface(5*61, 0, 61, 60)
        self.animate_right = False
        self.animate_left = False
        self.ani_pos = 5 # 11 images of ship leaning from left to right. 5th image is 'central'
        self.explosion_sheet = pygame.image.load(
        'data/graphics/explosion_new1.png').convert_alpha()
        self.explosion_image = self.explosion_sheet.subsurface(0, 0, 79, 96)
        self.alien_explosion_sheet = pygame.image.load(
        'data/graphics/alien_explosion.png')
        self.alien_explosion = self.alien_explosion_sheet.subsurface(0, 0, 94, 96)
        self.explode = False
        self.explode_pos = 0
        pygame.mixer.music.load('data/sound/10_Arpanauts.ogg')
        pygame.mixer.music.play(-1) #play song on an ifinite loop
        self.bullet_fx = pygame.mixer.Sound(
        'data/sound/medetix__pc-bitcrushed-lazer-beam.ogg')
        self.explosion_fx = pygame.mixer.Sound(
        'data/sound/timgormly__8-bit-explosion.ogg')

    def control(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.end_game = True
            if event.type == pygame.KEYDOWN \
            and event.key == pygame.K_ESCAPE:
                self.end_game = True
        self.keys = pygame.key.get_pressed()
        if self.keys[pygame.K_LEFT]:
            self.player.vector = -1
            self.animate_left = True
            self.animate_right = False
        elif self.keys[pygame.K_RIGHT]:
            self.player.vector = 1
            self.animate_right = True
            self.animate_left = False
        elif self.keys[pygame.K_SPACE]:
            self.explosion_fx.play()
            self.explode = True
            self.bullet_fx.play()

        else:
            self.player.vector = 0
            self.animate_right = False
            self.animate_left = False

    def animate_player(self):
        if self.animate_right:
            if self.ani_pos < 10:
                self.player.image = self.ship_sheet.subsurface(self.ani_pos*61, 0, 61, 60)
                self.ani_pos += 1
        else:
            if self.ani_pos > 5:
                self.ani_pos -= 1
                self.player.image = self.ship_sheet.subsurface(self.ani_pos*61, 0, 61, 60)

        if self.animate_left:
            if self.ani_pos > 0:
                self.ani_pos -= 1
                self.player.image = self.ship_sheet.subsurface(self.ani_pos*61, 0, 61, 60)
        else:
            if self.ani_pos < 5:
                self.player.image = self.ship_sheet.subsurface(self.ani_pos*61, 0, 61, 60)
                self.ani_pos += 1

    def explosion(self):
        # 66w 97h
        if self.explode:
            if self.explode_pos < 9:
                self.alien_explosion = self.alien_explosion_sheet.subsurface(0, self.explode_pos*96, 94, 96)
                self.explode_pos += 1
                self.screen.blit(self.alien_explosion, [self.player.rect.x -8, self.player.rect.y - 15])
                """if self.explode_pos < 8:
                self.explosion_image = self.explosion_sheet.subsurface(0, self.explode_pos*96, 79, 96)
                self.explode_pos += 1
                self.screen.blit(self.explosion_image, [self.player.rect.x -8, self.player.rect.y - 15])"""
            else:
                self.explode = False
                self.explode_pos = 0

    def refresh_screen(self):
        self.screen.blit(self.background, [0, 0])
        self.screen.blit(self.player.image, [self.player.rect.x, self.player.rect.y])
        self.explosion() #This must come after the player has been blitted
        pygame.display.flip() 
        self.clock.tick(self.refresh_rate)

    def main_loop(self):
        self.player = Player()
        while not self.end_game:
            self.control()
            self.player.update()
            self.animate_player() #This must come before refresh screen
            self.refresh_screen()
        pygame.quit()

if __name__ == '__main__':
    pv = Game()
    pv.main_loop()