import pygame
import random
import sys
import math

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 1920, 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Advanced Sparse Data Handling Visualizer")

# Colors
BACKGROUND = (15, 20, 30)
WHITE = (240, 240, 240)
BLACK = (10, 10, 10)
GRAY = (100, 100, 100)
BLUE = (30, 144, 255)
GREEN = (46, 204, 113)
RED = (231, 76, 60)
YELLOW = (241, 196, 15)
PURPLE = (155, 89, 182)

# Fonts
title_font = pygame.font.Font(None, 72)
subtitle_font = pygame.font.Font(None, 36)
text_font = pygame.font.Font(None, 28)

# User-Item Matrix
USERS = 12
ITEMS = 24
matrix = [[0 for _ in range(ITEMS)] for _ in range(USERS)]

# Fill matrix with sparse data
for _ in range(40):
    u, i = random.randint(0, USERS-1), random.randint(0, ITEMS-1)
    matrix[u][i] = random.randint(1, 5)

# Button class
class Button:
    def __init__(self, x, y, width, height, text, color, text_color, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.text_color = text_color
        self.action = action

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect, border_radius=10)
        pygame.draw.rect(surface, WHITE, self.rect, 2, border_radius=10)
        text_surface = text_font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.action()

# Demo states
ORIGINAL = 0
COLLABORATIVE_FILTERING = 1
MATRIX_FACTORIZATION = 2

current_state = ORIGINAL

# Button actions
def switch_to_original():
    global current_state
    current_state = ORIGINAL

def switch_to_collaborative_filtering():
    global current_state
    current_state = COLLABORATIVE_FILTERING

def switch_to_matrix_factorization():
    global current_state
    current_state = MATRIX_FACTORIZATION

# Create buttons
buttons = [
    Button(50, HEIGHT - 100, 250, 60, "Original Data", BLUE, WHITE, switch_to_original),
    Button(350, HEIGHT - 100, 250, 60, "Collaborative Filtering", GREEN, WHITE, switch_to_collaborative_filtering),
    Button(650, HEIGHT - 100, 250, 60, "Matrix Factorization", RED, WHITE, switch_to_matrix_factorization)
]

def draw_matrix(matrix, start_x, start_y, cell_width, cell_height):
    for i in range(USERS):
        for j in range(ITEMS):
            rect = pygame.Rect(start_x + j * cell_width, start_y + i * cell_height, cell_width, cell_height)
            pygame.draw.rect(screen, GRAY, rect, 1)
            
            if current_state == ORIGINAL:
                value = matrix[i][j]
            elif current_state == COLLABORATIVE_FILTERING:
                value = matrix[i][j] if matrix[i][j] != 0 else random.randint(0, 5) if random.random() < 0.3 else 0
            else:  # Matrix Factorization
                value = matrix[i][j] if matrix[i][j] != 0 else random.randint(1, 5)

            if value != 0:
                color = pygame.Color(0)
                color.hsva = (value * 30, 80, 100, 100)
                pygame.draw.rect(screen, color, rect)
                text = text_font.render(str(value), True, WHITE)
                screen.blit(text, (rect.centerx - text.get_width() // 2, rect.centery - text.get_height() // 2))

def draw_explanation():
    if current_state == ORIGINAL:
        explanation = "Original sparse data matrix. Empty cells represent missing ratings."
        sub_explanation = "This reflects real-world scenarios where most users rate only a few items."
    elif current_state == COLLABORATIVE_FILTERING:
        explanation = "Collaborative Filtering: Predicts some missing values based on similar users/items."
        sub_explanation = "Leverages patterns in existing ratings to estimate missing ones."
    else:
        explanation = "Matrix Factorization: Decomposes the matrix to predict all missing values."
        sub_explanation = "Finds latent features to represent users and items, enabling complete predictions."

    explanation_text = subtitle_font.render(explanation, True, WHITE)
    sub_explanation_text = text_font.render(sub_explanation, True, GRAY)
    screen.blit(explanation_text, (WIDTH // 2 - explanation_text.get_width() // 2, HEIGHT - 200))
    screen.blit(sub_explanation_text, (WIDTH // 2 - sub_explanation_text.get_width() // 2, HEIGHT - 160))

def draw_heatmap_legend():
    legend_width = 200
    legend_height = 20
    legend_x = WIDTH - legend_width - 50
    legend_y = HEIGHT - 150

    for i in range(legend_width):
        color = pygame.Color(0)
        color.hsva = (i / legend_width * 180, 80, 100, 100)
        pygame.draw.line(screen, color, (legend_x + i, legend_y), (legend_x + i, legend_y + legend_height))

    pygame.draw.rect(screen, WHITE, (legend_x, legend_y, legend_width, legend_height), 1)
    
    low_text = text_font.render("Low", True, WHITE)
    high_text = text_font.render("High", True, WHITE)
    screen.blit(low_text, (legend_x - 10, legend_y + legend_height + 5))
    screen.blit(high_text, (legend_x + legend_width - 30, legend_y + legend_height + 5))

# Main game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        for button in buttons:
            button.handle_event(event)

    screen.fill(BACKGROUND)

    # Draw title and subtitle
    title = title_font.render("Advanced Sparse Data Handling Visualizer", True, WHITE)
    subtitle = subtitle_font.render("Developed by: Venugopal Adep", True, GRAY)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 30))
    screen.blit(subtitle, (WIDTH // 2 - subtitle.get_width() // 2, 100))

    # Draw matrix
    cell_width, cell_height = 50, 40
    start_x, start_y = (WIDTH - ITEMS * cell_width) // 2, 180
    draw_matrix(matrix, start_x, start_y, cell_width, cell_height)

    # Draw buttons
    for button in buttons:
        button.draw(screen)

    # Draw explanation
    draw_explanation()

    # Draw heatmap legend
    draw_heatmap_legend()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()