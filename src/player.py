import pygame

class Player:
    position = pygame.Vector2()
    position.xy = 70, 280
    position_init = (70, 280)

    def __init__(self, sprites):
        self.sprite = sprites[0:2]
        self.dead_sprite = sprites[2]
        self.duck_sprite = sprites[3:5]
        self.curr_sprite = self.sprite[0]
        pass