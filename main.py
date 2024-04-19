import pygame, sys
from settings import *
from level import Level

class Game:
    def __init__(self):
        
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Prosim funguj o.o')
        self.clock = pygame.time.Clock()

        pygame.mixer.music.load('audio/harvest dawn.mp3')
        pygame.mixer.music.play(-1)  # -1 means loop indefinitely

        self.level = Level()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill((62,84,60)) #bud str se jmenem barvy nebo rgb tuple POZDEJS PRIDAM MAPU B)
            self.level.run()    #zavolá si metodu run definovanou v třídě Level
            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == '__main__':
    game = Game()
    game.run()
#