import pygame
import time
import random

tile_size = 32

class Block(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([32, 32])
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = pos

    def move(self):
        moveset = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]
        key = pygame.key.get_pressed()
        self.new_x = self.rect.x
        self.new_y = self.rect.y
        for i in range(2):
            if key[moveset[i]]:
                self.dx = [-32, 32][i]
                self.dy = 0
                self.new_x = self.rect.x + self.dx
                if self.new_x >= 0 and self.new_x <= 224:
                    self.rect.x = self.new_x
                    time.sleep(.25)
                    return True

        for i in range(2):
            if key[moveset[2:4][i]]:
                self.dy = [-32, 32][i]
                self.dx = 0
                self.new_y = self.rect.y + self.dy
                if self.new_y >= 0 and self.new_y <= 224:
                    self.rect.y = self.new_y
                    time.sleep(.25)
                    return True
        # self.rect.center = [self.new_x, self.new_y]

    def attack(self, target):
        if self.can_attack == True:
            target.health -= self.damage
            print("%s did %d damage to %s, %s has %d health now" % (self.name, self.damage, target.name, target.name, target.health))
            if isinstance(target, Monster):
                target.can_attack = False
                print("Dazed!")
                target.image = pygame.transform.flip(target.image, False, True)
            if target.health <= 0:
                print("%s has died" % target.name)
                target.kill()
        else:
            print("%s is dazed and can't attack" % self.name)

class Health_Marker(pygame.sprite.Sprite):
    def __init__(self, pos, health):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([12, 12], pygame.SRCALPHA, 32).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]     
        default_font = pygame.font.get_default_font()
        font_renderer = pygame.font.Font(default_font, 12)
        health_label = font_renderer.render(str(health), 1, (255,255,255))
        self.image.blit(health_label, (0,0))
        
class Floor(Block):
    def __init__(self, pos, image):
        super() .__init__(pos)
        self.can_attack = False
        self.image = pygame.image.load(image).convert_alpha()

class Stairs(Block):
    def __init__(self, pos):
        super() .__init__(pos)
        self.can_attack = False
        self.image = pygame.image.load('assets/dngn_enter.png').convert_alpha()
    
class Hero(Block):
    def __init__(self, pos):
        super() .__init__(pos)
        self.name = "The Hero"
        self.damage = 1
        self.health = 5
        self.can_attack = True
        self.image = pygame.image.load('assets/knight_m_idle_anim_f0_v2.png').convert_alpha()

class Monster(Block):
    def __init__(self, pos, name):
        super() .__init__(pos)
        self.damage = 1
        self.health = 2
        self.image = pygame.image.load('assets/ogre_idle_anim_f0.png').convert_alpha()
        self.next_to_hero = False
        self.name = name






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
            return [self.rect.x, self.rect.y]
        elif self.x_dir == 0:
            self.rect.y += self.y_dir * 32
            return [self.rect.x, self.rect.y]
        #if player diagonal from mosnter, move along x or y axis
        else:
            random_dir = random.randint(1,2)
            if random_dir == 1:
                self.rect.x += self.x_dir * 32
                return [self.rect.x, self.rect.y]
                self.y_dir = 0
                time.sleep(.25)
            elif random_dir == 2:
                self.rect.y += self.y_dir * 32
                return [self.rect.x, self.rect.y]
                self.x_dir = 0
                time.sleep(.25)

def create_floor():
    floor_group = pygame.sprite.Group()
    for i in range(0,17):
        for ii in range(0,17):
            floor_tile_index = random.randint(1,8)
            coords = [((i * 16)), ((ii * 16))]
            floor_tile_file_string = 'assets/floor_%s.png' % floor_tile_index
            floor_tile = Floor(coords, floor_tile_file_string)
            floor_group.add(floor_tile)
    return floor_group

def create_stairs():
    stairs_loc = random.randint(0,14)
    if stairs_loc <= 7:
        stairs = Stairs([16 + stairs_loc * 32, 240])
    elif stairs_loc > 7:
        stairs = Stairs([240, 240 - ((stairs_loc - 7) * 32)])
    stair_group = pygame.sprite.Group()
    stair_group.add(stairs)
    return stair_group

def create_enemies(count):
    #create x many monsters on the other half of the board from the hero
    enemy_group = pygame.sprite.Group()
    enemy_locs = list()
    for i in range(count):
        x = 0
        y = 0
        while x + y < 240:
            x = random.randint(0,7) * 32 + 16
            y = random.randint(0,7) * 32 + 16
            if [x,y] in enemy_locs:
                x = 0
                y = 0
        name = 'Monster %d' % i
        enemy = Monster([x,y], name)
        enemy_group.add(enemy)
        enemy_locs.append([x,y])
    return enemy_group



def main():
    levels = 6
    pygame.font.init()
    for level in range(1,levels):
        pygame.init()
        clock = pygame.time.Clock()
        fps = 50
        bg = [80, 100, 80]
        size =[256, 256]
        screen = pygame.display.set_mode(size)

        player = Hero([16, 16])

        # enemy = Monster([240, 240])
        # enemy2 = Monster([240,16])

        # enemy_group = pygame.sprite.Group()
        # enemy_group.add(enemy)
        # enemy_group.add(enemy2)
        player_group = pygame.sprite.Group()
        player_group.add(player)
        enemy_group = create_enemies(level)
        floor_group = create_floor()
        stairs_group = create_stairs()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            if player.move(): #if the user has done an input
                monster_locs = list()
                for e in enemy_group:
                    monster_locs.append([e.rect.x, e.rect.y])
                for e in enemy_group:
                    hit = pygame.sprite.collide_rect(player, e)
                    if hit:
                        #if a collision will happen, 'unmove' and attack instead
                        player.rect.x -= player.dx
                        player.rect.y -= player.dy
                        player.attack(e)
                        e.next_to_hero = True
                    else:
                        e.next_to_hero = False
                        e.can_attack = True
                    #find player position and move monster toward it
                    player_pos = [player.rect.x, player.rect.y]
                    if e.next_to_hero == True:
                        e.attack(player)
                    elif e.next_to_hero == False:
                        new_monster_loc = e.monster_move(player_pos)
                        if new_monster_loc in monster_locs:
                            e.rect.x -= e.x_dir * 32
                            e.rect.y -= e.y_dir * 32
                            print("monster collision detected")
                        else:
                            if e.monster_pos in monster_locs:
                                monster_locs.remove(e.monster_pos)
                            monster_locs.append(new_monster_loc)
                    #after the monster moves
                    hit = pygame.sprite.collide_rect(player, e)
                    if hit:
                        #if a collision will happen, 'unmove' and attack instead
                        e.next_to_hero = True
                        e.rect.x -= e.x_dir * 32
                        e.rect.y -= e.y_dir * 32
                        e.attack(player)
                    else:
                        e.next_to_hero = False                
            screen.fill(bg)

            floor_group.draw(screen)
            stairs_group.draw(screen)
            player_group.draw(screen)
            enemy_group.draw(screen)
            health_marker_group = pygame.sprite.Group()
            for e in enemy_group:
                health_marker_group.add(Health_Marker([e.rect.x,e.rect.y], e.health))
            health_marker_group.add(Health_Marker([player.rect.x, player.rect.y], player.health))
            health_marker_group.draw(screen)
            pygame.display.update()
            clock.tick(fps)
            if not enemy_group:
                stairs_hit = pygame.sprite.spritecollide(player, stairs_group, False)
                if stairs_hit:
                    pygame.quit()
                    break
    print("You win!")
    pygame.quit()


if __name__ == '__main__':
    main()