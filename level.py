from typing import Iterable
import pygame
from settings import *
from tile import Tile
from player import Player
from support import *
from random import choice
from debug import *
from npc import *

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
            'boundary': import_csv_layout('map/map_FloorBlocks.csv'),
            'grass': import_csv_layout('map/map_Grass.csv'),
            'object': import_csv_layout('map/map_Objects.csv'),
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

        self.player = Player((2000,1430),[self.visible_sprites],self.obstacle_sprites) #time stamp 34.24
        
        # self.npc = NPC((2250,1430), [self.visible_sprites, self.obstacle_sprites])

    def run(self):
        #updates and draws the game
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()

        # self.player_npc_interaction()

    # def player_npc_interaction(self):
    #     if pygame.sprite.collide_rect(self.player, self.npc):
    #         keys = pygame.key.get_pressed()
    #         if keys[pygame.K_SPACE]:
    #             print('interacting')

#camera     ysort - sort podle y souradnice(možnost overlapovani spritu)
class YsortCameraGroup(pygame.sprite.Group):    #predelani groupu
    def __init__(self):
        
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0]//2
        self.half_height = self.display_surface.get_size()[1]//2
        self.offset = pygame.math.Vector2()

        #map floor texture
        self.floor_surface = pygame.image.load('graphics/tilemap/ground.png').convert()
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