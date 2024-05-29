import pygame
from settings import *
from support import import_folder
from entity import Entity

class Player(Entity):
    def __init__(self, position, groups, obstacle_sprites, create_attack, destroy_attack, create_magic): #create_interaction, destroy_interaction
        super().__init__(groups)        #super() -> allows usage of methods and properties from a parent class
        self.image = pygame.image.load('graphics/player/down/down_0.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = position)
        self.hitbox = self.rect.inflate(-10,HITBOX_OFFSET['player'])

        #animation set up
        self.player_assets()
        self.status = 'down'

        #special movements
        self.attacking = False
        self.attack_cooldown = 300
        self.attack_time = None

        self.obstacle_sprites = obstacle_sprites

        # #interaction
        # self.create_interaction = create_interaction
        # self.destroy_interaction = destroy_interaction
        # self.interacting = False
        # self.can_interact = True
        # self.interaction_cooldown = 400
        # self.interaction_time = None

		# weapon
        self.create_attack = create_attack
        self.destroy_attack = destroy_attack
        self.weapon_index = 0
        self.weapon = list(weapon_data.keys())[self.weapon_index]
        self.can_switch_weapon = True
        self.weapon_switch_time = None
        self.switch_duration_cooldown = 200

		# magic 
        self.create_magic = create_magic
        self.magic_index = 0
        self.magic = list(magic_data.keys())[self.magic_index]
        self.can_switch_magic = True
        self.magic_switch_time = None

        #stats
        self.stats = {'health': 100,'energy':60,'attack': 10,'magic': 4,'speed': 5}
        self.max_stats = {'health': 300, 'energy': 140, 'attack': 20, 'magic' : 10, 'speed': 10}
        self.upgrade_cost = {'health': 100, 'energy': 100, 'attack': 100, 'magic' : 100, 'speed': 100}
        self.health = self.stats['health'] * 0.5
        self.energy = self.stats['energy'] * 0.8
        self.exp = 5000
        self.speed = self.stats['speed']

		# damage timer
        self.vulnerable = True
        self.hurt_time = None
        self.invulnerability_duration = 500

		# import a sound NEED TO ADD

    def player_assets(self):
        character_path = 'graphics/player/'    #to vyuziju potom, az se budu chtit zbavit tyhle prisery dole
        self.animations = {
            'up':[], 'down':[], 'left':[], 'right':[],
            'up_idle':[], 'down_idle':[], 'left_idle':[], 'right_idle':[],
            'up_interacting':[], 'down_interacting':[],
            'left_interacting':[], 'right_interacting':[],
            'up_attack':[], 'down_attack':[], 'left_attack':[], 'right_attack':[]}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def player_input(self):
        if not self.attacking:
            keys = pygame.key.get_pressed()

            #movement input
            if keys[pygame.K_w]:
                self.direction.y = -1   #up
                self.status = 'up'
            elif keys[pygame.K_s]:
                self.direction.y = 1    #down
                self.status = 'down'
            else:
                self.direction.y = 0

            if keys[pygame.K_a]:
                self.direction.x = -1   #left
                self.status = 'left'
            elif keys[pygame.K_d]:
                self.direction.x = 1    #right
                self.status = 'right'
            else:
                self.direction.x = 0
            
            # #interaction input
            # if keys[pygame.K_SPACE]:
            #     self.interacting = True
            #     self.attack_time = pygame.time.get_ticks()
            #     self.create_interaction()

            #attack input
            if keys[pygame.K_f]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                self.create_attack()
                #self.weapon_attack_sound.play()

            #magic input
            if keys[pygame.K_LCTRL]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                style = list(magic_data.keys())[self.magic_index]
                strength = list(magic_data.values())[self.magic_index]['strength'] + self.stats['magic']
                cost = list(magic_data.values())[self.magic_index]['cost']
                self.create_magic(style,strength,cost)

            #weapon switch
            if keys[pygame.K_q] and self.can_switch_weapon:
                self.can_switch_weapon = False
                self.weapon_switch_time = pygame.time.get_ticks()

                if self.weapon_index < len(list(weapon_data.keys())) - 1:
                    self.weapon_index += 1
                else:
                    self.weapon_index = 0

                self.weapon = list(weapon_data.keys())[self.weapon_index]

            #magic switch
            if keys[pygame.K_e] and self.can_switch_magic:
                self.can_switch_magic = False
                self.magic_switch_time = pygame.time.get_ticks()

                if self.magic_index < len(list(magic_data.keys())) - 1:
                    self.magic_index += 1
                else:
                    self.magic_index = 0

                self.magic = list(magic_data.keys())[self.magic_index]

    def get_status(self):
        #idle
        if self.direction.x == 0 and self.direction.y == 0:
            if not 'idle' in self.status and not 'attack' in self.status:               #pridava idle jenom jednou 
                self.status = self.status + '_idle'
        
        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            if not 'attack' in self.status:
                if 'idle' in self.status:
                    self.status = self.status.replace('_idle','_attack')
                else:
                    self.status = self.status + '_attack'

        # # Interacting
        # if self.interacting:
        #     self.direction.x = 0
        #     self.direction.y = 0
        #     if 'interacting' not in self.status:
        #         if 'idle' in self.status:
        #             self.status = self.status.replace('_idle', '_interacting')
        #         elif 'attack' in self.status:
        #             self.status = self.status.replace('_attack', '_interacting')
        #         else:
        #             self.status += '_interacting'
        
        # # Not attacking or interacting
        # if not self.attacking and not self.interacting:
        #     if 'attack' in self.status:
        #         self.status = self.status.replace('_attack', '')
        #     elif 'interacting' in self.status:
        #         self.status = self.status.replace('_interacting', '')

    def cooldowns(self):
        current_time = pygame.time.get_ticks()

        # if self.interacting:
        #     if current_time - self.interaction_time >= self.interaction_cooldown:
        #         self.interacting = False
        #         self.destroy_interaction()

        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown + weapon_data[self.weapon]['cooldown']:
                self.attacking = False
                self.destroy_attack()

        if not self.can_switch_weapon:
            if current_time - self.weapon_switch_time >= self.switch_duration_cooldown:
                self.can_switch_weapon = True

        if not self.can_switch_magic:
            if current_time - self.magic_switch_time >= self.switch_duration_cooldown:
                self.can_switch_magic = True

        if not self.vulnerable:
            if current_time - self.hurt_time >= self.invulnerability_duration:
                self.vulnerable = True

    def animation(self):
        animation = self.animations[self.status]

        #loop over frames
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0    #resetne hodnotu indexu na 0

        #frames
        self.image = animation[int(self.frame_index)] #int, protoze iterujeme floatem a bez toho by se python zlobil
        self.rect = self.image.get_rect(center = self.hitbox.center)

        #flicker
        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def get_full_weapon_damage(self):
        base_damage = self.stats['attack']
        weapon_damage = weapon_data[self.weapon]['damage']
        return base_damage + weapon_damage

    def get_full_magic_damage(self):
        base_damage = self.stats['magic']
        spell_damage = magic_data[self.magic]['strength']
        return base_damage + spell_damage

    def get_value_by_index(self,index):
        return list(self.stats.values())[index]

    def get_cost_by_index(self,index):
        return list(self.upgrade_cost.values())[index]

    def energy_recovery(self):
        if self.energy < self.stats['energy']:
            self.energy += 0.01 * self.stats['magic']
        else:
            self.energy = self.stats['energy']

    # def check_interaction(self):
    #     # Check if the SPACE key is pressed and the player is not already interacting
    #     keys = pygame.key.get_pressed()
    #     if keys[pygame.K_SPACE] and not self.interacting:
    #         # Loop through NPCs to find the nearest one within interaction range
    #         nearest_npc = None
    #         nearest_distance = float('inf')  # Initialize with a large value

    #         for npc in self.npcs:
    #             distance = self.rect.distance_to(npc.rect)
    #             if distance < self.interaction_range and distance < nearest_distance:
    #                 nearest_npc = npc
    #                 nearest_distance = distance

    #         # If a nearest NPC is found, interact with it
    #         if nearest_npc:
    #             self.interact(nearest_npc)

    # def interact(self, npc):
    #     # Trigger interaction with the specified NPC
    #     current_time = pygame.time.get_ticks()
    #     if current_time - self.last_interaction_time >= self.interaction_cooldown:
    #         self.interacting = True
    #         self.create_interaction(npc)
    #         self.last_interaction_time = current_time

    def update(self):
        self.player_input()
        self.cooldowns()
        self.get_status()
        self.animation()
        self.move(self.stats['speed'])
        self.energy_recovery()
        # self.check_interaction()