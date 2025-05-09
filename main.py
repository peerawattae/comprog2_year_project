import pygame
import random
from game import Game
from player import Player
from level_generator import generate_level
from collect_data import GameDataCollector

# -------- NEW MENU PART START --------
from menu import MainMenu  # <--- Make sure you have menu.py with MainMenu class

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cowboy")
clock = pygame.time.Clock()

# Launch main menu before starting game
menu = MainMenu(screen, WIDTH, HEIGHT)
while True:
    action = menu.run()
    if action == "start":
        break  # Proceed to game loop
    elif action == "graph":
        menu.show_graph_menu()
    elif action == "stats":
        menu.show_summary()
    elif action == "quit":
        pygame.quit()
        exit()
# -------- NEW MENU PART END --------

# Create the game instance
game = Game(screen, WIDTH, HEIGHT)

# Game loop
running = True

while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if not game.game_over:
                if event.key == pygame.K_j:
                    game.player.shoot(game.bullets)
                elif event.key == pygame.K_k:
                    game.player.shoot_special(game.special_bullets)
                elif event.key == pygame.K_l and not game.game_over:  # L key to shoot shotgun
                    game.player.shoot_shotgun(game.shotgun_bullets)
            else:
                if event.key == pygame.K_r:
                    game.reset_game()
                elif event.key == pygame.K_m:
                    # Return to menu
                    menu = MainMenu(screen, WIDTH, HEIGHT)
                    while True:
                        action = menu.run()
                        if action == "start":
                            game.reset_game()
                            break
                        elif action == "stats":
                            menu.show_summary()
                        elif action == "graph":
                            menu.show_graph_menu()
                        elif action == "quit":
                            running = False
                            break

    # Get keyboard state
    keys = pygame.key.get_pressed()

    # Update game state
    game.update(keys)

    # Draw everything
    game.draw()

    # Update display
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
