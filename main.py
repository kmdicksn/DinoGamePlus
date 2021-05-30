import math, pygame, sys, time, random, colorsys, abc,  ipinfo, requests
from pygame import Vector2
from src.player import Player
from src.ground import Ground
from src.cactus import Cactus
from src.utils import *
from pygame.draw import circle
from pygame.locals import *
from pygame.surface import *
from abc import ABC, abstractmethod
from math import *

#init pygame and display
pygame.init()
DISPLAY = pygame.display.set_mode((1000, 500),0,32)

#VISUALS
START = get_img('assets/Other/Button2.png')

CACTUS = [get_img('assets/Cactus/LargeCactus1.png'),get_img('assets/Cactus/LargeCactus2.png'),get_img('assets/Cactus/LargeCactus3.png'),get_img('assets/Cactus/SmallCactus1.png'),get_img('assets/Cactus/SmallCactus2.png'),get_img('assets/Cactus/SmallCactus3.png')]
CACTUS_INIT = (-100, 300)

PLAYER = [get_img('assets/Dino/DinoRun1.png'), get_img('assets/Dino/DinoRun2.png'), get_img('assets/Dino/DinoDead.png'), get_img('assets/Dino/DinoDuck1.png'), get_img('assets/Dino/DinoDuck2.png'), get_img('assets/Dino/DinoFly1.png'), get_img('assets/Dino/DinoFly2.png'), get_img('assets/Dino/DinoFlyDead.png')]

RESET = get_img('assets/Other/Reset.png')
RESET_INIT = (460, 200)

PTERODACTYL = [get_img('assets/Pterodactyl/Bird1.png'), get_img('assets/Pterodactyl/Bird2.png')]

COIN = get_img('assets/Other/coin.png')

BUTTON = get_img('assets/Other/Button.png')
BUTTON_FLY = get_img('assets/Other/Wings.png')
BUTTON_JUMP = get_img('assets/Other/DblJump.png')
BUTTON_HEART = get_img('assets/Other/Heart.png')

HEART = get_img('assets/Other/HeartNoBorder.png')

TRACK = get_img('assets/Other/Track.png')
TRACK_INIT = (0, 345)

CLOUD = get_img('assets/Other/Cloud.png')

BLACK = (0,0,0)

#SOUNDS
HIT = pygame.mixer.Sound('assets/Sounds/hit.wav')
JUMP = pygame.mixer.Sound('assets/Sounds/dinojump.wav')
UPGRADE = pygame.mixer.Sound('assets/Sounds/upgrade.wav')
CLICK = pygame.mixer.Sound('assets/Sounds/buttonclick.wav')
COINGET = pygame.mixer.Sound('assets/Sounds/coinget.wav')

class Pterodactyl:
    def __init__(self):
        self.sprite = PTERODACTYL
        self.position = pygame.Vector2()
        self.position.xy = 1050, -100


class Cloud:
    def __init__(self):
        self.sprite = CLOUD
        self.position = pygame.Vector2()
        self.position.xy = random.randint(1100, 2100), random.randint(100,300)

class Coin:
    def __init__(self):
        self.sprite = COIN
        self.position = pygame.Vector2()
        self.position.xy = random.randint(1300, 2000), 200

class Button():
    def __init__(self, num):
        self.type = num
        self.sprite = BUTTON
        self.position = pygame.Vector2()
        self.position.xy = 20 + num*(15 + BUTTON.get_width()), 400

    def on_click(self):
        print('a')

