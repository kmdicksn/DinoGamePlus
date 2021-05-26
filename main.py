import pygame, sys, time, random, colorsys, math, abc
from pygame.draw import circle
from pygame.locals import *
from abc import ABC, abstractmethod

CACTUS = [pygame.image.load('assets/Cactus/LargeCactus1.png'),pygame.image.load('assets/Cactus/LargeCactus2.png'),pygame.image.load('assets/Cactus/LargeCactus3.png'),pygame.image.load('assets/Cactus/SmallCactus1.png'),pygame.image.load('assets/Cactus/SmallCactus2.png'),pygame.image.load('assets/Cactus/SmallCactus3.png')]

RESET = pygame.image.load('assets/Other/Reset.png')
RESET_INIT = (460, 200)

PTERODACTYL = [pygame.image.load('assets/Pterodactyl/Bird1.png'), pygame.image.load('assets/Pterodactyl/Bird2.png')]

BUTTON = pygame.image.load('assets/Other/Button.png')

TRACK = pygame.image.load('assets/Other/Track.png')
TRACK_INIT = (0, 345)

PLAYER = [pygame.image.load('assets/Dino/DinoRun1.png'), pygame.image.load('assets/Dino/DinoRun2.png'), pygame.image.load('assets/Dino/DinoDead.png'), pygame.image.load('assets/Dino/DinoDuck1.png'), pygame.image.load('assets/Dino/DinoDuck2.png')]
PLAYER_INIT = (70, 280)

CLOUD = pygame.image.load('assets/Other/Cloud.png')

BLACK = (83, 83, 83)

class Player:
    position = pygame.Vector2()
    position.xy = 70, 280
    sprite = PLAYER[0:2]
    dead_sprite = PLAYER[2]
    duck_sprite = PLAYER[3:5]
    rect = sprite[0].get_rect()

class Ground:
    sprite = TRACK
    def __init__(self):
        self.position = pygame.Vector2()
        self.position.xy = TRACK_INIT[0], TRACK_INIT[1]

class Cactus:
    def __init__(self):
        self.type = random.randrange(4)
        self.sprite = CACTUS[self.type]
        self.position = pygame.Vector2()
        self.position.xy = -100, 300

    def change_sprite(self):
        self.type = random.randrange(4)
        self.sprite = CACTUS[self.type]
        if self.type < 3:
            self.position.y = 275
        else:
            self.position.y = 300

class Pterodactyl:
    def __init__(self):
        self.sprite = PTERODACTYL
        self.position = pygame.Vector2()
        self.position.xy = 1050, random.randint(200, 300)


class Cloud:
    def __init__(self):
        self.sprite = CLOUD
        self.position = pygame.Vector2()
        self.position.xy = random.randint(1100, 2100), random.randint(100,300)

class Button():
    def __init__(self, num):
        self.sprite = BUTTON
        self.position = pygame.Vector2()
        self.position.xy = 15 + num*(15 + BUTTON.get_width()), 400

def check_collide(a_x, a_y, a_width, a_height, b_x, b_y, b_width, b_height):
    return (a_x + a_width >= b_x) and (a_x <= b_x + b_width) and (a_y + a_height >= b_y) and (a_y <= b_y + b_height)

