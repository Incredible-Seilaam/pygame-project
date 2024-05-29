from typing import Iterable
import pygame
from settings import *
from tile import Tile
from player import Player
from debug import debug
from support import *
from random import choice, randint
from weapon import Weapon
from ui import UI
from npc import NPC
from enemy import Enemy
from particles import AnimationPlayer
from magic import MagicPlayer
from upgrade import Upgrade
# from weapon import Weapon

class Level:
    def __init__(self):
        #get the display surface, can call from anywhere
        self.display_surface = pygame.display.get_surface()
        self.game_paused = False
        
        #sprite group setup
        self.visible_sprites = YsortCameraGroup() #every visible sprite
        self.obstacle_sprites = pygame.sprite.Group() #every sprite the player will/can collide with
        
		# attack sprites
        self.current_attack = None
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()

        #sprite setup
        self.create_map()

        #user interface
        self.ui = UI()
        self.upgrade = Upgrade(self.player)

        #particles
        self.animation_player = AnimationPlayer()
        self.magic_player = MagicPlayer(self.animation_player) 

    def create_map(self):   #time stamp 24:38
        layout = {
            'boundary': import_csv_layout('map/map_final_fix5_CollisionBlocks.csv'),
            'grass': import_csv_layout('map/map_final_fix5_Grass.csv'),
            'object': import_csv_layout('map/map_final_fix5_Objects.csv'),      #FIX CSV FILE, ted je tam to stary co funguje
            'entities': import_csv_layout('map/map_final_fix5_Entities.csv'),
            'npcs': import_csv_layout('map/map_final_fix5_Npcs.csv')
        }
        
        graphics = {
            'grass': import_folder('graphics/Grass'),
            'objects': import_folder('graphics/Objects'),
        }
        
        for style, layout in layout.items():
            for row_index,row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'boundary':
                            Tile((x,y), [self.obstacle_sprites], 'invisible')
                        
                        if style == 'grass': #create grass tile
                            random_grass_img = choice(graphics['grass'])
                            Tile(
                                (x,y),
                                [self.visible_sprites,
                                self.obstacle_sprites,
                                self.attackable_sprites], 
                                'grass', random_grass_img)
                        
                        if style == 'object': #create object tile
                            surface = graphics['objects'][int(col)]
                            Tile((x,y), [self.visible_sprites, self.obstacle_sprites], 'object', surface)

                        if style == 'entities':
                            if col == '10':
                                self.player = Player(
                                    (x,y),
                                    [self.visible_sprites],
                                    self.obstacle_sprites,
                                    self.create_attack,
                                    self.destroy_attack,
                                    self.create_magic)
                                    #self.create_interaction,
                                    #self.destroy_interaction
                            else:
                                if col == '6': monster_name = 'bamboo'
                                elif col == '7': monster_name = 'spirit'
                                elif col == '8': monster_name = 'raccoon'
                                elif col == '9': monster_name = 'squid'
                                Enemy(monster_name,
                                        (x, y),
                                        [self.visible_sprites, self.attackable_sprites],
                                        self.obstacle_sprites,
                                        self.damage_player,
                                        self.trigger_death_particles,
                                        self.add_exp)
                        
                        if style == 'npcs':
                            if col == '0' : npc_name = 'kaya'
                            elif col == '1': npc_name = 'dietrich'
                            elif col == '2':npc_name = 'maya'
                            elif col == '3':npc_name = 'laura'
                            elif col == '4':npc_name = 'rin'
                            NPC(npc_name, (x, y), [self.visible_sprites], self.obstacle_sprites)

    def create_attack(self):
        self.current_attack = Weapon(self.player, [self.visible_sprites, self.attack_sprites])

    def create_magic(self, style, strength, cost):
        if style == 'heal':
            self.magic_player.heal(self.player,strength,cost,[self.visible_sprites])

        if style == 'flame':
            self.magic_player.flame(self.player,cost,[self.visible_sprites,self.attack_sprites])

    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def player_attack_logic(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(attack_sprite,self.attackable_sprites,False)
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        if target_sprite.sprite_type == 'grass':
                            pos = target_sprite.rect.center
                            offset = pygame.math.Vector2(0,75)
                            for leaf in range(randint(3,6)):
                                self.animation_player.create_grass_particles(pos - offset,[self.visible_sprites])
                            target_sprite.kill()
                        else:
                            target_sprite.get_damage(self.player,attack_sprite.sprite_type)

    def damage_player(self, amount, attack_type):
        if self.player.vulnerable:
            self.player.health -= amount
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()
            self.animation_player.create_particles(attack_type,self.player.rect.center,[self.visible_sprites])

    def trigger_death_particles(self, pos, particle_type):
        self.animation_player.create_particles(particle_type,pos,self.visible_sprites)

    def add_exp(self, amount):
        self.player.exp += amount

    def toggle_menu(self):
        self.game_paused = not self.game_paused 

    def run(self):
        #updates and draws the game
        self.visible_sprites.custom_draw(self.player)
        self.ui.display(self.player)

        if self.game_paused:
            self.upgrade.display()
        else:
            self.visible_sprites.update()
            self.visible_sprites.enemy_update(self.player)
            self.visible_sprites.npc_update(self.player)
            self.player_attack_logic()

#camera     ysort - sort podle y souradnice(možnost overlapovani spritu)
class YsortCameraGroup(pygame.sprite.Group):    #predelani groupu
    def __init__(self):
        
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0]//2
        self.half_height = self.display_surface.get_size()[1]//2
        self.offset = pygame.math.Vector2()

        #map floor texture
        self.floor_surface = pygame.image.load('graphics/tilemap/map_base.png').convert()
        self.floor_rect = self.floor_surface.get_rect(topleft = (0,0))

    def custom_draw(self,player):
        #getting the offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        #drawing the floor
        floor_offset_position = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surface, floor_offset_position)
        
        # for sprite in self.sprites():
        for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image,offset_pos)

    def enemy_update(self, player):
        enemy_sprites = [sprite 
                        for sprite in self.sprites()
                            if hasattr(sprite,'sprite_type') and sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)

    def npc_update(self, player):
        npc_sprites = [sprite
                        for sprite in self.sprites()
                            if hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'npc']
        for npc in npc_sprites:
            npc.npc_update(player)