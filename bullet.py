import pygame

class Bullet:
    def __init__(self, x, y, speed, damage=1):
        self.rect = pygame.Rect(x, y, 10, 5)
        self.speed = speed
        self.damage = damage

    def update(self):
        self.rect.x += self.speed

    def draw(self, screen, bullet_img):
        screen.blit(bullet_img, self.rect.topleft)


class SpecialBullet(Bullet):
    def __init__(self, x, y, speed):
        super().__init__(x, y, speed)
        self.rect = pygame.Rect(x, y, 15, 10)  # Larger bullet
        self.damage = 5  # Special bullets do more damage

    def draw(self, screen, special_bullet_img):
        screen.blit(special_bullet_img, self.rect.topleft)

    def update(self):
        self.rect.x += self.speed

class ShotgunBullet(Bullet):
    def __init__(self, x, y, direction, speed):
        super().__init__(x, y, speed)
        self.rect = pygame.Rect(x, y, 15, 10)
        self.speed = speed
        self.direction = direction
        self.damage = 2  # Can customize damage

        # Set different angles for spread (in degrees or simulated via offset)
        self.spread = [(0, 0), (10, -10), (10, 10)]  # Simulate 3-way shot

    def update(self):
        self.rect.x += self.speed * self.direction

    def draw(self, screen, shotgun_bullet_img):
        screen.blit(shotgun_bullet_img, self.rect.topleft)
