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
        tile_dict[pos] = self
        self.damage = 1
        self.health = 3

    def find_tile(self):
        for i in tile_dict.keys():
            if tile_dict[i] == self:
                return int(i)

    def move(self):
        self.old_pos = self.find_tile()
        moveset = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]
        key = pygame.key.get_pressed()
        for i in range(4):
            if key[moveset[i]]:
                self.movement = [-1, 1, -8, 8][i]
                self.new_pos = self.old_pos + self.movement
                tile_dict[self.new_pos] = self
                tile_dict[self.old_pos] = list() 
                time.sleep(.25)
                return True


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
        self.monster_pos = self.find_tile()
        if tile_dict[self.monster_pos]:
            mx = self.monster_pos
            my = self.monster_pos
            while mx > 8:
                mx -= 8
            while my % 8 != 0:
                my += 1
            my /= 8
        if tile_dict[player_pos]:
            px = player_pos
            py = player_pos
            while px > 8:
                px -= 8
            while py % 8 != 0:
                py += 1
            py /= 8
        dx = mx - px
        dy = my - py
        if dx >= dy:
            if dx > 0:
                self.x_dir = -1
            elif dx < 0:
                self.x_dir = 1
            tile_dict[self.monster_pos + self.x_dir] = self
        elif dy < dx:
            if dy > 0:
                self.y_dir = -8
            elif dy < 0:
                self.y_dir = 8
            tile_dict[self.monster_pos + self.y_dir] = self
        tile_dict[self.monster_pos] = list()
        





        # if self.monster_pos % 8 < player_pos % 8:
        #     self.x_dir = 1
        # elif self.monster_pos % 8 > player_pos % 8:
        #     self.x_dir = -1
        # else:
        #     self.x_dir = 0
        # if self.monster_pos < player_pos:
        #     self.y_dir = 8
        # elif self.monster_pos > player_pos:
        #     self.y_dir = -8
        # elif math.floor(self.monster_pos/8) == math.floor(player_pos/8):
        #     self.y_dir = 0
        # if self.y_dir == 0:
        #     tile_dict[self.monster_pos + self.x_dir] = self
        # elif self.x_dir == 0:
        #     tile_dict[self.monster_pos + self.y_dir] = self
        # else:
        #     random_dir = random.randint(1,2)
        #     if random_dir == 1:
        #         tile_dict[self.monster_pos + self.x_dir] = self
        #         self.y_dir = 0
        #         time.sleep(.25)
        #     elif random_dir == 2:
        #         tile_dict[self.monster_pos + self.y_dir] = self
        #         self.x_dir = 0
        #         time.sleep(.25)
        # tile_dict[self.monster_pos] = list()

def convert_tile_to_coords(pos):
    if tile_dict[pos]:
        x = pos
        y = pos
        while x > 8:
            x -= 8
        x = (x-1) * 32
        while y % 8 != 0:
            y += 1
        y /= 8
        y = (y-1) * 32
    return [x,y]

def main():
    pygame.init()
    clock = pygame.time.Clock()
    fps = 50
    bg = [80, 100, 80]
    size =[256, 256]
    screen = pygame.display.set_mode(size)

    player = Hero(1)
    enemy = Monster(64)
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
            player.pos = player.find_tile()
            enemy.pos = enemy.find_tile()
            if player.pos == enemy.pos:
                #if a collision will happen, 'unmove' and attack instead
                player.pos -= player.movement
                player.attack(enemy)
            #find player position and move monster toward it
            if enemy.pos - player.pos == 1 or enemy.pos - player.pos == -1 or enemy.pos - player.pos == 8 or player.pos - enemy.pos == -8:
                enemy.attack(player)
            else:
                player_coords = convert_tile_to_coords(player.pos)
                enemy_coords = convert_tile_to_coords(enemy.pos)
                #determine direction for monster to move
                print("player", player_coords, "enemy", enemy_coords)
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

        


        for i in tile_dict.keys():
            if tile_dict[i]:
                x = i
                y = i
                while x > 8:
                    x -= 8
                tile_dict[i].rect.x = (x-1) * 32
                while y % 8 != 0:
                    y += 1
                y /= 8
                tile_dict[i].rect.y = (y-1) * 32

        
        
        
        
        player_group.draw(screen)
        enemy_group.draw(screen)

        pygame.display.update()
        clock.tick(fps)
        print(enemy.find_tile())
        print(tile_dict)

    pygame.quit()


if __name__ == '__main__':
    main()