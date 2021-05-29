import pygame, random

class Cactus:
    def __init__(self, sprites, init):
        self.type = random.randrange(4)
        self.sprite = sprites[self.type]
        self.position = pygame.Vector2()
        self.position_init = init
        self.position.xy = init[0], init[1]

    def change_sprite(self, sprites):
        self.type = random.randrange(4)
        self.sprite = sprites[self.type]
        if self.type < 3:
            self.position.y = 275
        else:
            self.position.y = 300
    
    def reset(self):
        self.position.xy = self.position_init[0], self.position_init[1]
