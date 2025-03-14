import pygame
import os

BASE_IMG_PATH = 'data/images/'

def load_image(path):
    img = pygame.image.load(BASE_IMG_PATH + path).convert_alpha()
    # can't stack the cards if you set a colorkey
    # img.set_colorkey((0, 0, 0))
    return img

def load_images(path):
    images = []
    for img_name in os.listdir(BASE_IMG_PATH + path):
        images.append(load_image(path + '/' + img_name))
    return images

def debug(screen, font, info, x = 10, y = 10):
    debug_surf = font.render(str(info), True, 'white')
    debug_rect = debug_surf.get_rect(topleft=(x, y))
    screen.blit(debug_surf, debug_rect)