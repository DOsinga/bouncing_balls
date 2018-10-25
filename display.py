import pygame

class Display():
    def __init__(self, title, width, height, delay=30):
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)
        self.delay = delay

    def clear(self):
        self.screen.fill((0, 0, 0))

    def circle(self, color, center, radius):
        pygame.draw.circle(self.screen, color, center, radius)

    def flip(self):
        pygame.display.flip()
