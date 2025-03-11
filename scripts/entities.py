import random

class Card:
    def __init__(self, img, value, suit):
        self.img = img
        self.value = value
        self.suit = suit
        self.rect = None
    

class Deck:
    def __init__(self, card_imgs_by_suit):
        self.stack = []
        self.discarded = []
        self.drawn = []
        self.suits = ['clubs', 'diamonds', 'hearts', 'spades']

        for i in range(len(self.suits)):
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
    

