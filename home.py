import pygame

class Home(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('./assets/home.png')
        self.rect = self.image.get_rect(center = (x, y))
        self.active = False

    def update(self, py_events):
        for event in py_events:
            if event.type == pygame.MOUSEMOTION:
                if self.rect.collidepoint(pygame.mouse.get_pos()):
                    self.active = True
                    self.image = pygame.image.load('./assets/home-active.png')
                else:
                    self.active = False
                    self.image = pygame.image.load('./assets/home.png')