import pygame

class Ground:
    def __init__(self, sprite, init):
        self.sprite = sprite
        self.position = pygame.Vector2()
        self.position.xy = init[0], init[1]
        self.position_init = init

    def reset(self):
        self.position.xy = self.position_init[0], self.position_init[1]