import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend
import matplotlib.pyplot as plt
import csv

class GraphShow:
    def __init__(self, filename="game_save.csv"):
        self.filename = filename
        self.data = {
            "score": [],
            "reloads": [],
            "special_pickups": [],
            "level": [],
            "hits_taken": []
        }

    def load_data(self):
        try:
            with open(self.filename, "r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    self.data["score"].append(int(row.get("score", 0)))
                    self.data["reloads"].append(int(row.get("reloads", 1)))
                    self.data["special_pickups"].append(int(row.get("special_pickups", 0)))
                    self.data["level"].append(int(row.get("level", 0)))
                    self.data["hits_taken"].append(int(row.get("hits_taken", 0)))
        except Exception as e:
            print("Error loading data:", e)

    def save_graph(self, graph_type="score"):
        if not self.data["score"]:
            return

        accuracy = [
            round(score / (reloads * 6), 2) if reloads > 0 else 0
            for score, reloads in zip(self.data["score"], self.data["reloads"])
        ]

        plt.figure(figsize=(8, 5))

        if graph_type == "score":
            plt.plot(self.data["score"], marker="o")
            plt.title("Points")
        elif graph_type == "accuracy":
            plt.plot(accuracy, marker="o", color="orange")
            plt.title("Accuracy (Points per 6 bullets)")
        elif graph_type == "special_pickups":
            plt.plot(self.data["special_pickups"], marker="o", color="green")
            plt.title("Special Pickups")
        elif graph_type == "level":
            plt.plot(self.data["level"], marker="o", color="purple")
            plt.title("States Reached")
        elif graph_type == "times_shot":
            plt.plot(self.data["hits_taken"], marker="o", color="red")
            plt.title("hits_taken")
        else:
            plt.close()
            return

        plt.grid(True)
        plt.tight_layout()
        plt.savefig("graph_image.png")
        plt.close()

    def get_summary_stats(self):
        if not self.data["score"]:
            return {}

        accuracy = [
            round(score / (reloads * 6), 2) if reloads > 0 else 0
            for score, reloads in zip(self.data["score"], self.data["reloads"])
        ]

        return {
            "Average Points": sum(self.data["score"]) // len(self.data["score"]),
            "Max Points": max(self.data["score"]),
            "Average Accuracy (%)": round(sum(accuracy) / len(accuracy) * 100, 2),
            "Max Accuracy (%)": round(max(accuracy) * 100, 2),
            "Average Pickups": sum(self.data["special_pickups"]) // len(self.data["special_pickups"]),
            "Max Pickups": max(self.data["special_pickups"]),
        }


