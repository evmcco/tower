# Lifted from: https://stackoverflow.com/a/40338475

import pygame
import time
import random

tile_size = 32

class Block(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([32, 32])
        self.image.fill((255, 0, 0))
        # self.image = pygame.image.load('assets/knight_m_idle_anim_f0.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.damage = 1
        self.health = 3

    def move(self):
        moveset = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]
        key = pygame.key.get_pressed()
        for i in range(2):
            if key[moveset[i]]:
                self.dx = [-32, 32][i]
                self.new_x = self.rect.x + self.dx
                if self.new_x >= 0 and self.new_x <= 224:
                    self.rect.x = self.new_x
                    time.sleep(.25)
                    return True

        for i in range(2):
            if key[moveset[2:4][i]]:
                self.dy = [-32, 32][i]
                self.new_y = self.rect.y + self.dy
                if self.new_y >= 0 and self.new_y <= 224:
                    self.rect.y = self.new_y
                    time.sleep(.25)
                    return True

    def attack(self, target):
        target.health -= self.damage
        print("%s did %d damage to %s, it has %d health now" % (self.name, self.damage, target.name, target.health))
        if target.health <= 0:
            print("%s has died" % target.name)


class Hero(Block):
    def __init__(self, pos):
        super() .__init__(pos)
        self.name = "The Hero"
        self.health = 3

class Monster(Block):
    def __init__(self, pos):
        super() .__init__(pos)
        self.health = 3
        self.name = "A Monster"


    def monster_move(self, player_pos):
        #if the monster is next to the hero, don't move
        #calulate direction based on player and monster position
        self.monster_pos = [self.rect.x, self.rect.y]
        self.x_dir = 0
        self.y_dir = 0
        if player_pos[0] - self.monster_pos[0] < 0:
            self.x_dir = -1 #go left
        elif player_pos[0] - self.monster_pos[0] > 0:
            self.x_dir = 1 #go right
        else:
            self.x_dir = 0 #don't go left or right
        if player_pos[1] - self.monster_pos[1] < 0:
            self.y_dir = -1 #go up
        elif player_pos[1] - self.monster_pos[1] > 0:
            self.y_dir = 1 #go down
        else:
            self.y_dir = 0 #don't go up or down
        #if player is above or next to monster, move directly toward
        if self.y_dir == 0:
            self.rect.x += self.x_dir * 32
        elif self.x_dir == 0:
            self.rect.y += self.y_dir * 32
        #if player diagonal from mosnter, move along x or y axis
        else:
            random_dir = random.randint(1,2)
            if random_dir == 1:
                self.rect.x += self.x_dir * 32
                self.y_dir = 0
                time.sleep(.25)
            elif random_dir == 2:
                self.rect.y += self.y_dir * 32
                self.x_dir = 0
                time.sleep(.25)




def main():
    pygame.init()
    clock = pygame.time.Clock()
    fps = 50
    bg = [80, 100, 80]
    size =[256, 256]
    screen = pygame.display.set_mode(size)

    player = Hero([16, 16])
    enemy = Monster([240, 240])
    enemy.next_to_hero = False

    enemy_group = pygame.sprite.Group()
    enemy_group.add(enemy)

    player_group = pygame.sprite.Group()
    player_group.add(player)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        if player.move(): #if the user has done an input
            hit = pygame.sprite.spritecollide(player, enemy_group, False)
            if hit:
                #if a collision will happen, 'unmove' and attack instead
                player.rect.x -= player.dx
                player.rect.y -= player.dy
                player.dx = 0
                player.dy = 0
                player.attack(enemy)
                enemy.next_to_hero = True
            else:
                enemy.next_to_hero = False
            #find player position and move monster toward it
            player_pos = [player.rect.x, player.rect.y]
            if enemy.next_to_hero == True:
                enemy.attack(player)
            elif enemy.next_to_hero == False:
                enemy.monster_move(player_pos)
            #after the monster moves
            hit = pygame.sprite.spritecollide(player, enemy_group, False)
            if hit:
                #if a collision will happen, 'unmove' and attack instead
                enemy.next_to_hero = True
                enemy.rect.x -= enemy.x_dir * 32
                enemy.rect.y -= enemy.y_dir * 32
                enemy.attack(player)
            else:
                enemy.next_to_hero = False
        screen.fill(bg)

        # first parameter takes a single sprite
        # second parameter takes sprite groups
        # third parameter is a do kill commad if true
        # all group objects colliding with the first parameter object will be
        # destroyed. The first parameter could be bullets and the second one
        # targets although the bullet is not destroyed but can be done with
        # simple trick bellow

        player_group.draw(screen)
        enemy_group.draw(screen)

        pygame.display.update()
        clock.tick(fps)

    pygame.quit()


if __name__ == '__main__':
    main()