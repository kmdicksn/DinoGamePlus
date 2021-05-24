import pygame, os

class Player:
    position = pygame.Vector2()
    position.xy = 300, 200
    sprite = [pygame.image.load('/assets/Dino/DinoRun1.png'), pygame.image.load('/assets/Dino/DinoRun2.png')]