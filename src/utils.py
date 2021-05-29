import pygame

CLOUD_BG = (77,144,142)
RAIN_BG = (87,117,144)
CLEAR_BG = (193,255,145) 
SNOW_BG = (39,125,161)

def get_img(file_name):
    return pygame.Surface.convert_alpha(pygame.image.load(file_name))

def check_collide(a_x, a_y, a_width, a_height, b_x, b_y, b_width, b_height):
    return (a_x + a_width >= b_x) and (a_x <= b_x + b_width) and (a_y + a_height >= b_y) and (a_y <= b_y + b_height)

def get_bg_color(weather):
    return {
        "Clouds":CLOUD_BG,
        "Thunderstorm":RAIN_BG,
        "Drizzle":RAIN_BG,
        "Rain":RAIN_BG,
        "Snow":SNOW_BG,
        "Clear":CLEAR_BG,
        "Mist":CLEAR_BG,
        "Smoke":CLOUD_BG,
        "Haze":CLOUD_BG,
        "Dust":CLOUD_BG,
        "Fog": CLOUD_BG,
        "Sand":CLEAR_BG,
        "Ash":CLOUD_BG,
        "Tornado":RAIN_BG
    }[weather]
