import pygame

class NPC(pygame.sprite.Sprite):
    def __init__(self, position, groups):
        super().__init__(groups)
        self.image = pygame.image.load('graphics/npc/npc_idle.png').convert_alpha()  # Example surface size, replace with your NPC image
        self.rect = self.image.get_rect(topleft=position)
        self.hitbox = self.rect.inflate(-20,-40)
        #self.npc_sprites = pygame.sprite.Group()