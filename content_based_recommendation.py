import pygame
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 1600, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Content-Based Recommendation Demo")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Fonts
title_font = pygame.font.Font(None, 48)
subtitle_font = pygame.font.Font(None, 36)
font = pygame.font.Font(None, 36)

# Movie data
movies = [
    {"title": "Action Hero", "genres": [1, 0, 0]},
    {"title": "Love Story", "genres": [0, 1, 0]},
    {"title": "Space Odyssey", "genres": [0, 0, 1]},
    {"title": "Romantic Comedy", "genres": [0, 1, 0]},
    {"title": "Sci-Fi Action", "genres": [1, 0, 1]},
    {"title": "Drama", "genres": [0, 1, 0]},
]

# User profile
user_profile = [0, 0, 0]  # [Action, Romance, Sci-Fi]

def draw_text(text, position, color=WHITE, font=font):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, position)

def draw_bar(position, value, max_width, color):
    bar_width = int(value * max_width)
    pygame.draw.rect(screen, color, (*position, bar_width, 30))
    pygame.draw.rect(screen, WHITE, (*position, max_width, 30), 2)

def update_recommendations():
    user_vector = np.array(user_profile).reshape(1, -1)
    movie_vectors = np.array([movie['genres'] for movie in movies])
    similarities = cosine_similarity(user_vector, movie_vectors)[0]
    return sorted(zip(movies, similarities), key=lambda x: x[1], reverse=True)

# Main game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            if 50 <= x <= 550 and 100 <= y <= 250:
                genre_index = (y - 100) // 50
                if event.button == 1:  # Left click
                    user_profile[genre_index] = min(user_profile[genre_index] + 0.1, 1)
                elif event.button == 3:  # Right click
                    user_profile[genre_index] = max(user_profile[genre_index] - 0.1, 0)

    screen.fill(BLACK)

    # Draw title and developer credit
    draw_text("Content based Recommendation System", (width // 2 - 300, 10), font=title_font)
    draw_text("Developed by : Venugopal Adep", (width // 2 - 200, 60), font=subtitle_font)

    # Draw user profile
    draw_text("User Profile (Left click to increase, Right click to decrease):", (50, 110))
    genres = ["Action", "Romance", "Sci-Fi"]
    for i, (genre, value) in enumerate(zip(genres, user_profile)):
        draw_text(genre, (50, 160 + i * 50))
        draw_bar((200, 160 + i * 50), value, 300, BLUE)
        draw_text(f"{value:.1f}", (510, 160 + i * 50))

    # Draw recommendations
    draw_text("Recommended Movies:", (50, 350))
    recommendations = update_recommendations()
    for i, (movie, similarity) in enumerate(recommendations):
        draw_text(f"{movie['title']}", (50, 400 + i * 40))
        draw_bar((400, 400 + i * 40), similarity, 300, GREEN)
        draw_text(f"{similarity:.2f}", (710, 400 + i * 40))

    # Draw movie genres
    draw_text("Movie Genres:", (1000, 110))
    for i, movie in enumerate(movies):
        draw_text(movie['title'], (1000, 160 + i * 50))
        for j, genre_value in enumerate(movie['genres']):
            draw_bar((1200 + j * 100, 160 + i * 50), genre_value, 80, [RED, YELLOW, BLUE][j])

    pygame.display.flip()
    clock.tick(30)

pygame.quit()