def main():
    pygame.display.set_caption("Dinosaur Game+")
    pygame.display.set_icon(PLAYER[0])
    
    score = 0
    high_score = 0
    timer = 0
    fly_cost = 10
    jump_cost = 5
    life_cost = 15
    lives = 1
    flying = False
    dbl = False

    font_big = pygame.font.Font('assets/Font/PressStart2P-Regular.ttf', 32)
    font_small = pygame.font.Font('assets/Font/PressStart2P-Regular.ttf', 16)
    gameover = font_big.render('G A M E  O V E R', True, BLACK)
    player = Player(PLAYER)
    cactuses = [Cactus(CACTUS, CACTUS_INIT), Cactus(CACTUS, CACTUS_INIT)]
    pterodactyl = Pterodactyl()
    clouds = [Cloud(), Cloud(), Cloud()]
    buttons = [Button(0), Button(1), Button(2)]
    coin = Coin()
    money = 0
    dead = False

    y_velocity = 0
    acceleration = 0.1
    run_state = True
    curr_ground = False
    ducking = False

    access_token = "5cfe2e7b959d22"
    open_key = "43b4772e7b571175690a6242764876ea"
    open_url = "https://api.openweathermap.org/data/2.5/weather?lat="

    handler = ipinfo.getHandler(access_token)
    details = handler.getDetails()

    location = details.loc
    x = location.split(',')

    ro = requests.get(open_url + x[0] + "&lon=" + x[1] + "&appid=" + open_key)
    curr_weather = ro.json()["weather"][0]["main"]
    BG_COLOR = get_bg_color(curr_weather)

    fly_timer = 0
    jump_timer = 0
    has_dbl = False
    timer = 0
    #Start up screen
    while timer < 1000:
        timer += 1
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                sys.exit()

        DISPLAY.fill(BG_COLOR)
        startMessage = font_big.render("DICKSON NGAN", True, (0,0,0))
        DISPLAY.blit(startMessage, (DISPLAY.get_width()/2 - startMessage.get_width()/2, DISPLAY.get_height()/2 - startMessage.get_height()/2))
            
        pygame.display.update()
        pygame.time.delay(2)

    titleScreen = True
    
    # title screen
    while titleScreen:
        mouseX,mouseY = pygame.mouse.get_pos()  
        mouse_clicked = False
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_clicked = True
            # if the player quits
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
        if (mouse_clicked and check_collide(mouseX, mouseY, 3, 3, DISPLAY.get_width()/2 - START.get_width()/2, 277, START.get_width(), START.get_height())):
            pygame.mixer.Sound.play(CLICK)
            mouse_clicked = False
            titleScreen = False

        DISPLAY.fill(BG_COLOR)
        # draw fake title background
        pygame.draw.rect(DISPLAY, (255, 240, 201), (0, TRACK_INIT[1] + 10, 1000, 150))
        DISPLAY.blit(CLOUD, (650, 200))
        DISPLAY.blit(CLOUD, (225, 100))
        DISPLAY.blit(TRACK, (TRACK_INIT[0], TRACK_INIT[1]))
        DISPLAY.blit(CACTUS[1], (700,275))

        logo = font_big.render("DinoRun+", True, (0,0,0))
        DISPLAY.blit(logo, (DISPLAY.get_width()/2 - logo.get_width()/2, DISPLAY.get_height()/2 - logo.get_height()/2 + math.sin(time.time()*5)*5 - 25)) 
        DISPLAY.blit(START, (DISPLAY.get_width()/2 - START.get_width()/2, 277))
        startMessage = font_small.render("START", True, (0, 0, 0))
        DISPLAY.blit(startMessage, (DISPLAY.get_width()/2 - startMessage.get_width()/2, 292))

        pygame.display.update()
        pygame.time.delay(10)

    grounds = [Ground(TRACK, TRACK_INIT), Ground(TRACK, TRACK_INIT )]
    grounds[0].position.x = 0
    grounds[1].position.x = grounds[1].sprite.get_width()
    timer = 0
    # game loop
    while True:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_clicked = False
        key_clicked = False
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
                mouse_clicked = True
            if (event.type == pygame.KEYDOWN):
                key_clicked = True
        pygame.display.update()
        # draw background
        DISPLAY.fill(BG_COLOR)
        pygame.draw.rect(DISPLAY, (255, 240, 201), (0, TRACK_INIT[1] + 10, 1000, 150))
        #draw shapes
        if not dead:
            score = timer // 20
        money_display = font_big.render("x {:02d}".format(money), True, BLACK)
        score_display = font_big.render("{:05d}".format(score), True, BLACK)
        lives_display = font_big.render("x {:02d}".format(lives), True, BLACK)
        DISPLAY.blit(grounds[0].sprite, (grounds[0].position.x, grounds[0].position.y))
        DISPLAY.blit(grounds[1].sprite, (grounds[1].position.x, grounds[1].position.y))
        DISPLAY.blit(coin.sprite, coin.position.xy)
        for c in clouds:
            DISPLAY.blit(c.sprite, (c.position.x, c.position.y))
        if not dead:
            if flying:
                DISPLAY.blit(player.fly_sprite[run_state], player.position.xy)
            elif ducking:
                player.position.y = player.position_init[1] + 30
                DISPLAY.blit(player.duck_sprite[run_state], player.position.xy)
            else:
                if player.position.y > player.position_init[1]:
                    player.position.y = player.position_init[1]
                DISPLAY.blit(player.sprite[run_state], player.position.xy)
        for c in cactuses:
            DISPLAY.blit(c.sprite, (c.position.xy))
            #check collision between player and cactus
            if check_collide(player.position.x, player.position.y, player.sprite[0].get_width()-10, player.sprite[0].get_height()-40,c.position.x, c.position.y, c.sprite.get_width(), c.sprite.get_height()) and timer > 10 and dead == False:
                pygame.mixer.Sound.play(HIT)
                lives -= 1
                if lives >= 1:
                    c.position.x = -100
                else:
                    dead = True

        DISPLAY.blit(pterodactyl.sprite[(timer//50)%2], (pterodactyl.position.xy))
        if high_score > 0:
            DISPLAY.blit(font_big.render("HI {:05d}".format(high_score), True, BLACK), (545, 20))
        DISPLAY.blit(coin.sprite, (20, 17))
        DISPLAY.blit(money_display, (80, 20))
        DISPLAY.blit(score_display, (825, 20))
        DISPLAY.blit(HEART, (790, 450))
        DISPLAY.blit(lives_display, (850, 450))
        #check collision between player and pterodactyl
        if check_collide(player.position.x, player.position.y + 20, player.sprite[0].get_width()-10, player.sprite[0].get_height()-40,pterodactyl.position.x, pterodactyl.position.y, pterodactyl.sprite[0].get_width(), pterodactyl.sprite[0].get_height()) and timer > 10 and dead == False:
            pygame.mixer.Sound.play(HIT)
            lives -= 1
            if lives >= 1:
                pterodactyl.position.x = -100
            else:
                dead = True


        #Draw buttons and update cost
        jmp_display = font_big.render("{:02d}".format(jump_cost), True, BLACK)
        life_display = font_big.render("{:02d}".format(life_cost), True, BLACK)
        fly_display = font_big.render("{:02d}".format(fly_cost), True, BLACK)
        for b in buttons:
            DISPLAY.blit(b.sprite, (b.position.xy))
            DISPLAY.blit(COIN, (b.position.x + 15, b.position.y + 40))
            if b.type == 0:
                DISPLAY.blit(BUTTON_JUMP, (b.position.x - 5, b.position.y - 5))
                DISPLAY.blit(jmp_display, (b.position.x + 51, b.position.y + 42))
            elif b.type == 2:
                DISPLAY.blit(BUTTON_HEART, (b.position.x - 5, b.position.y - 5))
                DISPLAY.blit(life_display, (b.position.x + 51, b.position.y + 42))
            elif b.type == 1:
                DISPLAY.blit(BUTTON_FLY, (b.position.x - 5, b.position.y - 5))
                DISPLAY.blit(fly_display, (b.position.x + 51, b.position.y + 42))
            
        #check collision between player and coins
        if check_collide(player.position.x, player.position.y, player.sprite[0].get_height(), player.sprite[0].get_height(), coin.position.x, coin.position.y, coin.sprite.get_width(), coin.sprite.get_height()) and dead == False:
            money += 1
            pygame.mixer.Sound.play(COINGET)
            coin = Coin()

        #reset from game over
        if dead:
            fly_timer = 0
            jump_timer = 0
            if score > high_score:
                    high_score = score
            if ducking:
                player.position.y = player.position_init[1]
            else:
                DISPLAY.blit(player.dead_sprite, ((player.position.x, player.position.y)))
            DISPLAY.blit(gameover, (250, 150))
            DISPLAY.blit(RESET, (RESET_INIT[0],RESET_INIT[1]))
            if (check_collide(mouse_x, mouse_y, 3, 3, RESET_INIT[0], RESET_INIT[1], RESET.get_width(), RESET.get_height()) and mouse_clicked):
                pygame.mixer.Sound.play(CLICK)
                lives = 1
                fly_cost = 10
                jump_cost = 5
                life_cost = 15
                money = 99
                for c in cactuses:
                    c.reset()
                for g in grounds:
                    g.reset()
                coin = Coin()
                pterodactyl = Pterodactyl()
                dead = not dead
                timer = 0
                grounds[0].position.x = 0
                grounds[1].position.x = grounds[1].sprite.get_width()
                curr_ground = False
                player.position.xy = player.position_init[0], player.position_init[1]

        #buy upgrades
        for b in buttons:
            if mouse_clicked and check_collide(mouse_x, mouse_y, 3, 3, b.position.x, b.position.y, BUTTON.get_height() +30, BUTTON.get_width()+30) and not dead:
                if b.type == 0 and jump_cost <= money and jump_timer == 0 and fly_timer == 0:
                    pygame.mixer.Sound.play(CLICK)
                    money -= jump_cost
                    jump_cost = round(jump_cost*1.5)
                    if jump_cost >= 100:
                        jump_cost = 99
                    print("BUY DBL")
                    jump_timer = 2000
                elif b.type == 1 and fly_cost <= money and fly_timer == 0 and jump_timer == 0:
                    pygame.mixer.Sound.play(CLICK)
                    money -= fly_cost
                    fly_cost = round(fly_cost*1.5)
                    if fly_cost >= 100:
                        fly_cost = 99
                    print("BUY FLY")
                    fly_timer = 4000
                elif b.type == 2 and life_cost <= money:
                    pygame.mixer.Sound.play(CLICK)
                    money -= life_cost
                    life_cost = round(life_cost*1.5)
                    if life_cost >= 100:
                        life_cost = 99
                    lives += 1
        
        if fly_timer > 0:
            flying = True
            fly_timer -= 1
            pygame.draw.rect(DISPLAY, BLACK, (buttons[1].position.x + 24, buttons[1].position.y + 8, 90*(fly_timer/4000), 5))
        else:
            flying = False

        if jump_timer > 0:
            dbl = True
            jump_timer -= 1
            pygame.draw.rect(DISPLAY, BLACK, (buttons[0].position.x + 24, buttons[0].position.y + 8, 90*(jump_timer/2000), 5))
        else:
            dbl = False

        #move grounds and clouds to imitate movement
        if not dead:
            grounds[0].position.x -= 4
            grounds[1].position.x -= 4
            pterodactyl.position.x -= 4
            coin.position.x -= 4
            for c in clouds:
                c.position.x -= 2
                if c.position.x <= -100:
                    c.position.xy = random.randint(1000, 4000),random.randint(50, 300)
            for c in cactuses:
                c.position.x -= 4
            if not flying:
                player.position.y += y_velocity
                y_velocity += acceleration

        #jumping and flying
        if not flying:
            if (key_clicked) and not has_dbl and dbl and not dead:
                has_dbl = True
                y_velocity = -5.5
                pygame.mixer.Sound.play(JUMP)
            if player.position.y >= player.position_init[1]:
                y_velocity = 0
                has_dbl = False
            if (keys[pygame.K_SPACE] or keys[pygame.K_UP]) and (player.position.y >= player.position_init[1]) and not dead:
                y_velocity = -5.5
                pygame.mixer.Sound.play(JUMP)
        else:
            if player.position.y > player.position_init[1]:
                y_velocity = 0
            elif (keys[pygame.K_DOWN]):
                player.position.y += 2
            if player.position.y <= 0:
                y_velocity = 0
            elif (keys[pygame.K_UP]):
                player.position.y += -2

        #ducking
        if (player.position.y == player.position_init[1] or player.position.y == player.position_init[1] + 30) and keys[K_DOWN]:
            ducking = True
        else:
            ducking = False
        
        #change between running sprites
        if timer%25 == 0 and (player.position.y >= player.position_init[1] or flying) and not dead:
            run_state = not run_state
            
        #change between tracks
        if (timer*4)%grounds[0].sprite.get_width() == 0 and timer != 0 and not dead:
            grounds[curr_ground].position.x += 2*grounds[0].sprite.get_width()
            curr_ground = not curr_ground

        #create cactuses
        if timer%100 == 0: 
            for c in cactuses:
                if c.position.x < -500:
                    if c == cactuses[0]:
                        c.position.x = random.randint(1050, 1500)
                    else:
                        c.position.x = random.randint(1500, 1800)
                    c.change_sprite(CACTUS)
                    DISPLAY.blit(c.sprite, (c.position.x, c.position.y))
                    break

        #create pterodactyls
        if timer%100 == 0 and score > 500:
            if pterodactyl.position.x < -300:
                pterodactyl.position.x = 2100
                pterodactyl.position.y = random.randint(50,150)

        
        #create coins
        if timer%random.randint(100,1000) == 0:
            if coin.position.x < -100:
                coin.position.x = 1050

        
        timer += 1

        pygame.display.update()
        
        pygame.time.delay(4)
main()