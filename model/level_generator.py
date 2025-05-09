import random
from model.game_platform import Platform
from model.enemy import Enemy, SpecialEnemy, ShotgunEnemy
from model.constants import JUMP_STRENGTH, PLAYER_HEIGHT
from model.health_pickup import HealthPickup

def generate_level(state, width, height):
    platforms = []
    enemies = []
    health_items = []
    special_enemies = []
    shotgun_enemies = []

    # Minimum vertical and horizontal spacing
    JUMP_HEIGHT = JUMP_STRENGTH * 2  # Ensures the player can jump to the next platform
    PLATFORM_GAP = PLAYER_HEIGHT  # Ensures platforms are far enough apart

    # Starting platform at the bottom
    platforms.append(Platform(50, height - 100, 200, 20))

    last_platform_y = height - 100
    last_platform_x = 50
    platform_width = 200

    # Generate additional platforms with spacing
    for _ in range(5):
        valid_position = False
        attempts = 0

        while not valid_position and attempts < 10:  # Try 10 times to avoid overlapping
            new_y = last_platform_y - (JUMP_HEIGHT + random.randint(10, 30))
            if len(platforms) % 2 == 0:
                new_x = random.randint(width // 2, width - platform_width - 50)
            else:
                new_x = random.randint(50, width // 2 - platform_width)

            new_platform = Platform(new_x, new_y, platform_width, 20)

            # Check if new platform collides with existing platforms
            if all(not new_platform.rect.colliderect(p.rect) for p in platforms):
                platforms.append(new_platform)
                last_platform_y = new_y
                valid_position = True
            else:
                attempts += 1  # Try a different position

    # Enemy counts increase with level
    normal_enemy_count = 2 + (state // 2)  # Increase every 2 levels
    special_enemy_count = (state // 5)  # Special enemies every 5 levels
    shotgun_enemy_count = (state // 3)

    # Assign normal enemies to platforms
    for _ in range(normal_enemy_count):
        platform = random.choice(platforms)
        x = random.randint(platform.rect.left, platform.rect.right - 40)
        y = platform.rect.top - 50
        enemies.append(Enemy(x, y, platform))

    # Assign special enemies to platforms
    for _ in range(special_enemy_count):
        platform = random.choice(platforms)
        x = random.randint(platform.rect.left, platform.rect.right - 40)
        y = platform.rect.top - 50
        special_enemies.append(SpecialEnemy(x, y, platform))

    for _ in range(shotgun_enemy_count):
        platform = random.choice(platforms)
        x = random.randint(platform.rect.left, platform.rect.right - 40)
        y = platform.rect.top - 50
        shotgun_enemies.append(ShotgunEnemy(x, y, platform))

    return enemies, platforms, health_items, special_enemies, shotgun_enemies
