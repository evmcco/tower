# Lifted from: https://stackoverflow.com/a/40338475

import pygame
import time
import random
import math

tile_size = 32
tile_dict = {k:list() for k in range(1,65)}
print(tile_dict)

class Block(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([32, 32])
        self.image.fill((255, 0, 0))
        # self.image = pygame.image.load('assets/knight_m_idle_anim_f0.png').convert_alpha()
        self.rect = self.image.get_rect()
        tile_dict[pos] == self
        self.damage = 1
        self.health = 3
        print(tile_dict)

    def find_tile(self):
        for i in range(1,65):
            if tile_dict[i] == self:
                return int(i)

    def move(self):
        self.old_pos = self.find_tile()
        print(self.find_tile())
        moveset = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]
        key = pygame.key.get_pressed()
        for i in range(4):
            if key[moveset[i]]:
                self.movement = [-1, 1, -8, 8][i]
                print(type(self.old_pos))
                self.new_pos = self.old_pos + self.movement
                tile_dict[self.new_pos] = self
                tile_dict[self.old_pos] = list() 


    def attack(self, target):
        target.health -= self.damage
        print("%s did %d damage to %s, it has %d health now" % (self.name, self.damage, target.name, target.health))
        if target.health <= 0:
            print("%s has died" % target.name)


class Hero(Block):
    # def __init__(self, pos):
    #     super() .__init__()
    #     self.name = "The Hero"
    #     self.health = 3
    pass

class Monster(Block):
    # def __init__(self, pos):
    #     super() .__init__(pos)
    #     self.health = 3
    #     self.name = "A Monster"
    pass


    def monster_move(self, player_pos):
        #if the monster is next to the hero, don't move
        #calulate direction based on player and monster position
        self.monster_pos = self.find_title()
        if self.monster_pos % 8 < player_pos % 8:
            self.x_dir = -1
        elif self.monster_pos % 8 > player_pos % 8:
            self.x_dir = 1
        else:
            self.x_dir = 0
        if self.monster_pos < player_pos:
            self.y_dir = -8
        elif self.monster_pos > player_pos:
            self.y_dir = 8
        if math.floor(monster_pos/8) == math.floor(player_pos/8):
            self.y_dir = 0
        if self.y_dir == 0:
            tile_dict[self.monster_pos + self.x_dir] = self
        elif self.x_dir == 0:
            tile_dict[self.monster_pos + self.y_dir] = self
        else:
            random_dir = random.randint(1,2)
            if random_dir == 1:
                tile_dict[self.monster_pos + self.x_dir] = self
                self.y_dir = 0
                time.sleep(.25)
            elif random_dir == 2:
                tile_dict[self.monster_pos + self.y_dir] = self
                self.x_dir = 0
                time.sleep(.25)
        tile_dict[self.monster_pos] = list()


def main():
    pygame.init()
    clock = pygame.time.Clock()
    fps = 50
    bg = [80, 100, 80]
    size =[256, 256]
    screen = pygame.display.set_mode(size)

    player = Hero(24)
    enemy = Monster(48)
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
            if player.pos == enemy.pos:
                #if a collision will happen, 'unmove' and attack instead
                player.pos -= player.movement
                player.attack(enemy)
                enemy.next_to_hero = True
            else:
                enemy.next_to_hero = False
            #find player position and move monster toward it
            if enemy.next_to_hero == True:
                enemy.attack(player)
            elif enemy.next_to_hero == False:
                enemy.monster_move(player.pos)
            #after the monster moves
            hit = pygame.sprite.spritecollide(player, enemy_group, False)
            if hit:
                #if a collision will happen, 'unmove' and attack instead
                enemy.next_to_hero = True
                enemy.pos -= (enemy.y_dir + enemy.x_dir)
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

        

        for i in range(1,65):
            if tile_dict[i]:
                tile_dict[i].rect.x = ((i % 8) - 1) * 32
                print(tile_dict[i].rect.x)
                tile_dict[i].rect.y = math.ceil(i/8) * 32
                print(tile_dict[i].rect.y)
        player_group.draw(screen)
        enemy_group.draw(screen)

        pygame.display.update()
        clock.tick(fps)
        print(tile_dict)
    pygame.quit()


if __name__ == '__main__':
    main()