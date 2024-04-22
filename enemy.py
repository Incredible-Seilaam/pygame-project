import pygame
from settings import *
from support import *
from entity import Entity

class Enemy(Entity):
    def __init__(self, monster_name, position, groups):
        super().__init__(groups)

        self.sprite_type = 'enemy'

        #graphics set up
        self.import_graphics(monster_name)
        self.status = 'idle'
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(topleft = position)

    def import_graphics(self, name):
        self.animations = {'idle':[], 'move':[], 'attack':[]}
        main_path = f'graphics/monsters/{name}/'

        for animation in self.animations.keys():
            self.animations[animation] = import_folder(main_path + animation)