import os
import json
import csv

class GameDataCollector:
    def __init__(self, save_file="game_save.csv"):
        self.save_file = save_file
        self.data = {
            "score": 0,
            "level": 1,
            "reloads": 0,
            "special_pickups": 0,
            "hits_taken": 0
        }

    def new_save(self):
        """Create a new save file and reset data."""
        self.data = {
            "score": 0,
            "level": 1,
            "reloads": 0,
            "special_pickups": 0,
            "hits_taken": 0
        }
        self.save_data()
        print("New save file created.")

    def load_save(self):
        """Load latest save data if available."""
        if os.path.exists(self.save_file):
            with open(self.save_file, "r", newline="") as file:
                reader = csv.DictReader(file)
                # Convert to list and get the last row (most recent save)
                rows = list(reader)
                if rows:  # Check if there are any rows
                    # Convert string values to appropriate types
                    latest_data = rows[-1]  # Get the last row
                    self.data = {
                        "score": int(latest_data["score"]),
                        "level": int(latest_data["level"]),
                        "reloads": int(latest_data["reloads"]),
                        "special_pickups": int(latest_data["special_pickups"]),
                        "hits_taken": int(latest_data["hits_taken"])
                    }
                    print("Save file loaded.")
                else:
                    print("Save file exists but is empty. Starting new game.")
                    self.new_save()
        else:
            print("No save file found. Starting new game.")
            self.new_save()

    def save_data(self):
        """Save game data to a CSV file."""
        file_exists = os.path.exists(self.save_file)

        with open(self.save_file, mode="a", newline="") as file:  # Use append mode
            writer = csv.DictWriter(file, fieldnames=self.data.keys())

            # Write the header only if the file is new
            if not file_exists or os.stat(self.save_file).st_size == 0:
                writer.writeheader()

            # Append the new game data
            writer.writerow(self.data)
        print("Game data saved in CSV format.")

    def reset_data(self):
        """Reset stats but keep save file."""
        self.data["score"] = 0
        self.data["level"] = 1
        self.data["reloads"] = 0
        self.data["special_pickups"] = 0
        self.data["hits_taken"] = 0

    def update_score(self, points):
        self.data["score"] += points

    def update_level(self, level):
        self.data["level"] = level

    def record_reload(self):
        self.data["reloads"] += 1

    def record_special_pickup(self):
        self.data["special_pickups"] += 1

    def record_hit(self):
        self.data["hits_taken"] += 1
