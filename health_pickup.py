import pygame

class HealthPickup:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 20, 20)
        self.color = (0, 255, 0)  # Green health pickup

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

class ShotgunBulletPickup:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 20, 20)
        self.color = (255, 100, 0)  # Orange color for pickup

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

class SpecialBulletPickup:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 20, 20)
        self.color = (0, 0, 255)  # blue color for pickup

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
