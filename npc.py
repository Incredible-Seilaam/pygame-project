import pygame
from settings import *
from support import *
from entity import Entity

class NPC(Entity):
    def __init__(self, npc_name, position, groups, obstacle_sprites):
        super().__init__(groups)

        self.sprite_type = 'npc'

        #graphics setup
        self.import_graphics(npc_name)
        self.status = 'idle'
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(topleft = position)

        #movement
        self.hitbox = self.rect.inflate(0,-10)
        self.obstacle_sprites = obstacle_sprites

        #stats
        self.npc_name = npc_name
        npc_info = npc_data[self.npc_name]
        self.speed = npc_info['speed']
        self.attack_damage = npc_info['attack_damage']
        self.attack_radius = npc_info['attack_radius']
        self.notice_radius = npc_info['notice_radius']
        self.attack_type = npc_info['attack_type']

        # self.npc_name = npc_name
        # npc_info = npc_data[self.npc_name]
        # self.speed = npc_info['speed']
        # self.interaction_radius = npc_info['interaction_radius']
        # self.notice_radius = npc_info['notice_radius']

        #player interaction
        self.can_attack = True
        self.attack_time = None
        self.attack_cooldown = 400

    def import_graphics(self, name):
        self.animations = {'idle':[], 'attack':[], 'move':[]}
        main_path = f'graphics/npcs/{name}/'

        for animation in self.animations.keys():
            self.animations[animation] = import_folder(main_path + animation)
    
    def find_player(self, player):
        npc_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)

        distance = (player_vec - npc_vec).magnitude()
        if self.status == 'attack':
            direction = pygame.math.Vector2()
        else:
            if distance > 0:
                direction = (player_vec - npc_vec).normalize() #matematický čáry máry
            else:
                direction = pygame.math.Vector2()    
        return(distance, direction)
    
    def get_status(self, player):
        distance = self.find_player(player)[0]

        if distance <= self.attack_radius and self.can_attack:
            if self.status != 'attack':
                self.frame_index = 0
            self.status = 'attack'
        elif distance <= self.notice_radius:
            self.status = 'move'
        else:
            self.status = 'idle'

    def actions(self, player):
        if self.status == 'attack':
            input('bla bla bla: ')
            print('ble ble ble')
            self.direction = self.find_player(player)[1]
        elif self.status == 'move':
            self.direction = self.find_player(player)[1]
        else:
            self.direction = pygame.math.Vector2()

    def animate(self):
        animation = self.animations[self.status]

        #loop over frames
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.interaction_time = pygame.time.get_ticks()
            if self.status == 'attack':
                self.can_interact = False
            self.frame_index = 0
        
        #frames
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)

    def cooldown(self):
        if not self.can_attack:
            current_time = pygame.time.get_ticks()
            if current_time - self.attack_time >= self.attack_cooldown:
                self.can_attack = True

    def update(self):
        self.move(self.speed)
        self.animate()
        self.cooldown()

    def npc_update(self, player):
        self.get_status(player)
        self.actions(player)