def main():
    pygame.init()
    pygame.display.set_caption("Dinosaur Game+")
    pygame.display.set_icon(Player.sprite[0])
    
    score = 0
    high_score = 0
    timer = 0

    font_big = pygame.font.Font('assets/Font/PressStart2P-Regular.ttf', 32)
    gameover = font_big.render('G A M E  O V E R', True, BLACK)
    player = Player()
    grounds = [Ground(), Ground()]
    cactuses = [Cactus(), Cactus(), Cactus()]
    pterodactyl = Pterodactyl()
    clouds = [Cloud(), Cloud(), Cloud()]
    buttons = [Button(0), Button(1), Button(2)]
    grounds[0].position.x = 0
    grounds[1].position.x = grounds[1].sprite.get_width()
    dead = False

    DISPLAY = pygame.display.set_mode((1000, 500),0,32)

    WHITE = (255, 255, 255)

    y_velocity = 0
    acceleration = 0.1
    run_state = True
    curr_ground = False
    ducking = False
    next_cactus = random.randint(30,40)

    # game loop
    while True:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()
        # draw background
        DISPLAY.fill(WHITE)

        #draw shapes
        if not dead:
            score = timer // 20
        score_display = font_big.render("{:05d}".format(score), True, BLACK)
        if high_score > 0:
            DISPLAY.blit(font_big.render("HI {:05d}".format(high_score), True, BLACK), (545, 20))
        DISPLAY.blit(score_display, (825, 20))
        DISPLAY.blit(grounds[0].sprite, (grounds[0].position.x, grounds[0].position.y))
        DISPLAY.blit(grounds[1].sprite, (grounds[1].position.x, grounds[1].position.y))
        for c in clouds:
            DISPLAY.blit(c.sprite, (c.position.x, c.position.y))
        if not dead:
            if ducking:
                player.position.y = PLAYER_INIT[1] + 30
                DISPLAY.blit(player.duck_sprite[run_state], player.position.xy)
            else:
                if player.position.y > PLAYER_INIT[1]:
                    player.position.y = PLAYER_INIT[1]
                DISPLAY.blit(player.sprite[run_state], player.position.xy)
        else:
            if score != 0:
                if score > high_score:
                    high_score = score
            if ducking:
                player.position.y = PLAYER_INIT[1]
            DISPLAY.blit(player.dead_sprite, ((player.position.x, player.position.y)))
            DISPLAY.blit(gameover, (250, 150))
            DISPLAY.blit(RESET, (RESET_INIT[0],RESET_INIT[1]))
        for c in cactuses:
            DISPLAY.blit(c.sprite, (c.position.xy))
            #check collision between player and cactus
            if check_collide(player.position.x, player.position.y, player.sprite[0].get_width()-10, player.sprite[0].get_height()-40,c.position.x, c.position.y, c.sprite.get_width(), c.sprite.get_height()) and timer > 10 and dead == False:
                dead = True

        DISPLAY.blit(pterodactyl.sprite[(timer//50)%2], (pterodactyl.position.xy))
        #check collision between player and pterodactyl
        if check_collide(player.position.x, player.position.y, player.sprite[0].get_width()-10, player.sprite[0].get_height()-40,pterodactyl.position.x, pterodactyl.position.y, pterodactyl.sprite[0].get_width(), pterodactyl.sprite[0].get_height()) and timer > 10 and dead == False:
            dead = True
        for b in buttons:
            DISPLAY.blit(b.sprite, (b.position.xy))

        if dead:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if (check_collide(mouse_x, mouse_y, 3, 3, RESET_INIT[0], RESET_INIT[1], RESET.get_width(), RESET.get_height()) and pygame.mouse.get_pressed() == (1,0,0)) or keys[K_SPACE]:
                cactuses = (Cactus(), Cactus(), Cactus())
                grounds = (Ground(), Ground())
                pterodactyl = Pterodactyl()
                dead = not dead
                timer = 0
                grounds[0].position.x = 0
                grounds[1].position.x = grounds[1].sprite.get_width()
                curr_ground = False
                player.position.xy = PLAYER_INIT[0], PLAYER_INIT[1]

            

        #move grounds and clouds to imitate movement
        if not dead:
            grounds[0].position.x -= 4
            grounds[1].position.x -= 4
            pterodactyl.position.x -= 4
            for c in clouds:
                c.position.x -= 2
                if c.position.x <= -100:
                    c.position.xy = random.randint(1100, 3100),random.randint(50, 300)
            for c in cactuses:
                c.position.x -= 4
            player.position.y += y_velocity
            y_velocity += acceleration

        #jumping
        if player.position.y >= PLAYER_INIT[1]:
            y_velocity = 0
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP]) and player.position.y >= PLAYER_INIT[1]:
            y_velocity = -5.5

        #ducking
        if (player.position.y == PLAYER_INIT[1] or player.position.y == PLAYER_INIT[1] + 30) and keys[K_DOWN]:
            ducking = True
        else:
            ducking = False
        
        #change between running sprites
        if timer%25 == 0 and player.position.y >= PLAYER_INIT[1] and not dead:
            run_state = not run_state
            
        #change between tracks
        if (timer*4)%grounds[0].sprite.get_width() == 0 and timer != 0 and not dead:
            grounds[curr_ground].position.x += 2*grounds[0].sprite.get_width()
            curr_ground = not curr_ground

        #create cactuses
        if timer%next_cactus == 0:
            next_cactus = random.randint(400,600)
            for c in cactuses:
                if c.position.x < -300:
                    c.position.x = 1050
                    c.change_sprite()
                    DISPLAY.blit(c.sprite, (c.position.x, c.position.y))
                    break

        if timer%random.randint(50,100) == 0:
            if pterodactyl.position.x < -300:
                pterodactyl.position.x = 1050
                pterodactyl.position.y = random.randint(200,300)

        
        timer += 1

        pygame.display.update()
        
        pygame.time.delay(4)


main()