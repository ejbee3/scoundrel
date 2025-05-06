import random
import pygame

class Card(pygame.sprite.Sprite):
    def __init__(self, image, value, suit):
        super().__init__()
        self.image = image
        self.value = value
        self.suit = suit
        self.rect = None
        self.pos = None
    

class Deck:
    def __init__(self, card_imgs_by_suit):
        self.stack = []
        self.drawn = []
        self.suits = ['clubs', 'diamonds', 'hearts', 'spades']

        for i in range(len(self.suits)):
            if self.suits[i] == 'clubs' or self.suits[i] == 'spades':
                for j in range(2, 15):
                    self.stack.append(Card(card_imgs_by_suit[i][j - 2], j, self.suits[i]))
            else:
                for j in range(2, 11):
                    self.stack.append(Card(card_imgs_by_suit[i][j - 2], j, self.suits[i]))

        random.shuffle(self.stack)

    def draw(self):
        return self.stack.pop()


class Button:
    def __init__(self, center, font, text, text_color):
        self.surf = font.render(text, True, text_color)
        self.rect = self.surf.get_rect(center=center)

    def render(self, screen):
        screen.blit(self.surf, self.rect)
    
    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)
    

