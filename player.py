import pygame
from support import import_folder
from npc import NPC

class Player(pygame.sprite.Sprite):
    def __init__(self,position,groups,obstacle_sprites):
        super().__init__(groups)        #super() -> allows usage of methods and properties from a parent class
        self.image = pygame.image.load('graphics/player/down/down_0.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = position)
        self.hitbox = self.rect.inflate(-10,-26)

        #movemnts
        self.direction = pygame.math.Vector2()
        self.speed = 5

        #special movements
        self.interacting = False
        self.interacting_cooldown = 300
        self.interacting_time = None

        #animation set up
        self.player_assets()
        self.status = 'down'
        self.frame_index = 0
        self.animation_speed = 0.15

        self.obstacle_sprites = obstacle_sprites

        self.npc = NPC

    def player_assets(self):
        character_path = 'graphics/player/'    #to vyuziju potom, az se budu chtit zbavit tyhle prisery dole
        self.animations = {
            'up':[], 'down':[], 'left':[], 'right':[],
            'up_idle':[], 'down_idle':[], 'left_idle':[], 'right_idle':[],
            'up_interacting':[], 'down_interacting':[],
            'left_interacting':[], 'right_interacting':[],
        }

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def animation(self):
        animation = self.animations[self.status]

        #loop over frames
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0    #resetne hodnotu indexu na 0
        #frames
        self.image = animation[int(self.frame_index)] #int, protoze iterujeme floatem a bez toho by se python zlobil
        self.rect = self.image.get_rect(center = self.hitbox.center)

    def get_status(self):
        #idle
        if self.direction.x == 0 and self.direction.y == 0:
            if not 'idle' in self.status and not 'interacting' in self.status:               #pridava idle jenom jednou 
                self.status = self.status + '_idle'
        
        if self.interacting:
            self.direction.x = 0
            self.direction.y = 0
            if not 'interacting' in self.status:
                if 'idle' in self.status:
                    self.status = self.status.replace('_idle','_interacting')
                else:
                    self.status = self.status + '_interacting'
        else:
            if 'interacting' in self.status:
                self.status = self.status.replace('_interacting','')

    def player_input(self):
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

        #interacting
        if keys[pygame.K_SPACE] and not self.interacting:
            self.interacting = True
            self.interacting_time = pygame.time.get_ticks()

    def move(self,speed):
        if self.direction.magnitude() != 0: #38:40 COOOOOOOOO TOOOOO ZNAMENAAAAA!!!!!!!!
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')
        self.rect.center = self.hitbox.center

        #self.rect.center += self.direction * speed #self.speed - enemaci by meli stejnej speed a to nechceme 
    
    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0: #player is moving to the right
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0: #player is moving to the left
                        self.hitbox.left = sprite.hitbox.right
        
        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0: #player is moving down
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0: #player is moving up
                        self.hitbox.top = sprite.hitbox.bottom

    def cooldowns(self):
        current_time = pygame.time.get_ticks()

        if self.interacting:
            if current_time - self.interacting_time >= self.interacting_cooldown:
                self.interacting = False

    def update(self):
        self.player_input()
        self.cooldowns()
        self.move(self.speed)
        self.animation()
        self.get_status()