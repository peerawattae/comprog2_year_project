import pygame
import random
from constants import ENEMY_BULLET_SPEED
from bullet import Bullet
from health_pickup import HealthPickup, ShotgunBulletPickup

class Enemy:
    def __init__(self, x, y, platform, special=False, shotgun=False):
        self.rect = pygame.Rect(x, y, 40, 50)
        self.health = 1 if not special or shotgun else 5
        self.shoot_timer = random.randint(1000, 3000)
        self.last_shot = pygame.time.get_ticks()
        self.special = special
        self.shotgun = shotgun
        self.speed = 2 if not special else 1  # Special enemies move slower
        self.direction = 1  # Start moving right
        self.platform = platform  # Store platform reference

    def move(self):
        """Move enemy left and right within its platform boundaries."""
        self.rect.x += self.speed * self.direction

        # Change direction when reaching platform edges
        if self.rect.right >= self.platform.rect.right or self.rect.left <= self.platform.rect.left:
            self.direction *= -1  # Reverse direction

    def shoot(self, enemy_bullets):
        """Shoot in the direction the enemy is facing."""
        if pygame.time.get_ticks() - self.last_shot > self.shoot_timer:
            bullet_speed = ENEMY_BULLET_SPEED * self.direction  # Bullets move based on direction
            enemy_bullets.append(Bullet(self.rect.centerx, self.rect.centery, bullet_speed))
            self.last_shot = pygame.time.get_ticks()

    def drop_health(self, health_img):
        """20% chance to drop health."""
        if random.random() < 0.2:
            return HealthPickup(self.rect.centerx, self.rect.centery, health_img)
        return None


    def draw(self, screen, enemy_img):
        """Draw the enemy on screen."""
        screen.blit(enemy_img, self.rect.topleft)

    def hit(self, bullets, special_bullets, shotgun_bullets, health_items, health_image):
        """Check if the enemy is hit by a bullet."""
        for bullet in bullets[:]:
            if self.rect.colliderect(bullet.rect):
                bullets.remove(bullet)
                self.health -= 1
                if self.health <= 0:
                    health_item = self.drop_health(health_image)  # Drop health item if the enemy dies
                    if health_item:
                        health_items.append(health_item)
                    return True  # Enemy is dead

        for bullet in special_bullets[:]:
            if self.rect.colliderect(bullet.rect):
                special_bullets.remove(bullet)
                self.health -= bullet.damage  # Special bullets do more damage
                if self.health <= 0:
                    return True  # Enemy is dead

        for bullet in shotgun_bullets[:]:
            if self.rect.colliderect(bullet.rect):
                shotgun_bullets.remove(bullet)
                self.health -= bullet.damage
                if self.health <= 0:
                    return True

        return False

class SpecialEnemy(Enemy):
    def __init__(self, x, y, platform):
        super().__init__(x, y, platform, special=True)
        self.health = 5

    def draw(self, screen, special_img):
        screen.blit(special_img, self.rect.topleft)

class ShotgunEnemy(Enemy):
    def __init__(self, x, y, platform):
        super().__init__(x, y, platform, special=True)
        self.health = 3  # Lower HP
        self.shoot_spread = [-2, 0, 2]  # Bullets spread out
        self.shoot_timer = random.randint(800, 2000)  # Shoots faster

    def move(self):
        self.rect.x += self.speed * self.direction

        # Reverse direction if hitting platform edges
        if self.rect.left <= self.platform.rect.left or self.rect.right >= self.platform.rect.right:
            self.direction *= -1  # Change direction

    def shoot(self, enemy_bullets):
        """Shoot 3 bullets in a spread pattern: center, top-right, bottom-right."""
        if pygame.time.get_ticks() - self.last_shot > self.shoot_timer:
            # Define the spread directions (center, top-right, bottom-right)
            spread_offsets = [(0, 0), (10, -10), (10, 10)]  # (x, y) offsets for each bullet

            for offset in spread_offsets:
                # Calculate the bullet's position based on the offsets
                x_offset, y_offset = offset
                bullet_speed = ENEMY_BULLET_SPEED * self.direction

                # Create bullet at the enemy's position with the calculated offset
                bullet = Bullet(self.rect.centerx + x_offset, self.rect.centery + y_offset, bullet_speed)
                enemy_bullets.append(bullet)

            # Update last shot time
            self.last_shot = pygame.time.get_ticks()

    def drop_loot(self, health_img, shotgun_img):
        loot = []

        # 20% chance to drop health
        if random.random() < 0.2:
            loot.append(HealthPickup(self.rect.centerx, self.rect.centery, health_img))

        loot.append(ShotgunBulletPickup(self.rect.centerx, self.rect.centery, shotgun_img))
        return loot


    def draw(self, screen, shotgun_enemy_img):
        """Draw the shotgun enemy with its specific image."""
        screen.blit(shotgun_enemy_img, self.rect.topleft)
