import pygame
import numpy as np
import random

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 1600, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Alternating Least Squares (ALS) Demo")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (100, 100, 100)

# Fonts
title_font = pygame.font.Font(None, 48)
text_font = pygame.font.Font(None, 24)
small_font = pygame.font.Font(None, 20)

# ALS parameters
num_users = 5
num_items = 5
num_factors = 2

# Initialize user and item matrices
user_matrix = np.random.rand(num_users, num_factors)
item_matrix = np.random.rand(num_factors, num_items)

# Create a sparse rating matrix
rating_matrix = np.zeros((num_users, num_items))
for _ in range(num_users * num_items // 2):
    i, j = random.randint(0, num_users - 1), random.randint(0, num_items - 1)
    rating_matrix[i, j] = random.randint(1, 5)

# Ensure at least one non-zero value in each row and column
for i in range(num_users):
    if np.all(rating_matrix[i] == 0):
        j = random.randint(0, num_items - 1)
        rating_matrix[i, j] = random.randint(1, 5)
for j in range(num_items):
    if np.all(rating_matrix[:, j] == 0):
        i = random.randint(0, num_users - 1)
        rating_matrix[i, j] = random.randint(1, 5)

# ALS iteration
current_matrix = "user"
iteration = 0
max_iterations = 10

def draw_matrix(matrix, x, y, cell_size, title):
    rows, cols = matrix.shape
    pygame.draw.rect(screen, WHITE, (x, y, cols * cell_size, rows * cell_size), 2)
    
    max_value = np.max(matrix)
    min_value = np.min(matrix)
    
    for i in range(rows):
        for j in range(cols):
            value = matrix[i, j]
            if max_value != min_value:
                normalized_value = (value - min_value) / (max_value - min_value)
            else:
                normalized_value = 0
            color = pygame.Color(int(normalized_value * 255), int(normalized_value * 255), int(normalized_value * 255))
            pygame.draw.rect(screen, color, (x + j * cell_size, y + i * cell_size, cell_size, cell_size))
            
            # Display the value in each cell
            value_text = small_font.render(f"{value:.2f}", True, RED if value == 0 else BLACK)
            screen.blit(value_text, (x + j * cell_size + 5, y + i * cell_size + 5))
    
    title_surface = text_font.render(title, True, WHITE)
    screen.blit(title_surface, (x, y - 30))

def draw_text(text, x, y, font=text_font, color=WHITE):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

def als_step():
    global user_matrix, item_matrix, current_matrix, iteration
    
    if current_matrix == "user":
        for i in range(num_users):
            rated_items = np.nonzero(rating_matrix[i])[0]
            if len(rated_items) > 0:
                A = item_matrix[:, rated_items].T
                b = rating_matrix[i, rated_items]
                user_matrix[i] = np.linalg.lstsq(A, b, rcond=None)[0]
        current_matrix = "item"
    else:
        for j in range(num_items):
            rated_users = np.nonzero(rating_matrix[:, j])[0]
            if len(rated_users) > 0:
                A = user_matrix[rated_users]
                b = rating_matrix[rated_users, j]
                item_matrix[:, j] = np.linalg.lstsq(A, b, rcond=None)[0]
        current_matrix = "user"
        iteration += 1

def draw_arrow(start, end, color=WHITE):
    pygame.draw.line(screen, color, start, end, 2)
    rotation = np.arctan2(start[1] - end[1], end[0] - start[0])
    pygame.draw.polygon(screen, color, [
        (end[0] + 10 * np.cos(rotation), end[1] - 10 * np.sin(rotation)),
        (end[0] + 10 * np.cos(rotation + np.pi * 3/4), end[1] - 10 * np.sin(rotation + np.pi * 3/4)),
        (end[0] + 10 * np.cos(rotation - np.pi * 3/4), end[1] - 10 * np.sin(rotation - np.pi * 3/4)),
    ])

running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                als_step()

    screen.fill(BLACK)

    # Draw title
    title_surface = title_font.render("Alternating Least Squares (ALS) Demo", True, WHITE)
    screen.blit(title_surface, (WIDTH // 2 - title_surface.get_width() // 2, 20))

    # Draw developer info
    dev_surface = text_font.render("Developed by: Venugopal Adep", True, WHITE)
    screen.blit(dev_surface, (WIDTH // 2 - dev_surface.get_width() // 2, 70))

    # Draw matrices
    draw_matrix(rating_matrix, 100, 150, 50, "Rating Matrix")
    draw_matrix(user_matrix, 500, 150, 50, "User Matrix")
    draw_matrix(item_matrix, 900, 150, 50, "Item Matrix")

    # Draw predicted matrix
    predicted_matrix = np.dot(user_matrix, item_matrix)
    draw_matrix(predicted_matrix, 1300, 150, 50, "Predicted Matrix")

    # Draw arrows
    draw_arrow((400, 250), (480, 250))
    draw_arrow((800, 250), (880, 250))
    draw_arrow((1200, 250), (1280, 250))

    # Draw instructions and info
    draw_text("Press SPACE to perform one ALS iteration", 100, 500)
    draw_text(f"Current Matrix: {current_matrix.capitalize()}", 100, 530)
    draw_text(f"Iteration: {iteration}/{max_iterations}", 100, 560)

    # Draw explanation
    explanation = [
        "Alternating Least Squares (ALS) is a matrix factorization algorithm used in recommendation systems.",
        "It decomposes the rating matrix into two lower-dimensional matrices: User and Item.",
        "The algorithm alternates between fixing the User matrix and updating the Item matrix, and vice versa.",
        "This process minimizes the difference between the original ratings and the predicted ratings.",
        "As the algorithm progresses, the Predicted Matrix should become closer to the Rating Matrix.",
        "",
        "Color intensity in matrices represents the magnitude of values (darker = higher value).",
        "Red zeros in the Rating Matrix indicate missing ratings.",
        "The User and Item matrices start with random values and are refined in each iteration.",
    ]

    for i, line in enumerate(explanation):
        draw_text(line, 100, 600 + i * 25)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()