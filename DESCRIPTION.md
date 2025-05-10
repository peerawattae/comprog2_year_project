# Wild West

**[GitHub Repository](https://github.com/peerawattae/comprog2_year_project.git)**  
**[Presentation Video](https://youtu.be/8EBVcwT_3yA)**

---

## Project Overview

This game is about a cowboy exploring the western land and facing many enemies. The player will have the option to either shoot enemies to gain points and special items or run away to the next state to save health but forgo points. The goal of the game is to get as many points as possible.

---

## Project Review

A project that inspires this game is the Python-based "Rockman (Megaman)" game. Its objective is to beat the boss by progressing through levels quickly.

In contrast to Rockman, where players often skip regular enemies to save health for the boss fight, this game encourages players to engage with enemies by rewarding them with points and potential health pickups. Avoiding enemies means missing out on valuable rewards.

---

## Programming Development

### 3.1 Game Concept

- Game starts at state 1 with 2 enemies.
- Goal: collect the most points by defeating enemies.
- Every 10th level features a special, stronger enemy.
- Every 5 levels, the number of enemies increases by 1.
- Defeating normal enemies may reward players with extra health.
- Players have limited ammunition (6 bullets/magazine) to prevent button spamming.
- Game ends when player health reaches 0.

### 3.2 Object-Oriented Programming Implementation

1. **Player**: Handles player attributes like health, ammo, movement, shooting, UI, etc.  
2. **Enemy**: Manages enemy health, actions, random health drops, and movements.  
3. **Bullet**: Manages drawing and behavior of bullets.  
4. **SpecialBullet** *(inherits Bullet)*: More powerful than regular bullets.  
5. **ShotgunBullet** *(inherits Bullet)*: Fires three bullets in a spread pattern.  
6. **SpecialEnemy** *(inherits Enemy)*: Has more health and drops special bullets.  
7. **ShotgunEnemy** *(inherits Enemy)*: Fires spread bullets and has 3 health points.  
8. **Platform**: Generates platforms for enemies and the player.  
9. **HealthPickup**: Manages random health drop pickup behavior.  
10. **Game**: Core logic — drawing game elements, background, player/enemy mechanics, collision detection, and updates.  
11. **GameDataCollector**: Records game statistics into a `.csv` file.  
12. **GraphShow**: Plots graphs of recorded data and saves them as `.png`.  
13. **MainMenu**: Displays UI for choosing between gameplay or data analysis.  

### 3.3 Algorithms Involved

- Health calculation for players and enemies  
- Platform distance and placement  
- Health drop randomization  
- Bullet-enemy and bullet-player hit detection  
- Enemy movement and edge detection  
- Enemy spawning logic based on game level  

---

## Statistical Data (Prop Stats)

### 4.1 Data Features

| Feature         | Purpose                                                  | Collection Class | Visualization                |
|----------------|-----------------------------------------------------------|------------------|-------------------------------|
| **Point**       | Indicates player skill level                             | `Game`           | Line graph, bar chart         |
| **Reload**      | Accuracy = `Point / (Reload × 6)`                        | `Player`         | Accuracy percentage           |
| **Special Object** | Number of special enemies defeated                     | `Game`           | Table (most, average pickups) |
| **Level**       | Represents how far the player progressed                 | `Game`           | Bar chart                     |
| **Got Shot**    | Indicates dodging/movement skill                         | `Game`           | Scatter plot                  |

---

## Why This Data Matters

- **Point**: Measures how well a player plays.  
- **Reload**: Evaluates shooting accuracy.  
- **Special Object**: Reveals player strategy (engage vs evade).  
- **Level**: Reflects overall progress and survivability.  
- **Got Shot**: Gauges how often the player takes damage.  

---

## Data Collection Method

- Play the game 50 times (due to short playtime).  
- Use corresponding class variables to collect stats.  
- Save all values to a CSV file using the `GameDataCollector` class.  

---

## Graph Summary

| Graph     | Feature      | Purpose                                      | Type        | X-Axis                   | Y-Axis              |
|-----------|--------------|----------------------------------------------|-------------|--------------------------|---------------------|
| Graph 1   | Point         | Show player improvement over time           | Time Series | Game instance (1–50)     | Points              |
| Graph 2   | Level         | Analyze progression trends every 10 games   | Bar Graph   | Games grouped (10, 20...)| Average level       |
| Graph 3   | Got Shot      | Explore difficulty trend per level          | Scatter Plot| Level (1–30)             | Times got shot      |

---

## Data Analysis Report

- Use **mean**, **max**, and **min** to analyze each data point.  
- Determine:
  - Highest and average point totals  
  - Player accuracy over sessions  
  - Frequency of special pickups  
  - Highest and average levels reached  
  - Times the player was shot  

This helps evaluate consistency and improvement.  
Data is presented via **charts** and **tables** for easy visualization.
