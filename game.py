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

        self.WHITE = (255, 255, 255)
        
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
        self.weapon_text = Button((int(self.DISPLAY_WIDTH * 0.75), 20), self.small_font, 'Weapon', 'white')
        self.arena = {
            'weapon': pygame.sprite.GroupSingle(),
            'monsters': pygame.sprite.Group()
        }
        self.keep = {
            'kept_card': None,
            'index': 0
        }
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
                    mouse_pos = tuple(pos // self.SCALE_FACTOR for pos in pygame.mouse.get_pos())
                    # left click
                    if event.button == 1:
                        # if clicking on deck
                        if card_back_rect.collidepoint(mouse_pos):
                            if len(self.deck.drawn) > 0:
                                self.deck.drawn.clear()
                            room_offset = 75
                            # draw cards until you have 4
                            i = 0
                            kept = self.keep['kept_card']
                            kept_i = self.keep['index']
                            while(len(self.deck.drawn) != 4):
                                if kept and i == kept_i:
                                    kept.pos = (room_offset + (room_offset * i), int(self.DISPLAY_HEIGHT * 0.75))
                                    self.deck.drawn.append(kept)
                                else:
                                    card = self.deck.draw()
                                    card.pos = (room_offset + (room_offset * i), int(self.DISPLAY_HEIGHT * 0.75))
                                    self.deck.drawn.append(card)
                                i += 1
                            if kept:
                                for i, card in enumerate(self.deck.drawn):
                                    if card.image == kept.image:
                                        # swap positions
                                        kept_el = self.deck.drawn[i]
                                        swapped_el = self.deck.drawn[kept_i]
                                        kept_el.pos = (room_offset + (room_offset * kept_i), int(self.DISPLAY_HEIGHT * 0.75))
                                        swapped_el.pos = (room_offset + (room_offset * i), int(self.DISPLAY_HEIGHT * 0.75))
                                        # swap positions in list
                                        self.deck.drawn[i], self.deck.drawn[kept_i] = self.deck.drawn[kept_i], self.deck.drawn[i]
                                        break
                            self.keep['kept_card'] = None
                            self.keep['index'] = 0       
                        else:
                            # else you're clicking on cards
                            for card in self.deck.drawn:
                                if card.rect.collidepoint(mouse_pos):
                                    if not self.arena['weapon']:
                                        if card.suit == self.deck.suits[1]:
                                            card.rect.center = (self.weapon_text.rect.left, self.weapon_text.rect.top + 40)
                                            self.arena['weapon'].add(card)
                                        # fighting barehanded (take full damage)   
                                        if card.suit == self.deck.suits[0] or card.suit == self.deck.suits[3]:
                                            self.hp -= card.value
                                            self.deck.discarded += 1
                                    else:
                                        if card.suit == self.deck.suits[1]:
                                            card.rect.center = (self.weapon_text.rect.left, self.weapon_text.rect.top + 40)
                                            self.arena['weapon'].add(card)
                                            self.deck.discarded += len(self.arena['monsters']) + 1
                                            self.arena['monsters'].empty()
                                        if card.suit == self.deck.suits[0] or card.suit == self.deck.suits[3]:
                                             # weapon already equipped, find offset amt
                                            offset = len(self.arena['monsters']) + 1
                                            wpn = self.arena['weapon'].sprite
                                            card.rect.center = tuple(x + (7 * offset) for x in wpn.rect.center)
                                            self.arena['monsters'].add(card)
                                            if wpn.value < card.value:
                                                self.hp -= abs(wpn.value - card.value)
                                        
                                    # you have to remove the card from the drawn list or else it won't display properly!  
                                    self.deck.drawn.remove(card)
                    # right click
                    if event.button == 3:
                        # keep mechanic
                        if self.keep['kept_card']:
                            self.keep['kept_card'] = None
                            self.keep['index'] = 0  
                        else:
                            for i, card in enumerate(self.deck.drawn):
                                if card.rect.collidepoint(mouse_pos):
                                    # update keep with card and info
                                    self.keep['kept_card'] = card
                                    self.keep['index'] = i


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
            pygame.draw.lines(self.display, self.WHITE, True, [(text_center_x - box_offset, 10), (text_center_x + box_offset, 10), (text_center_x + box_offset, int(self.DISPLAY_HEIGHT * 0.4)), (text_center_x - box_offset, int(self.DISPLAY_HEIGHT * 0.4))], 2)
            # show weapon card and monsters
            if self.arena['weapon']:
                self.arena['weapon'].draw(self.display)
                
            if len(self.arena['monsters']) > 0:
                self.arena['monsters'].draw(self.display)

            cards_left = Button((100, int(self.DISPLAY_HEIGHT // 3)), self.small_font, f'cards left: {len(self.deck.stack)}', 'white')
            cards_left.render(self.display)
                
            for card in self.deck.drawn:
                card.rect = card.image.get_rect(center=card.pos)
                kept = self.keep['kept_card']
                if kept and kept.image == card.image:
                    pygame.draw.lines(self.display, self.WHITE, True, [(card.rect.left - 1, card.rect.top - 1), (card.rect.right + 1, card.rect.top - 1), (card.rect.right + 1, card.rect.bottom + 1), (card.rect.left - 1, card.rect.bottom + 1)])
                self.display.blit(card.image, card.rect)

            # debug(self.display, self.font, pygame.mouse.get_pos())
            # debug(self.display, self.font, (card_back_rect.topleft, card_back_rect.width, card_back_rect.height), 10, 40)     
                    
            # have to blit the render display to the original screen size -- scale up 2x
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            
            # print(pygame.mouse.get_pos())
            pygame.display.update()
            # for simplicity, we won't use deltatime
            self.clock.tick(60)


Game().run()
