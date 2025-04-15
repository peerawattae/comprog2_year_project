import pygame
import random
from player import Player
from enemy import Enemy, SpecialEnemy
from bullet import Bullet, SpecialBullet
from game_platform import Platform
from health_pickup import HealthPickup, ShotgunBulletPickup
from level_generator import generate_level
from constants import GRAVITY, BULLET_SPEED, ENEMY_BULLET_SPEED, WHITE, RED, GREEN, BLUE, BLACK, YELLOW
from collect_data import GameDataCollector  # Import the data collection system
import csv
import os

DATA_FILE = "game_save.csv"

class Game:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.WIDTH = width
        self.HEIGHT = height
        self.FONT = pygame.font.Font(None, 36)

        # Initialize data collection
        self.data_collector = GameDataCollector()  # Ask whether to create a new save file

        # Load images
        self.load_images()

        # Create the ground rectangle
        self.ground_rect = pygame.Rect(0, self.HEIGHT - 20, self.WIDTH, 20)

        self.bg_x = 0  # Background position
        self.bg_speed = 2  # Scrolling speed

        # Initialize game objects
        self.player = Player(100, self.HEIGHT - 100, self.player_right_img, self.player_left_img, self.data_collector)
        self.state = 1
        self.enemies, self.platforms, self.health_items, self.special_enemies, self.shotgun_enemies = generate_level(self.state, self.WIDTH, self.HEIGHT)
        self.bullets = []
        self.enemy_bullets = []
        self.special_bullets = []
        self.shotgun_bullets = []
        self.game_over = False
        # Stats tracking
        self.points = 0
        self.special_pickups = 0
        self.times_shot = 0
        self.level_reached = 1

    def load_images(self):
        """Load game assets such as player, enemy, and background images."""
        try:
            self.player_right_img = pygame.image.load("/Users/salmon/work/comprog2/project/cowboy/game_photo/player_right.png").convert_alpha()
            self.player_right_img = pygame.transform.scale(self.player_right_img, (40, 50))

            self.player_left_img = pygame.image.load("/Users/salmon/work/comprog2/project/cowboy/game_photo/player_left.png").convert_alpha()
            self.player_left_img = pygame.transform.scale(self.player_left_img, (40, 50))
        except:
            self.player_right_img = pygame.Surface((40, 50))
            self.player_right_img.fill(BLUE)

            self.player_left_img = pygame.Surface((40, 50))
            self.player_left_img.fill(RED)

        try:
            self.enemy_img = pygame.image.load("/Users/salmon/work/comprog2/project/cowboy/game_photo/enemy.png").convert_alpha()
            self.enemy_img = pygame.transform.scale(self.enemy_img, (40, 50))
        except:
            self.enemy_img = pygame.Surface((40, 50))
            self.enemy_img.fill(RED)

        try:
            self.special_img = pygame.image.load("/Users/salmon/work/comprog2/project/cowboy/game_photo/special.png").convert_alpha()
            self.special_img = pygame.transform.scale(self.special_img, (40, 50))
        except:
            self.special_img = pygame.Surface((40, 50))
            self.special_img.fill((255, 0, 255))  # Purple if special.png not found

        try:
            self.shotgun_img = pygame.image.load("/Users/salmon/work/comprog2/project/cowboy/game_photo/shotgun enemy.png").convert_alpha()
            self.shotgun_img = pygame.transform.scale(self.shotgun_img, (40, 50))
        except:
            self.shotgun_img = pygame.Surface((40, 50))
            self.shotgun_img.fill((255, 165, 0))

        try:
            self.background_img = pygame.image.load("/Users/salmon/work/comprog2/project/cowboy/game_photo/background.png").convert()
            self.background_img = pygame.transform.scale(self.background_img, (self.WIDTH, self.HEIGHT))
        except:
            self.background_img = pygame.Surface((self.WIDTH, self.HEIGHT))
            self.background_img.fill(BLACK)
        try:
            self.bullet_img = pygame.image.load("/Users/salmon/work/comprog2/project/cowboy/game_photo/Bullet.png").convert()
            self.bullet_img = pygame.transform.scale(self.shotgun_img, (10, 5))
        except:
            self.bullet_img = pygame.Surface((10, 5))
            self.bullet_img.fill(YELLOW)

        self.special_bullet_img = pygame.Surface((15, 10))
        self.special_bullet_img.fill((0, 255, 255))  # Cyan color for special bullets

    def reset_game(self):
        """Reset the game state for a new session."""
        self.data_collector.reset_data()  # Reset stats for a new game
        self.player = Player(100, self.HEIGHT - 100, self.player_right_img, self.player_left_img, self.data_collector)
        self.state = 1
        self.enemies, self.platforms, self.health_items, self.special_enemies, self.shotgun_enemies = generate_level(self.state, self.WIDTH, self.HEIGHT)
        self.bullets = []
        self.enemy_bullets = []
        self.special_bullets = []
        self.shotgun_bullets = []
        self.game_over = False

    def handle_collisions(self):
        """Check for collisions between the player, bullets, and other objects."""
        for health_item in self.health_items[:]:
            if self.player.rect.colliderect(health_item.rect):
                self.player.health += 1
                self.data_collector.record_special_pickup()  # Record special object pickup
                self.health_items.remove(health_item)

        for bullet in self.enemy_bullets[:]:
            if self.player.rect.colliderect(bullet.rect):
                self.player.health -= 1
                self.data_collector.record_hit()  # Record when the player gets hit
                self.enemy_bullets.remove(bullet)

        for bullet in self.special_bullets[:]:
            if bullet:
                self.data_collector.record_special_pickup()

        for bullet in self.shotgun_bullets[:]:
            if bullet:
                self.data_collector.record_special_pickup()

        if self.player.rect.right >= self.WIDTH:
            self.state += 1
            self.data_collector.update_level(self.state)  # Update the player's level progress
            self.player.rect.x = 50
            self.enemies, self.platforms, self.health_items, self.special_enemies, self.shotgun_enemies = generate_level(self.state, self.WIDTH, self.HEIGHT)

    def update(self, keys):
        """Update game objects and handle events."""
        if not self.game_over:
            self.player.move(keys)
            self.player.apply_gravity(self.platforms, self.ground_rect)

            self.player.score = self.data_collector.data["score"]  # Sync player score

            for enemy in self.enemies[:]:
                enemy.move()
                enemy.shoot(self.enemy_bullets)
                if enemy.hit(self.bullets, self.special_bullets, self.shotgun_bullets, self.health_items):
                    self.data_collector.update_score(1)  # Update player score
                    self.enemies.remove(enemy)
                    enemy.drop_health()

            for enemy in self.special_enemies[:]:
                enemy.move()
                enemy.shoot(self.enemy_bullets)
                if enemy.hit(self.bullets, self.special_bullets, self.shotgun_bullets, self.health_items):
                    if enemy.health <= 0:
                        self.player.special_bullet = True
                        self.data_collector.update_score(5)  # Special enemies give more points
                        self.data_collector.record_special_pickup()
                        self.special_enemies.remove(enemy)

            for enemy in self.shotgun_enemies[:]:
                enemy.move()
                enemy.shoot(self.enemy_bullets)
                if enemy.hit(self.bullets, self.special_bullets, self.shotgun_bullets, self.health_items):
                    if enemy.health <= 0:
                        loot = enemy.drop_loot()
                        self.health_items.extend(loot)
                        self.data_collector.update_score(2)
                        self.shotgun_enemies.remove(enemy)

            for bullet in self.bullets[:]:
                bullet.update()
                if bullet.rect.x > self.WIDTH or bullet.rect.x < 0:
                    self.bullets.remove(bullet)

            for bullet in self.enemy_bullets[:]:
                bullet.update()
                if bullet.rect.x > self.WIDTH or bullet.rect.x < 0:
                    self.enemy_bullets.remove(bullet)

            for bullet in self.special_bullets[:]:
                bullet.update()
                if bullet.rect.x > self.WIDTH or bullet.rect.x < 0:
                    self.special_bullets.remove(bullet)

            for bullet in self.shotgun_bullets[:]:
                bullet.update()
                if bullet.rect.x > self.WIDTH or bullet.rect.x < 0:
                    self.shotgun_bullets.remove(bullet)

            for item in self.health_items[:]:
                if isinstance(item, ShotgunBulletPickup) and self.player.rect.colliderect(item.rect):
                    self.player.has_shotgun_bullet = True
                    self.health_items.remove(item)
                elif isinstance(item, HealthPickup) and self.player.rect.colliderect(item.rect):
                    self.player.health += 1
                    self.health_items.remove(item)

            prev_x = self.player.rect.x  # Store previous X position
            self.player.move(keys)  # Move player
            self.player.apply_gravity(self.platforms, self.ground_rect)

            # Scroll background when player moves forward
            if self.player.rect.x > prev_x and self.player.rect.x > self.WIDTH // 3:
                self.bg_x -= self.bg_speed  # Move background to the left
                self.player.rect.x = prev_x  # Keep player in place visually

            if self.bg_x <= -self.WIDTH:  # Reset background for looping effect
                self.bg_x = 0

            self.handle_collisions()

            if self.player.health <= 0:
                self.game_over = True
                self.data_collector.save_data()  # Save data when the game ends

    def draw(self):
        """Render game objects onto the screen."""
        self.screen.blit(self.background_img, (self.bg_x, 0))
        self.screen.blit(self.background_img, (self.bg_x + self.WIDTH, 0))

        if self.bg_x <= -self.WIDTH:  # Reset background position when it moves too far
            self.bg_x = 0
        pygame.draw.rect(self.screen, (100, 50, 0), self.ground_rect)

        for platform in self.platforms:
            platform.draw(self.screen)

        for enemy in self.enemies:
            enemy.draw(self.screen, self.enemy_img)

        for enemy in self.special_enemies:
            enemy.draw(self.screen, self.special_img)

        for enemy in self.shotgun_enemies:
            enemy.draw(self.screen, self.shotgun_img)

        for bullet in self.bullets:
            bullet.draw(self.screen, self.bullet_img)

        for bullet in self.enemy_bullets:
            bullet.draw(self.screen, self.bullet_img)

        for bullet in self.special_bullets:
            bullet.draw(self.screen, self.special_bullet_img)

        for bullet in self.shotgun_bullets:
            bullet.draw(self.screen, self.special_bullet_img)

        for health_item in self.health_items:
            health_item.draw(self.screen)

        self.player.draw(self.screen)
        self.player.draw_ui(self.screen, self.state, self.FONT, self.WIDTH, self.HEIGHT, WHITE, RED)

        if self.game_over:
            game_over_text = self.FONT.render(f"Game Over! Score: {self.player.score}", True, RED)
            restart_text = self.FONT.render("Press R to Restart", True, WHITE)
            menu_text = self.FONT.render("Press M to Return to Menu", True, WHITE)

            self.screen.blit(game_over_text, (self.WIDTH // 2 - 150, self.HEIGHT // 2 - 70))
            self.screen.blit(restart_text, (self.WIDTH // 2 - 100, self.HEIGHT // 2 - 20))
            self.screen.blit(menu_text, (self.WIDTH // 2 - 160, self.HEIGHT // 2 + 20))


