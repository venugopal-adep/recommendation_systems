import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 1600, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Context-Aware Recommendations Demo")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Fonts
title_font = pygame.font.Font(None, 48)
text_font = pygame.font.Font(None, 24)

# User preferences
user_preferences = {
    "action": 0.5,
    "comedy": 0.5,
    "drama": 0.5,
    "sci-fi": 0.5
}

# Context factors
contexts = ["morning", "afternoon", "evening", "night"]
current_context = random.choice(contexts)

# Movies
movies = [
    {"name": "Action Movie", "genre": "action", "morning": 0.3, "afternoon": 0.5, "evening": 0.7, "night": 0.9},
    {"name": "Comedy Show", "genre": "comedy", "morning": 0.8, "afternoon": 0.6, "evening": 0.7, "night": 0.4},
    {"name": "Drama Series", "genre": "drama", "morning": 0.4, "afternoon": 0.6, "evening": 0.8, "night": 0.5},
    {"name": "Sci-Fi Adventure", "genre": "sci-fi", "morning": 0.5, "afternoon": 0.7, "evening": 0.6, "night": 0.8}
]

def draw_text(text, font, color, x, y, align="left"):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    if align == "center":
        text_rect.center = (x, y)
    elif align == "right":
        text_rect.right = x
        text_rect.top = y
    else:
        text_rect.left = x
        text_rect.top = y
    screen.blit(text_surface, text_rect)

def draw_slider(x, y, width, value, label):
    pygame.draw.rect(screen, WHITE, (x, y, width, 20), 2)
    pygame.draw.rect(screen, GREEN, (x, y, int(width * value), 20))
    draw_text(label, text_font, WHITE, x + width + 10, y)

def update_recommendations():
    for movie in movies:
        context_score = movie[current_context]
        user_score = user_preferences[movie["genre"]]
        movie["score"] = (context_score + user_score) / 2

def draw_recommendations():
    sorted_movies = sorted(movies, key=lambda x: x["score"], reverse=True)
    for i, movie in enumerate(sorted_movies):
        x = 1000
        y = 300 + i * 60
        width = 500
        height = 50
        pygame.draw.rect(screen, WHITE, (x, y, width, height), 2)
        pygame.draw.rect(screen, BLUE, (x, y, int(width * movie["score"]), height))
        draw_text(f"{movie['name']} ({movie['score']:.2f})", text_font, WHITE, x + 10, y + 15)

def main():
    global current_context
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                for i, (genre, value) in enumerate(user_preferences.items()):
                    if 50 <= x <= 450 and 300 + i * 60 <= y <= 320 + i * 60:
                        user_preferences[genre] = (x - 50) / 400
                if 50 <= x <= 450 and 550 <= y <= 570:
                    current_context = contexts[int((x - 50) / 100)]

        screen.fill(BLACK)

        # Draw title and author
        draw_text("Context-Aware Recommendations Demo", title_font, WHITE, WIDTH // 2, 50, align="center")
        draw_text("Developed by: Venugopal Adep", text_font, WHITE, WIDTH // 2, 100, align="center")

        # Draw user preferences
        draw_text("User Preferences:", text_font, WHITE, 50, 250)
        for i, (genre, value) in enumerate(user_preferences.items()):
            draw_slider(50, 300 + i * 60, 400, value, genre.capitalize())

        # Draw context selector
        draw_text("Current Context:", text_font, WHITE, 50, 520)
        pygame.draw.rect(screen, WHITE, (50, 550, 400, 20), 2)
        for i, context in enumerate(contexts):
            if context == current_context:
                pygame.draw.rect(screen, YELLOW, (50 + i * 100, 550, 100, 20))
            draw_text(context.capitalize(), text_font, WHITE, 60 + i * 100, 550)

        # Update and draw recommendations
        update_recommendations()
        draw_text("Recommendations:", text_font, WHITE, 1000, 250)
        draw_recommendations()

        # Draw explanation
        explanation = [
            "This demo shows how context-aware recommendations work:",
            "1. Adjust user preferences using the sliders on the left.",
            "2. Change the context by clicking on the context bar.",
            "3. See how recommendations change based on both",
            "   user preferences and the current context.",
            "The final score is an average of context and user scores."
        ]
        for i, line in enumerate(explanation):
            draw_text(line, text_font, WHITE, 50, 650 + i * 30)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()