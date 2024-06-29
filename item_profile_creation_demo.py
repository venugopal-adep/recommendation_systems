import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 1600, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Content-Based Filtering: Movie Profile Visualizer")

# Colors
BACKGROUND = (240, 248, 255)  # Alice Blue
TEXT_COLOR = (47, 79, 79)  # Dark Slate Gray
MOVIE_COLOR = (70, 130, 180)  # Steel Blue
FEATURE_COLOR = (255, 165, 0)  # Orange
CONNECTION_COLOR = (50, 205, 50)  # Lime Green
INFO_BOX_COLOR = (230, 230, 250)  # Lavender
BUTTON_COLOR = (176, 224, 230)  # Powder Blue

# Fonts
title_font = pygame.font.Font(None, 56)
text_font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 28)

# Movie class
class Movie:
    def __init__(self, name, features):
        self.name = name
        self.features = features
        self.x = random.randint(100, WIDTH - 400)
        self.y = random.randint(200, HEIGHT - 100)
        self.radius = 40
        self.color = MOVIE_COLOR
        
    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
        pygame.draw.circle(screen, TEXT_COLOR, (self.x, self.y), self.radius, 2)
        name_text = small_font.render(self.name, True, TEXT_COLOR)
        screen.blit(name_text, (self.x - name_text.get_width() // 2, self.y - self.radius - 25))

# Feature class
class Feature:
    def __init__(self, name):
        self.name = name
        self.x = random.randint(100, WIDTH - 400)
        self.y = random.randint(200, HEIGHT - 100)
        self.radius = 30
        
    def draw(self):
        pygame.draw.circle(screen, FEATURE_COLOR, (self.x, self.y), self.radius)
        pygame.draw.circle(screen, TEXT_COLOR, (self.x, self.y), self.radius, 2)
        name_text = small_font.render(self.name, True, TEXT_COLOR)
        screen.blit(name_text, (self.x - name_text.get_width() // 2, self.y - self.radius - 25))

# Create movies and features
movies = [
    Movie("Movie A", ["Action", "Sci-Fi"]),
    Movie("Movie B", ["Romance", "Comedy"]),
    Movie("Movie C", ["Drama", "Thriller"]),
    Movie("Movie D", ["Action", "Comedy"]),
]

features = [Feature(f) for f in ["Action", "Sci-Fi", "Romance", "Comedy", "Drama", "Thriller"]]

# Button class
class Button:
    def __init__(self, x, y, width, height, text, color, text_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.text_color = text_color

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect, border_radius=10)
        pygame.draw.rect(screen, TEXT_COLOR, self.rect, 2, border_radius=10)
        text_surf = small_font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# Create button
reset_button = Button(WIDTH - 280, HEIGHT - 80, 260, 50, "Reset Selection", BUTTON_COLOR, TEXT_COLOR)

# Main game loop
running = True
selected_movie = None

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                mouse_pos = pygame.mouse.get_pos()
                for movie in movies:
                    distance = math.sqrt((mouse_pos[0] - movie.x)**2 + (mouse_pos[1] - movie.y)**2)
                    if distance <= movie.radius:
                        selected_movie = movie
                        break
                else:
                    if reset_button.is_clicked(mouse_pos):
                        selected_movie = None

    # Clear the screen
    screen.fill(BACKGROUND)

    # Draw title and developer info
    title_text = title_font.render("Content-Based Filtering: Movie Profile Visualizer", True, TEXT_COLOR)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 20))
    
    dev_text = text_font.render("Developed by: Venugopal Adep", True, TEXT_COLOR)
    screen.blit(dev_text, (WIDTH // 2 - dev_text.get_width() // 2, 80))

    # Draw movies and features
    for movie in movies:
        movie.draw()
    
    for feature in features:
        feature.draw()

    # Draw connections for selected movie
    if selected_movie:
        for feature in features:
            if feature.name in selected_movie.features:
                pygame.draw.line(screen, CONNECTION_COLOR, (selected_movie.x, selected_movie.y), (feature.x, feature.y), 3)

    # Draw information box
    info_box = pygame.Rect(WIDTH - 300, 120, 280, HEIGHT - 220)
    pygame.draw.rect(screen, INFO_BOX_COLOR, info_box, border_radius=10)
    pygame.draw.rect(screen, TEXT_COLOR, info_box, 2, border_radius=10)

    if selected_movie:
        movie_name = text_font.render(f"Movie: {selected_movie.name}", True, TEXT_COLOR)
        screen.blit(movie_name, (info_box.x + 10, info_box.y + 10))
        
        feature_text = text_font.render("Features:", True, TEXT_COLOR)
        screen.blit(feature_text, (info_box.x + 10, info_box.y + 50))
        
        for i, feature in enumerate(selected_movie.features):
            feature_item = small_font.render(f"- {feature}", True, TEXT_COLOR)
            screen.blit(feature_item, (info_box.x + 20, info_box.y + 90 + i * 30))
    else:
        no_selection = text_font.render("No movie selected", True, TEXT_COLOR)
        screen.blit(no_selection, (info_box.x + 10, info_box.y + 10))

    # Draw instructions
    instructions = [
        "Instructions:",
        "- Click on a movie to see its profile",
        "  and connections to features",
        "- Click 'Reset Selection' to clear",
        "  the current selection",
        "- Explore the relationships between",
        "  movies and their features"
    ]
    
    for i, instruction in enumerate(instructions):
        inst_text = small_font.render(instruction, True, TEXT_COLOR)
        screen.blit(inst_text, (20, HEIGHT - 200 + i * 30))

    # Draw button
    reset_button.draw()

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()