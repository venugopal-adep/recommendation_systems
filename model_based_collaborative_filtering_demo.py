import pygame
import numpy as np
from scipy.sparse.linalg import svds

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 1600, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Model-Based Collaborative Filtering Demo")

# Colors
BACKGROUND = (15, 23, 42)  # Dark blue
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 99, 71)  # Tomato
GREEN = (46, 204, 113)  # Emerald
BLUE = (52, 152, 219)  # Dodger Blue
YELLOW = (241, 196, 15)  # Sun Flower
PURPLE = (155, 89, 182)  # Amethyst
GRAY = (149, 165, 166)  # Asbestos
LIGHT_GRAY = (236, 240, 241)  # Cloud

# Fonts
title_font = pygame.font.Font(None, 48)
subtitle_font = pygame.font.Font(None, 36)
text_font = pygame.font.Font(None, 24)
small_font = pygame.font.Font(None, 20)

# Rating data
ratings = {
    "Alice": {"Action": 5, "Comedy": 3, "Drama": 4, "Sci-Fi": 2, "Mystery": 4},
    "Bob": {"Action": 4, "Comedy": 5, "Drama": 2, "Sci-Fi": 3, "Mystery": 4},
    "Charlie": {"Action": 3, "Comedy": 4, "Drama": 5, "Sci-Fi": 1, "Mystery": 3},
    "David": {"Action": 2, "Comedy": 3, "Drama": 3, "Sci-Fi": 5, "Mystery": 4},
    "Eve": {"Action": 5, "Comedy": 2, "Drama": 4, "Sci-Fi": 4, "Mystery": 3}
}

users = list(ratings.keys())
items = list(ratings["Alice"].keys())

active_user = "Alice"
active_item = "Action"

# Button class
class Button:
    def __init__(self, x, y, width, height, text, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect, border_radius=10)
        pygame.draw.rect(screen, WHITE, self.rect, border_radius=10, width=2)
        text_surface = text_font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# Create buttons
user_buttons = [Button(50 + i * 150, 150, 120, 40, user, BLUE) for i, user in enumerate(users)]
item_buttons = [Button(50 + i * 150, 220, 120, 40, item, GREEN) for i, item in enumerate(items)]

# Helper functions
def create_matrix():
    matrix = np.zeros((len(users), len(items)))
    for i, user in enumerate(users):
        for j, item in enumerate(items):
            matrix[i, j] = ratings[user][item]
    return matrix

def matrix_factorization(matrix, k=2):
    U, s, Vt = svds(matrix, k=k)
    s_diag = np.diag(s)
    return U, s_diag, Vt

def get_recommendation(user_index, item_index, U, s, Vt):
    prediction = np.dot(np.dot(U[user_index], s), Vt[:, item_index])
    return prediction

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

# Prepare data
rating_matrix = create_matrix()
U, s, Vt = matrix_factorization(rating_matrix)

# Main game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            for button in user_buttons:
                if button.is_clicked(pos):
                    active_user = button.text
            for button in item_buttons:
                if button.is_clicked(pos):
                    active_item = button.text

    # Clear the screen
    screen.fill(BACKGROUND)

    # Draw title and developer info
    draw_text("Model-Based Collaborative Filtering Demo", title_font, WHITE, WIDTH // 2, 50, align="center")
    draw_text("Developed by: Venugopal Adep", subtitle_font, GRAY, WIDTH // 2, 100, align="center")

    # Draw buttons
    for button in user_buttons:
        button.color = PURPLE if button.text == active_user else BLUE
        button.draw()

    for button in item_buttons:
        button.color = YELLOW if button.text == active_item else GREEN
        button.draw()

    # Draw rating matrix
    matrix_box = pygame.Rect(50, 300, 700, 300)
    pygame.draw.rect(screen, LIGHT_GRAY, matrix_box, border_radius=10)
    pygame.draw.rect(screen, WHITE, matrix_box, border_radius=10, width=2)

    draw_text("User-Item Rating Matrix", subtitle_font, BLACK, matrix_box.centerx, matrix_box.top + 30, align="center")

    for i, user in enumerate(users):
        y_offset = 360 + i * 50
        draw_text(f"{user}:", text_font, BLACK, 60, y_offset)
        
        for j, item in enumerate(items):
            rating_text = f"{item}: {ratings[user][item]}"
            draw_text(rating_text, text_font, BLACK, 160 + j * 120, y_offset)

    # Calculate and display recommendation with explanation
    user_index = users.index(active_user)
    item_index = items.index(active_item)
    recommendation = get_recommendation(user_index, item_index, U, s, Vt)
    
    # Draw explanation box
    explanation_box = pygame.Rect(800, 150, 750, 700)
    pygame.draw.rect(screen, LIGHT_GRAY, explanation_box, border_radius=10)
    pygame.draw.rect(screen, WHITE, explanation_box, border_radius=10, width=2)

    y_offset = 170
    draw_text("Model-Based Collaborative Filtering using Matrix Factorization", subtitle_font, BLACK, 820, y_offset)

    y_offset += 50
    draw_text(f"Predicted rating for {active_user} - {active_item}: {recommendation:.2f}", text_font, RED, 820, y_offset)
    
    y_offset += 50
    draw_text("Explanation:", subtitle_font, BLACK, 820, y_offset)
    
    y_offset += 40
    steps = [
        "1. The user-item rating matrix is decomposed into three matrices: U, s, and Vt.",
        "2. U represents user factors, Vt represents item factors, and s contains singular values.",
        f"3. We use {U.shape[1]} latent factors for this demonstration.",
        "4. To predict a rating, we multiply the corresponding user vector, singular values, and item vector:",
        f"   Prediction = U[user] · s · Vt[:, item]",
        f"5. For {active_user} and {active_item}:",
        f"   User vector: {U[user_index]}",
        f"   Singular values: {np.diag(s)}",
        f"   Item vector: {Vt[:, item_index]}",
        f"6. The final prediction is the dot product of these vectors: {recommendation:.2f}"
    ]
    
    for step in steps:
        draw_text(step, small_font, BLACK, 820, y_offset)
        y_offset += 30

    # Update the display
    pygame.display.flip()
    clock.tick(60)

# Quit Pygame
pygame.quit()