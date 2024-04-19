import pygame

class SpeechBubble:
    def __init__(self, position, text):
        self.font = pygame.font.Font(None, 24)
        self.text = text
        self.text_surface = self.font.render(self.text, True, (255, 255, 255))
        self.rect = self.text_surface.get_rect(center=position)
        self.background_rect = self.rect.inflate(10, 10)

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 0, 0), self.background_rect)
        screen.blit(self.text_surface, self.rect)