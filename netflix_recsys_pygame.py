import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Netflix Recommendation System")

# Colors
BACKGROUND = (15, 23, 42)  # Dark blue
WHITE = (255, 255, 255)
RED = (229, 9, 20)  # Netflix red
GRAY = (156, 163, 175)
LIGHT_GRAY = (209, 213, 219)
DARK_GRAY = (55, 65, 81)

# Fonts
font_small = pygame.font.Font(None, 24)
font_medium = pygame.font.Font(None, 32)
font_large = pygame.font.Font(None, 48)

# Content class
class Content:
    def __init__(self, title, genre, year, popularity):
        self.title = title
        self.genre = genre
        self.year = year
        self.popularity = popularity
        self.watched = False

# Create content library
genres = ["Action", "Comedy", "Drama", "Sci-Fi", "Romance", "Thriller"]
content_library = [
    Content(f"Title {i}", random.choice(genres), random.randint(1990, 2023), random.uniform(0, 1))
    for i in range(1, 51)
]

# User profile
user_preferences = {genre: random.uniform(0, 1) for genre in genres}
watched_content = []

# Function to calculate content score
def calculate_score(content):
    genre_score = user_preferences[content.genre]
    recency_score = (content.year - 1990) / (2023 - 1990)
    popularity_score = content.popularity
    return 0.5 * genre_score + 0.3 * recency_score + 0.2 * popularity_score

# Function to get recommendations
def get_recommendations():
    unwatched = [c for c in content_library if c not in watched_content]
    scored_content = [(c, calculate_score(c)) for c in unwatched]
    return sorted(scored_content, key=lambda x: x[1], reverse=True)[:10]

# Button class
class Button:
    def __init__(self, x, y, width, height, text, action, color=RED):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.color = color

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect, border_radius=5)
        text_surface = font_small.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

# Create buttons
buttons = [
    Button(50, 650, 200, 50, "Watch Random", "watch_random"),
    Button(300, 650, 250, 50, "Refresh Recommendations", "refresh")
]

# Main game loop
running = True
recommendations = get_recommendations()
selected_content = None

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            for button in buttons:
                if button.rect.collidepoint(pos):
                    if button.action == "watch_random":
                        unwatched = [c for c in content_library if not c.watched]
                        if unwatched:
                            selected_content = random.choice(unwatched)
                            selected_content.watched = True
                            watched_content.append(selected_content)
                            user_preferences[selected_content.genre] += 0.1
                            recommendations = get_recommendations()
                    elif button.action == "refresh":
                        recommendations = get_recommendations()

    # Clear the screen
    screen.fill(BACKGROUND)

    # Draw title
    title_text = font_large.render("Netflix Recommendation System", True, RED)
    screen.blit(title_text, (20, 20))

    # Draw user preferences
    pref_text = font_medium.render("User Preferences:", True, WHITE)
    screen.blit(pref_text, (20, 80))
    for i, (genre, score) in enumerate(user_preferences.items()):
        text = font_small.render(f"{genre}: {score:.2f}", True, GRAY)
        pygame.draw.rect(screen, DARK_GRAY, (20, 120 + i * 35, 200, 25), border_radius=5)
        pygame.draw.rect(screen, RED, (20, 120 + i * 35, int(200 * score), 25), border_radius=5)
        screen.blit(text, (25, 123 + i * 35))

    # Draw recommendations
    rec_text = font_medium.render("Recommended for You:", True, WHITE)
    screen.blit(rec_text, (300, 80))
    for i, (content, score) in enumerate(recommendations):
        text = font_small.render(f"{content.title} ({content.genre}, {content.year})", True, LIGHT_GRAY)
        screen.blit(text, (300, 120 + i * 30))
        pygame.draw.rect(screen, DARK_GRAY, (700, 120 + i * 30, 100, 20), border_radius=5)
        pygame.draw.rect(screen, RED, (700, 120 + i * 30, int(100 * score), 20), border_radius=5)
        score_text = font_small.render(f"{score:.2f}", True, WHITE)
        screen.blit(score_text, (810, 120 + i * 30))

    # Draw watched content
    watched_text = font_medium.render("Recently Watched:", True, WHITE)
    screen.blit(watched_text, (950, 80))
    for i, content in enumerate(watched_content[-5:]):
        text = font_small.render(f"{content.title} ({content.genre}, {content.year})", True, LIGHT_GRAY)
        screen.blit(text, (950, 120 + i * 30))

    # Draw buttons
    for button in buttons:
        button.draw()

    # Draw selected content info
    if selected_content:
        pygame.draw.rect(screen, DARK_GRAY, (50, 400, 500, 200), border_radius=10)
        info_text = [
            f"You just watched: {selected_content.title}",
            f"Genre: {selected_content.genre}",
            f"Year: {selected_content.year}",
            f"Popularity: {selected_content.popularity:.2f}",
            "Your preferences have been updated!"
        ]
        for i, text in enumerate(info_text):
            text_surface = font_small.render(text, True, WHITE)
            screen.blit(text_surface, (70, 420 + i * 30))

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()