
# 🕹️ Game Project with Graph Stats

This is a simple Wild West-themed game menu system built using `pygame` that allows players to:

- Start the game and fight enemies across states
- View gameplay statistics as graphs (Score, Level, Hits Taken)
- View a summary of gameplay stats (Average Points, Max Accuracy, etc.)

Gameplay data is loaded from a `game_save.csv` file and visualized using `matplotlib`.

---

## 📦 Requirements

Before running the project, ensure you have Python and the required libraries installed.

### ✅ Python Version

- Python 3.7 or higher

### 📦 Install Required Packages

Install all dependencies using:

```bash
pip install -r requirements.txt
```

---

## 📁 Project Structure

```
.
├── main.py                # Main launcher and menu system
├── model/                 # Game model classes
├── views/                 # UI-related files
├── control/               # Controls game flow
├── game_save.csv          # Game data file (must exist to view stats)
├── README.md              # Project documentation
```

---

## 🚀 How to Run

1. **Clone the repository**

```bash
git clone https://github.com/peerawattae/comprog2_year_project.git
cd comprog2_year_project
```

2. **Create or verify the `game_save.csv` file**

If it doesn’t already exist, create one manually with this content:

```csv
score,reloads,special_pickups,level,hits_taken
60,3,2,2,1
40,2,1,1,3
100,4,3,3,2
```

3. **Run the game**

```bash
python main.py
```

---

## 🎮 Controls

When inside the game (after clicking "Start Game"):

| Key      | Action       |
| -------- | ------------ |
| W        | Walk Up      |
| A        | Walk Left    |
| S        | Walk Down    |
| D        | Walk Right   |
| J        | Normal Shoot |
| Spacebar | Jump         |

---

## 📊 Stats & Graphs

### From the Main Menu:

* **View Stats**
  Opens a graph menu with options:

  * **Points**: Player score over time.
  * **Level**: States/levels reached.
  * **Times Got Shot**: Number of times player was hit.

* **Stats Summary**
  Displays:

  * Average & Max Points
  * Average & Max Accuracy (%)
  * Average & Max Special Pickups

---

## 🛠️ Customize

* Modify `graph_show.py` to add new graph types or statistical metrics.
* Expand the gameplay logic in `main.py` or related files.
* Append new rows to `game_save.csv` after each session to track long-term progress.

---

## 📐 UML Diagram

Below is the UML diagram for the project structure and interactions:

![UML Diagram](game_photo/project_UML.png)

---

## 🔗 Resources

* 💻 GitHub Repository: [peerawattae/comprog2\_year\_project](https://github.com/peerawattae/comprog2_year_project.git)
* 🎥 YouTube Presentation Video: [Watch Gameplay Demo](https://youtu.be/8EBVcwT_3yA)

---
