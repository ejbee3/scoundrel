import sys
import pygame

from pygame.locals import *

from scripts.utils import load_image, load_images
from scripts.entities import Deck, Button


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('scoundrel')
        self.SCALE_FACTOR = 2

        self.DISPLAY_WIDTH = 400
        self.DISPLAY_HEIGHT = 300
        self.display = pygame.Surface((self.DISPLAY_WIDTH, self.DISPLAY_HEIGHT))

        self.SCREEN_WIDTH = self.DISPLAY_WIDTH * self.SCALE_FACTOR
        self.SCREEN_HEIGHT = self.DISPLAY_HEIGHT * self.SCALE_FACTOR
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        
        self.clock = pygame.time.Clock()
        self.small_font = pygame.font.Font('font/yoster.ttf', 12)
        self.large_font = pygame.font.Font('font/yoster.ttf', 24)

        self.assets = {
            'diamonds': load_images('diamonds'),
            'clubs': load_images('clubs'),
            'hearts': load_images('hearts'),
            'spades': load_images('spades'),
            'back': load_image('card_back.png'),
            'no_cards': load_image('no_cards.png'),
            'health_heart': load_image('health_heart.png')
        }

        self.deck = Deck([self.assets['clubs'], self.assets['diamonds'], self.assets['hearts'], self.assets['spades']])
        self.card = self.deck.draw()
        self.weapon_text = Button((int(self.DISPLAY_WIDTH * 0.75), 20), self.small_font, 'Weapon', 'white')
        self.room_offset = 50
        self.hp = 20


    def run(self):
        while True:
            # event queue
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                if event.type == MOUSEBUTTONDOWN:
                    # left click
                    if event.button == 1:
                        mx, my = pygame.mouse.get_pos()
                        if card_back_rect.collidepoint((mx // self.SCALE_FACTOR, my // self.SCALE_FACTOR)):
                            self.room_offset = 50
                            # draw cards until you have 4
                            while(len(self.deck.drawn) < 4):
                                card = self.deck.draw()
                                self.deck.drawn.append((card, (self.room_offset, int(self.DISPLAY_HEIGHT * 0.75))))
                                self.room_offset += 75

            # update/render
            self.display.fill((0, 0, 0))
            # draw from deck image and empty
            stack_pos = (self.DISPLAY_WIDTH // 2, 40)
            card_back_rect = self.assets['back'].get_rect(center=stack_pos)
            if len(self.deck.stack) == 0:
                self.display.blit(self.assets['no_cards'], self.assets['no_cards'].get_rect(center=stack_pos))
            else:
                self.display.blit(self.assets['back'], card_back_rect)

            # hearts
            heart_pos = (40, 40)
            self.display.blit(self.assets['health_heart'], self.assets['health_heart'].get_rect(center=heart_pos))
            hp_display = Button((80, 40), self.large_font, str(self.hp), 'red')
            hp_display.render(self.display)

            # weapon slot
            self.weapon_text.render(self.display)
            box_offset = (self.weapon_text.rect.centerx - self.weapon_text.rect.left) * 2
            text_center_x = self.weapon_text.rect.centerx
            pygame.draw.lines(self.display, (255, 255, 255), True, [(text_center_x - box_offset, 10), (text_center_x + box_offset, 10), (text_center_x + box_offset, int(self.DISPLAY_HEIGHT * 0.4)), (text_center_x - box_offset, int(self.DISPLAY_HEIGHT * 0.4))], 2)
            
            if len(self.deck.drawn) == 4:
                for card, pos in self.deck.drawn:
                    card.rect = card.img.get_rect(center=pos)
                    self.display.blit(card.img, card.rect)

            # debug(self.display, self.font, pygame.mouse.get_pos())
            # debug(self.display, self.font, (card_back_rect.topleft, card_back_rect.width, card_back_rect.height), 10, 40)     
                    
            # have to blit the render display to the original screen size  
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            
            # print(pygame.mouse.get_pos())
            pygame.display.update()
            # for simplicity, we won't use deltatime
            self.clock.tick(60)


Game().run()
