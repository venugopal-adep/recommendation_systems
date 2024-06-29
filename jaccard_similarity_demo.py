import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 1600, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jaccard Similarity Demo")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 128)
GREEN = (0, 255, 0)

# Fonts
title_font = pygame.font.Font(None, 64)
text_font = pygame.font.Font(None, 32)

# Sets
set_a = set()
set_b = set()

# Circles
CIRCLE_RADIUS = 200
CIRCLE_CENTER_A = (WIDTH // 2 - 150, HEIGHT // 2)
CIRCLE_CENTER_B = (WIDTH // 2 + 150, HEIGHT // 2)

# Buttons
ADD_RANDOM_BUTTON = pygame.Rect(20, 120, 200, 50)
REMOVE_RANDOM_BUTTON = pygame.Rect(20, 180, 200, 50)

# Jaccard Similarity
jaccard_similarity = 0

def draw_text():
    title = title_font.render("Jaccard Similarity Demo", True, BLACK)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 20))

    developer = text_font.render("Developed by: Venugopal Adep", True, BLACK)
    screen.blit(developer, (WIDTH // 2 - developer.get_width() // 2, 80))

    instruction1 = text_font.render("Click inside the circles to add elements", True, BLACK)
    screen.blit(instruction1, (20, HEIGHT - 90))

    instruction2 = text_font.render("Press SPACE to reset", True, BLACK)
    screen.blit(instruction2, (20, HEIGHT - 60))

    instruction3 = text_font.render("Right-click to remove elements", True, BLACK)
    screen.blit(instruction3, (20, HEIGHT - 30))

def draw_circles():
    pygame.draw.circle(screen, RED, CIRCLE_CENTER_A, CIRCLE_RADIUS, 2)
    pygame.draw.circle(screen, BLUE, CIRCLE_CENTER_B, CIRCLE_RADIUS, 2)

def draw_elements():
    for elem in set_a:
        pygame.draw.circle(screen, RED, elem, 5)
    for elem in set_b:
        pygame.draw.circle(screen, BLUE, elem, 5)
    for elem in set_a.intersection(set_b):
        pygame.draw.circle(screen, PURPLE, elem, 5)

def calculate_jaccard_similarity():
    global jaccard_similarity
    intersection = len(set_a.intersection(set_b))
    union = len(set_a.union(set_b))
    jaccard_similarity = intersection / union if union > 0 else 0

def draw_jaccard_similarity():
    text = text_font.render(f"Jaccard Similarity: {jaccard_similarity:.2f}", True, BLACK)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT - 50))

def is_inside_circle(pos, center):
    return math.dist(pos, center) <= CIRCLE_RADIUS

def add_element(pos):
    in_a = is_inside_circle(pos, CIRCLE_CENTER_A)
    in_b = is_inside_circle(pos, CIRCLE_CENTER_B)
    if in_a and in_b:
        set_a.add(pos)
        set_b.add(pos)
    elif in_a:
        set_a.add(pos)
    elif in_b:
        set_b.add(pos)
    calculate_jaccard_similarity()

def remove_element(pos):
    set_a.discard(pos)
    set_b.discard(pos)
    calculate_jaccard_similarity()

def add_random_elements():
    for _ in range(5):
        angle = random.uniform(0, 2 * math.pi)
        radius = random.uniform(0, CIRCLE_RADIUS)
        x = int(CIRCLE_CENTER_A[0] + radius * math.cos(angle))
        y = int(CIRCLE_CENTER_A[1] + radius * math.sin(angle))
        add_element((x, y))

        angle = random.uniform(0, 2 * math.pi)
        radius = random.uniform(0, CIRCLE_RADIUS)
        x = int(CIRCLE_CENTER_B[0] + radius * math.cos(angle))
        y = int(CIRCLE_CENTER_B[1] + radius * math.sin(angle))
        add_element((x, y))

def remove_random_elements():
    if set_a:
        elem = random.choice(list(set_a))
        set_a.remove(elem)
        set_b.discard(elem)
    if set_b:
        elem = random.choice(list(set_b))
        set_b.remove(elem)
        set_a.discard(elem)
    calculate_jaccard_similarity()

def draw_buttons():
    pygame.draw.rect(screen, GREEN, ADD_RANDOM_BUTTON)
    add_text = text_font.render("Add Random", True, BLACK)
    screen.blit(add_text, (ADD_RANDOM_BUTTON.x + 10, ADD_RANDOM_BUTTON.y + 15))

    pygame.draw.rect(screen, RED, REMOVE_RANDOM_BUTTON)
    remove_text = text_font.render("Remove Random", True, BLACK)
    screen.blit(remove_text, (REMOVE_RANDOM_BUTTON.x + 10, REMOVE_RANDOM_BUTTON.y + 15))

def main():
    global jaccard_similarity
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    if ADD_RANDOM_BUTTON.collidepoint(event.pos):
                        add_random_elements()
                    elif REMOVE_RANDOM_BUTTON.collidepoint(event.pos):
                        remove_random_elements()
                    else:
                        add_element(event.pos)
                elif event.button == 3:  # Right click
                    remove_element(event.pos)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    set_a.clear()
                    set_b.clear()
                    jaccard_similarity = 0

        screen.fill(WHITE)
        draw_circles()
        draw_elements()
        draw_text()
        draw_jaccard_similarity()
        draw_buttons()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()