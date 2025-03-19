import sys
import pygame

from pygame.locals import *

from scripts.utils import load_image, load_images, debug
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
        self.defeated = 0


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
                    room_offset = 75
                    # left click
                    if event.button == 1:
                        # if clicking on deck
                        if card_back_rect.collidepoint(mouse_pos):
                            if len(self.deck.drawn) > 0:
                                self.deck.drawn.clear()
                            # draw cards until you have 4
                            kept = self.keep['kept_card']
                            if kept:
                                kept_index = self.keep['index']
                                print(kept_index)
                                kept.pos = (room_offset, int(self.DISPLAY_HEIGHT * 0.75))
                                self.deck.drawn.append(kept)
                                for i in range(1, 4):
                                    card = self.deck.draw()
                                    card.pos = (room_offset + (room_offset * i), int(self.DISPLAY_HEIGHT * 0.75))
                                    self.deck.drawn.append(card)
                                # kept_index = self.keep['index']
                                # print(kept_index)
                                if kept_index != 0:
                                    kept_card = self.deck.drawn[0]
                                    kept_card.pos = (room_offset + (room_offset * kept_index), int(self.DISPLAY_HEIGHT * 0.75))
                                    swapped_card = self.deck.drawn[kept_index]
                                    swapped_card.pos = (room_offset, int(self.DISPLAY_HEIGHT * 0.75))
                                    kept_card, swapped_card = swapped_card, kept_card
                            else:
                                for i in range(4):
                                    card = self.deck.draw()
                                    card.pos = (room_offset + (room_offset * i), int(self.DISPLAY_HEIGHT * 0.75))
                                    self.deck.drawn.append(card)      
                        else:
                            # else you're clicking on cards
                            if len(self.deck.drawn) > 0:
                                for card in self.deck.drawn:
                                    if card.rect.collidepoint(mouse_pos):
                                        # hearts
                                        if card.suit == self.deck.suits[2]:
                                                self.hp += card.value
                                                if self.hp > 20:
                                                    self.hp = 20
                                        if not self.arena['weapon']:
                                            if card.suit == self.deck.suits[1]:
                                                card.rect.center = (self.weapon_text.rect.left, self.weapon_text.rect.top + 40)
                                                self.arena['weapon'].add(card)
                                            # fighting barehanded (take full damage)   
                                            if card.suit == self.deck.suits[0] or card.suit == self.deck.suits[3]:
                                                self.hp -= card.value
                                                self.defeated += 1
                                        else:
                                            # diamonds
                                            if card.suit == self.deck.suits[1]:
                                                card.rect.center = (self.weapon_text.rect.left, self.weapon_text.rect.top + 40)
                                                self.arena['weapon'].add(card)
                                                self.arena['monsters'].empty()
                                            # clubs or spades
                                            if card.suit == self.deck.suits[0] or card.suit == self.deck.suits[3]:
                                                # weapon already equipped, find offset amt
                                                offset = len(self.arena['monsters']) + 1
                                                wpn = self.arena['weapon'].sprite
                                                card.rect.center = tuple(x + (7 * offset) for x in wpn.rect.center)
                                                self.arena['monsters'].add(card)
                                                if wpn.value < card.value:
                                                    self.hp -= abs(wpn.value - card.value)
                                                self.defeated += 1
                                        # you have to remove the card from the drawn list or else it won't display properly!  
                                        self.deck.drawn.remove(card)
                    # right click
                    if event.button == 3:
                        if card_back_rect.collidepoint(mouse_pos):
                            while(len(self.deck.drawn) > 0):
                                card = self.deck.drawn.pop()
                                card.rect = None
                                card.pos = None
                                self.deck.stack.insert(0, card)
                            for i in range(4):
                                card = self.deck.draw()
                                card.pos = (room_offset + (room_offset * i), int(self.DISPLAY_HEIGHT * 0.75))
                                self.deck.drawn.append(card)
                        # keep mechanic
                        for i, card in enumerate(self.deck.drawn):
                            if card.rect.collidepoint(mouse_pos):
                                if self.keep['kept_card']:
                                    self.keep['kept_card'] = None
                                    self.keep['index'] = 0
                                else:
                                    self.keep['kept_card'] = card
                                    self.keep['index'] = (card.pos[0] // room_offset) - 1
                                    print(self.keep['index'])
                                    
                                    
                                    


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

            cards_left = Button((100, int(self.DISPLAY_HEIGHT // 4)), self.small_font, f'cards left: {len(self.deck.stack)}', 'white')
            cards_left.render(self.display)

            monsters_slain = Button((100, int(self.DISPLAY_HEIGHT // 3)), self.small_font, f'monsters slain: {self.defeated}', 'white')
            monsters_slain.render(self.display)
                
            for card in self.deck.drawn:
                card.rect = card.image.get_rect(center=card.pos)
                if self.keep['kept_card'] and card.image == self.keep['kept_card'].image:
                    pygame.draw.lines(self.display, self.WHITE, True, [(card.rect.left - 1, card.rect.top - 1), (card.rect.right + 1, card.rect.top - 1), (card.rect.right + 1, card.rect.bottom + 1), (card.rect.left - 1, card.rect.bottom + 1)])
                self.display.blit(card.image, card.rect)

            # debug(self.display, self.small_font, pygame.mouse.get_pos())
            # debug(self.display, self.font, (card_back_rect.topleft, card_back_rect.width, card_back_rect.height), 10, 40)     
                    
            # have to blit the render display to the original screen size -- scale up 2x
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            
            # print(pygame.mouse.get_pos())
            pygame.display.update()
            # for simplicity, we won't use deltatime
            self.clock.tick(60)


Game().run()
