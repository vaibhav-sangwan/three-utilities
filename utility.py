import pygame

class Utility(pygame.sprite.Sprite):
    def __init__(self, x, y, type, color):
        super().__init__()
        self.type = type
        self.color = color
        self.image = pygame.image.load('./assets/' + self.type + '.png')
        self.rect = self.image.get_rect(center = (x, y))
    
    def update(self, py_events):
        for event in py_events:
            if event.type == pygame.MOUSEMOTION:
                if self.rect.collidepoint(pygame.mouse.get_pos()):
                    self.image = pygame.image.load('./assets/' + self.type + '-active.png')
                else:
                    self.image = pygame.image.load('./assets/' + self.type + '.png')