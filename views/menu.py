import pygame
import sys
import threading
from views.graph_show import GraphShow  # Import the GraphShow class

class MainMenu:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.WIDTH = width
        self.HEIGHT = height
        self.FONT = pygame.font.Font(None, 48)

        self.buttons = {
            "Start Game": pygame.Rect(width // 2 - 100, 200, 200, 50),
            "View Stats": pygame.Rect(width // 2 - 100, 300, 200, 50),
            ("Stats", "Summary"): pygame.Rect(width // 2 - 100, 400, 200, 50),
            "Quit": pygame.Rect(width // 2 - 100, 500, 200, 50)
        }


    def draw_menu(self):
        self.screen.fill((30, 30, 30))
        title = self.FONT.render("Main Menu", True, (255, 255, 255))
        self.screen.blit(title, (self.WIDTH // 2 - title.get_width() // 2, 100))

        for label, rect in self.buttons.items():
            pygame.draw.rect(self.screen, (50, 150, 200), rect)

            if isinstance(label, tuple):
                for i, line in enumerate(label):
                    line_surface = self.FONT.render(line, True, (255, 255, 255))
                    line_rect = line_surface.get_rect(center=(rect.centerx, rect.y + 15 + i * 20))
                    self.screen.blit(line_surface, line_rect)
            else:
                label_surface = self.FONT.render(label, True, (255, 255, 255))
                label_rect = label_surface.get_rect(center=rect.center)
                self.screen.blit(label_surface, label_rect)

        pygame.display.flip()


    def run(self):
        while True:
            self.draw_menu()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    for label, rect in self.buttons.items():
                        if rect.collidepoint(mouse_pos):
                            if label == "Start Game":
                                return "start"
                            elif label == "View Stats":
                                return "graph"
                            elif label == ("Stats", "Summary"):
                                return "stats"
                            elif label == "Quit":
                                return "quit"


    def show_graph(self, graph_type="score"):
        # Generate and save the graph
        graph_show = GraphShow()
        graph_show.load_data()
        graph_show.save_graph(graph_type=graph_type)

        # Open Pygame window to display the graph
        graph_screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption(f"{graph_type.title()} Graph")

        try:
            graph_image = pygame.image.load(f"graph_photo/{graph_type}_graph.png")
        except pygame.error:
            print("Failed to load graph image.")
            return

        # Display the image
        running = True
        while running:
            graph_screen.fill((0, 0, 0))
            graph_screen.blit(graph_image, (0, 0))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    running = False

        pygame.display.set_mode((self.WIDTH, self.HEIGHT))  # Reset back to menu

    def show_graph_menu(self):
        graph_show = GraphShow()
        graph_show.load_data()

        buttons = {
            "Points": pygame.Rect(self.WIDTH // 2 - 100, 150, 200, 50),
            "Level": pygame.Rect(self.WIDTH // 2 - 100, 220, 200, 50),
            "Got Shot": pygame.Rect(self.WIDTH // 2 - 100, 290, 200, 50),
            "Back": pygame.Rect(self.WIDTH // 2 - 100, 360, 200, 50)
        }

        while True:
            self.screen.fill((20, 20, 20))
            title = self.FONT.render("Choose Graph", True, (255, 255, 255))
            self.screen.blit(title, (self.WIDTH // 2 - title.get_width() // 2, 80))

            for label, rect in buttons.items():
                pygame.draw.rect(self.screen, (50, 150, 200), rect)
                text = self.FONT.render(label, True, (255, 255, 255))
                self.screen.blit(text, (rect.x + 20, rect.y + 10))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    for label, rect in buttons.items():
                        if rect.collidepoint(pos):
                            if label == "Back":
                                return
                            elif label == "Points":
                                graph_show.save_graph("score")
                                self.show_graph("score")
                            elif label == "Level":
                                graph_show.save_graph("level")
                                self.show_graph("level")
                            elif label == "Got Shot":
                                graph_show.save_graph("times_shot")
                                self.show_graph("times_shot")

    def show_summary(self):
        graph_show = GraphShow()
        graph_show.load_data()
        stats = graph_show.get_summary_stats()

        summary_screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Player Stats Summary")
        font = pygame.font.Font(None, 36)

        running = True
        while running:
            summary_screen.fill((10, 10, 10))
            title = font.render("Stats Summary", True, (255, 255, 255))
            summary_screen.blit(title, (300, 50))

            if stats:
                for i, (label, value) in enumerate(stats.items()):
                    text = font.render(f"{label}: {value}", True, (255, 255, 255))
                    summary_screen.blit(text, (150, 120 + i * 40))
            else:
                error_text = font.render("No data to display.", True, (255, 0, 0))
                summary_screen.blit(error_text, (200, 200))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    running = False

        pygame.display.set_mode((self.WIDTH, self.HEIGHT))

