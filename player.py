import pygame
from constants import PLAYER_SPEED, JUMP_STRENGTH, GRAVITY, BULLET_SPEED, RELOAD_TIME, WHITE
from bullet import Bullet, SpecialBullet, ShotgunBullet
from collect_data import GameDataCollector


class Player:
    def __init__(self, x, y, right_img, left_img, data_collector):
        self.rect = pygame.Rect(x, y, 40, 50)
        self.health = 5
        self.magazine = 6
        self.last_reload = 0
        self.vel_y = 0
        self.on_ground = False
        self.score = 0
        self.special_bullet = False
        self.has_shotgun_bullet = False
        self.dropping = False  # Flag for dropping through platforms
        self.facing_right = True  # Track player's facing direction
        # Player images for both directions
        self.right_img = right_img
        self.left_img = left_img
        self.collect_data = data_collector

    def move(self, keys):
        if keys[pygame.K_a]:  # Move left
            self.rect.x -= PLAYER_SPEED
            self.facing_right = False  # Turn left
        if keys[pygame.K_d]:  # Move right
            self.rect.x += PLAYER_SPEED
            self.facing_right = True  # Turn right
        if keys[pygame.K_w] and self.on_ground:
            self.vel_y = -JUMP_STRENGTH
            self.on_ground = False
        if keys[pygame.K_s]:
            self.dropping = True
        else:
            self.dropping = False

        # Prevent moving beyond the left side of the screen
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self, bullets):
        if self.magazine > 0:
            bullet_x = self.rect.right if self.facing_right else self.rect.left - 10
            bullet_y = self.rect.centery - 5
            bullet_speed = BULLET_SPEED if self.facing_right else -BULLET_SPEED
            bullets.append(Bullet(bullet_x, bullet_y, bullet_speed))
            self.magazine -= 1
        elif self.magazine == 0 and pygame.time.get_ticks() - self.last_reload > RELOAD_TIME:
            self.magazine = 6
            self.last_reload = pygame.time.get_ticks()
            self.collect_data.record_reload()

    def shoot_special(self, special_bullets):
        """Fires a strong single special bullet."""
        if self.special_bullet:
            bullet_x = self.rect.right if self.facing_right else self.rect.left - 15
            bullet_y = self.rect.centery - 5
            bullet_speed = BULLET_SPEED * 1.5 if self.facing_right else -BULLET_SPEED * 1.5
            special_bullets.append(SpecialBullet(bullet_x, bullet_y, bullet_speed))
            self.special_bullet = False
            return True
        return False

    def shoot_shotgun(self, special_bullets):
        """Fires a 3-way shotgun bullet."""
        if self.has_shotgun_bullet:
            spread_offsets = [(0, 0), (10, -10), (10, 10)]
            direction = 1 if self.facing_right else -1
            bullet_speed = BULLET_SPEED * 0.5 if self.facing_right else -BULLET_SPEED * 0.5
            for offset in spread_offsets:
                bullet = ShotgunBullet(
                    self.rect.centerx,
                    self.rect.centery + offset[1],
                    (bullet_speed + offset[0]) * direction,
                    bullet_speed
                )
                special_bullets.append(bullet)
            self.has_shotgun_bullet = False  # Remove this if you want shotgun to persist
            return True
        return False

    def apply_gravity(self, platforms, ground_rect):
        self.vel_y += GRAVITY
        self.rect.y += self.vel_y
        self.on_ground = False  # Assume the player is not on the ground

        # Check collision with the ground
        if self.rect.colliderect(ground_rect):
            self.rect.bottom = ground_rect.top
            self.vel_y = 0
            self.on_ground = True
            return

        # Check collision with platforms
        for platform in platforms:
            if self.rect.colliderect(platform.rect) and self.vel_y > 0:
                if not self.dropping:  # Allow dropping through platforms when holding 'S'
                    self.rect.bottom = platform.rect.top
                    self.vel_y = 0
                    self.on_ground = True
                break

    def draw(self, screen):
        # Choose the correct image based on direction
        player_img = self.right_img if self.facing_right else self.left_img
        screen.blit(player_img, self.rect.topleft)

    def draw_ui(self, screen, level, font, width, height, white_color, red_color):
        health_text = font.render(f"Health: {self.health}", True, white_color)
        ammo_text = font.render(f"Ammo: {self.magazine}/6", True, white_color)
        score_text = font.render(f"Score: {self.score}", True, white_color)
        level_text = font.render(f"Level: {level}", True, white_color)

        # Display special bullet status
        if self.special_bullet:
            special_text = font.render("Special Bullet Ready! Press K", True, (0, 255, 255))
            screen.blit(special_text, (10, 130))

        if self.has_shotgun_bullet:
            shotgun_text = font.render("Shotgun Bullet Ready! Press L", True, (255, 255, 0))
            screen.blit(shotgun_text, (10, 160))

        screen.blit(health_text, (10, 10))
        screen.blit(ammo_text, (10, 40))
        screen.blit(score_text, (10, 70))
        screen.blit(level_text, (10, 100))

        # Draw a visual indicator of the exit at the right edge
        pygame.draw.rect(screen, red_color, (width - 10, 0, 10, height))
        exit_text = font.render("EXIT", True, white_color)
        exit_text = pygame.transform.rotate(exit_text, 90)
        screen.blit(exit_text, (width - 30, height // 2 - 50))
