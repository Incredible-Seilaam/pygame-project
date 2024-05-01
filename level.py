from typing import Iterable
import pygame
from settings import *
from tile import Tile
from player import Player
from support import *
from random import choice
from debug import *
from npc import NPC
from enemy import Enemy
# from weapon import Weapon

class Level:
    def __init__(self):
        #get the display surface, can call from anywhere
        self.display_surface = pygame.display.get_surface()

        #sprite group setup
        self.visible_sprites = YsortCameraGroup() #every visible sprite
        self.obstacle_sprites = pygame.sprite.Group() #every sprite the player will/can collide with
        self.npc_sprites = pygame.sprite.Group()

        #sprite setup
        self.create_map()

    def create_map(self):   #time stamp 24:38
        layout = {
            'boundary': import_csv_layout('map/final_map__FloorBlocks.csv'),
            'grass': import_csv_layout('map/final_map__Grass.csv'),
            'object': import_csv_layout('map/final_map__Objects.csv'),
            'entities': import_csv_layout('map/final_map__Entities.csv')
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
                            Tile((x,y), [self.visible_sprites], 'grass', random_grass_img)
                        
                        if style == 'object': #create object tile
                            surface = graphics['objects'][int(col)]
                            Tile((x,y), [self.visible_sprites, self.obstacle_sprites], 'object', surface)

                        if style == 'entities':
                            if col == '10':
                                self.player = Player(
                                    (x,y),
                                    [self.visible_sprites],
                                    self.obstacle_sprites)
                            else:
                                if col == '6': monster_name = 'bamboo'
                                elif col == '7': monster_name = 'spirit'
                                elif col == '8': monster_name = 'raccoon'
                                elif col == '9': monster_name = 'squid'
                                elif col in {'0', '1', '2', '3', '4'}:  # NPC types
                                    npc_name = {'0': 'kaya', '1': 'dietrich', '2': 'maya', '3': 'laura', '4': 'rin'}[col]
                                    NPC(npc_name, (x, y), [self.visible_sprites], self.obstacle_sprites)
                                    
                                if col in {'6', '7', '8', '9'}:
                                    Enemy(monster_name, (x, y), [self.visible_sprites], self.obstacle_sprites)
                            # else:
                            #     if col == '6': monster_name = 'bamboo'
                            #     elif col == '7': monster_name = 'spirit'
                            #     elif col == '8': monster_name = 'raccoon'
                            #     elif col == '9': monster_name = 'squid'
                            #     Enemy(monster_name,(x, y), 
                            #         [self.visible_sprites], 
                            #         self.obstacle_sprites)
                            
                            #     if col == '0' : npc_name = 'kaya'
                            #     elif col == '1': npc_name = 'dietrich'
                            #     elif col == '2':npc_name = 'maya'
                            #     elif col == '3':npc_name = 'laura'
                            #     elif col == '4':npc_name = 'rin'
                            #     NPC(npc_name,(x, y),
                            #         [self.visible_sprites],
                            #         self.obstacle_sprites)



    # def create_attack(self):
    #     Weapon(self.player, [self.visible_sprites])

    def run(self):
        #updates and draws the game
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        self.visible_sprites.enemy_update(self.player)

#camera     ysort - sort podle y souradnice(možnost overlapovani spritu)
class YsortCameraGroup(pygame.sprite.Group):    #predelani groupu
    def __init__(self):
        
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0]//2
        self.half_height = self.display_surface.get_size()[1]//2
        self.offset = pygame.math.Vector2()

        #map floor texture
        self.floor_surface = pygame.image.load('graphics/tilemap/final_map.png').convert()
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
            npc.npc_sprites(player)