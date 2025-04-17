import pygame
from constants import GREEN

class Platform:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, screen, image=None):
        if image:
            screen.blit(image, self.rect)
        else:
            pygame.draw.rect(screen, GREEN, self.rect)
