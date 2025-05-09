import pygame

class HealthPickup:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class ShotgunBulletPickup:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = pygame.Rect(x, y, 20, 20)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class SpecialBulletPickup:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 20, 20)
        self.color = (0, 0, 255)  # blue color for pickup

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
