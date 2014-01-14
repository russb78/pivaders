#!/usr/bin/env python2

import pygame, random, os

RES = [800, 600]; BARRIER_ROW = 10; BARRIER_COLUMN = 4
BLACK = [0, 0, 0]; BLUE = [0, 0, 255]; WHITE = [255, 255, 255]; RED = [255, 0, 0]
ALIEN_WIDTH = 30; ALIEN_HEIGHT = 40; ALIEN_SPACER = 20

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) 
        self.image = pygame.image.load(
            os.path.join("data", "ship.png")).convert() 
        self.image.set_colorkey(BLACK)
        self.size = (60, 55)
        self.rect = self.image.get_rect()
        self.rect.x = (RES[0] / 2) - (self.size[0] / 2)
        self.rect.y = 510
        self.vector = 0; self.travel = 7; self.speed = 350 
        self.time = pygame.time.get_ticks()
        self.shoot_bullet = False

    def update(self):
        self.rect.x += self.vector * self.travel
        if self.rect.x > RES[0] - self.size[0]:
            self.rect.x = RES[0] - self.size[0]
        elif self.rect.x < 0:
            self.rect.x = 0

    def control(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Game.end_game = True
            if event.type == pygame.KEYDOWN \
            and event.key == pygame.K_ESCAPE:
                Game.goto_intro = True
        self.keys = pygame.key.get_pressed()
        if self.keys[pygame.K_LEFT]:
            self.vector = -1 
        elif self.keys[pygame.K_RIGHT]:
            self.vector = 1 
        else:
            self.vector = 0 
        if self.keys[pygame.K_SPACE]:
            self.shoot_bullet = True

class Alien(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) 
        #Credit: Skorpio & Wubitog http://opengameart.org/content/3-spaceships
        self.image = pygame.image.load(
            os.path.join("data", "Spaceship16.png")).convert() 
        self.image.set_colorkey(WHITE)
        self.size = (30, 40) 
        self.rect = self.image.get_rect()
        self.vector = [1, 1]
        self.has_moved = [0, 0] 
        self.time = pygame.time.get_ticks()
        self.speed = 600 
        self.travel = [(self.size[0] - 7), ALIEN_SPACER]

    def update(self):
        if Game.alien_time - self.time > self.speed:
            if self.has_moved[0] < 12: 
                self.rect.x += self.vector[0] * self.travel[0]
                self.has_moved[0] +=1
            else:
                if not self.has_moved[1]: 
                    self.rect.y += self.vector[1] * self.travel[1]
                self.vector[0] *= -1 # reverse the vector
                self.has_moved = [0, 0]
                self.speed -= 20
                if self.speed <= 100:
                    self.speed = 100
            self.time = Game.alien_time


class Ammo(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        pygame.sprite.Sprite.__init__(self) 
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect() 
        self.vector = 0; self.speed = 0
        self.shoot = random.randrange(50)

    def update(self):
        self.rect.y += self.vector * self.speed
        if self.rect.y < 0 or self.rect.y > RES[1]:
            self.kill()


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
        pygame.mouse.set_visible(False) 
        self.font = pygame.font.Font(os.path.join('data', 'Orbitracer.ttf'), 28)
        self.screen = pygame.display.set_mode([RES[0], RES[1]])
        self.time = pygame.time.get_ticks()
        self.refresh_rate = 20
        self.missile_booster = 1; self.level_up = 100
        self.score = 0; self.lives = 2
        self.player_group = pygame.sprite.Group()
        self.alien_group = pygame.sprite.Group()
        self.bullet_group = pygame.sprite.Group()
        self.missile_group = pygame.sprite.Group()
        self.barrier_group = pygame.sprite.Group()
        self.all_sprite_list = pygame.sprite.Group()
        # Load the graphical images we're using for the background
        # courtesy of http://opengameart.org/users/rawdanitsu:  
        self.intro_screen = pygame.image.load(
            os.path.join('data', 'start_screen.jpg')).convert()
        self.background = pygame.image.load(
            os.path.join('data', 'Space-Background.jpg')).convert()
        Game.end_game = False; Game.goto_intro = True

    def splash_screen(self):
        while Game.goto_intro:
            self.kill_all()
            self.screen.blit(self.intro_screen, [0, 0])
            self.screen.blit(self.font.render(
            "PIVADERS", 1, WHITE), (265, 120))
            self.screen.blit(self.font.render(
                "PRESS SPACE TO PLAY", 1, WHITE), (274, 191))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    Game.end_game = True # Quit if window close button is pressed
                    Game.goto_intro = False
                if event.type == pygame.KEYDOWN: 
                    if event.key == pygame.K_ESCAPE:
                        Game.end_game = True
                        Game.goto_intro = False
                        self.kill_all()
                    elif event.key == pygame.K_SPACE:
                        Game.goto_intro = False
                        self.lives = 2; self.score = 0
                        self.make_player()
                        self.make_defenses()
                        self.alien_wave(0)

    def make_player(self):
        self.player = Player()
        self.player_group.add(self.player)
        self.all_sprite_list.add(self.player)

    def refresh_screen(self):
        self.all_sprite_list.draw(self.screen) 
        self.refresh_scores()
        pygame.display.flip() 
        self.screen.blit(self.background, [0, 0])
        self.clock.tick(self.refresh_rate) 

    def refresh_scores(self):
        self.screen.blit(self.font.render(
            "SCORE " + str(self.score), 1, WHITE), (12, 10))
        self.screen.blit(self.font.render(
            "LIVES " + str(self.lives + 1), 1, RED), (355, 570))

    def alien_wave(self, speed):
        for column in range(BARRIER_COLUMN):
            for row in range(BARRIER_ROW):
                alien = Alien()
                alien.rect.y = 55 + (column * (ALIEN_HEIGHT + ALIEN_SPACER))
                alien.rect.x = ALIEN_SPACER + (row * (ALIEN_WIDTH + ALIEN_SPACER))
                self.alien_group.add(alien) 
                self.all_sprite_list.add(alien)
                alien.speed -= speed

    def make_bullet(self):
        if self.player.shoot_bullet:
            if Game.game_time - self.player.time > self.player.speed:
                bullet = Ammo(BLUE, 5, 15)
                bullet.vector = -1
                bullet.speed = 26
                bullet.rect.x = self.player.rect.x + 30
                bullet.rect.y = self.player.rect.y + 10
                self.bullet_group.add(bullet)
                self.all_sprite_list.add(bullet)
                self.player.shoot_bullet = False
                self.player.time = Game.game_time

    def make_missile(self):
        shoot = random.randrange(50)
        if shoot in [16, 33, 49]:
            if len(self.alien_group):
                shooter = random.choice([alien for alien in self.alien_group])
                if shoot in [16, 33, 49]:
                    missile = Ammo(RED, 5, 5)
                    missile.vector = 1
                    missile.speed = 9
                    missile.rect.x = shooter.rect.x + 15
                    missile.rect.y = shooter.rect.y + 40
                    missile.speed += self.missile_booster
                    self.missile_group.add(missile)
                    self.all_sprite_list.add(missile)

    def make_barrier(self, columns, rows, barrier_spacer):
        for column in range(columns):
            for row in range(rows):
                barrier = Block(WHITE, 10, 10)
                barrier.rect.x = 55 + (200 * barrier_spacer) + (row * 10)
                barrier.rect.y = 450 + (column * 10)
                self.barrier_group.add(barrier)
                self.all_sprite_list.add(barrier)

    def make_defenses(self):
        for spacing, spacing in enumerate(xrange(4)):
            self.make_barrier(3, 9, spacing)

    def kill_all(self):
        for items in [self.bullet_group, self.player_group, 
        self.missile_group, self.alien_group, self.barrier_group]:
            for i in items:
                i.kill()

    def is_dead(self):
        if self.lives < 0:
            self.screen.blit(self.font.render(
            "Game Over! You scored: " + str(self.score), 1, RED), (275, 15))
            self.refresh_screen()
            pygame.time.delay(2500)
            return True

    def win_round(self):
        if len(self.alien_group) < 1 and self.goto_intro == False:
            self.screen.blit(self.font.render(
            "You won the round!", 1, RED), (325, 15))
            self.refresh_screen()
            pygame.time.delay(2500)
            return True

    def defenses_breached(self):
        for alien in self.alien_group:
            if alien.rect.y > 405:
                self.screen.blit(self.font.render(
                "The aliens have breached our defenses!", 1, RED), (240, 15))
                self.refresh_screen()
                pygame.time.delay(2500)
                return True

    def calc_collisions(self):
        pygame.sprite.groupcollide(
            self.missile_group, self.barrier_group, True, True)
        pygame.sprite.groupcollide(
            self.bullet_group, self.barrier_group, True, True)
        if pygame.sprite.groupcollide(
            self.bullet_group, self.alien_group, True, True):
            self.score += 10
        if pygame.sprite.groupcollide(
            self.player_group, self.missile_group, False, True):
            self.lives -= 1

    def next_round(self):
        for actor in [self.missile_group, self.barrier_group, self.bullet_group]:
            for i in actor:
                i.kill()
        self.alien_wave(self.level_up)
        self.make_defenses()
        self.missile_booster += 1
        self.level_up += 100

    def main_loop(self):
        while not Game.end_game:
            while not Game.goto_intro:
                Game.game_time = pygame.time.get_ticks()
                Game.alien_time = pygame.time.get_ticks()
                self.player.control()
                if self.player.shoot_bullet:
                    self.make_bullet()
                self.make_missile()
                for actor in [self.bullet_group, self.player_group, 
                self.alien_group, self.missile_group]:
                    for i in actor:
                        i.update()
                self.calc_collisions()
                if self.is_dead() or self.defenses_breached():
                    Game.goto_intro = True
                if self.win_round():
                    self.next_round()
                self.refresh_screen()
            self.splash_screen()
        pygame.quit()

if __name__ == '__main__':
    pv = Game()
    pv.main_loop()