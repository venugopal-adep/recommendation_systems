import pygame
import math

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 1600, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cosine Similarity Demo")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)
LIGHT_GRAY = (240, 240, 240)

# Fonts
title_font = pygame.font.Font(None, 64)
text_font = pygame.font.Font(None, 32)
math_font = pygame.font.Font(None, 24)

# Vector properties
center_x, center_y = WIDTH // 2, HEIGHT // 2
vector_length = 300
vector1 = [1, 0]
vector2 = [1, 0]

def draw_vector(start, end, color):
    pygame.draw.line(screen, color, start, end, 3)
    angle = math.atan2(end[1] - start[1], end[0] - start[0])
    pygame.draw.polygon(screen, color, [
        end,
        (end[0] - 15 * math.cos(angle - math.pi/6), end[1] - 15 * math.sin(angle - math.pi/6)),
        (end[0] - 15 * math.cos(angle + math.pi/6), end[1] - 15 * math.sin(angle + math.pi/6))
    ])

def calculate_cosine_similarity(v1, v2):
    dot_product = v1[0] * v2[0] + v1[1] * v2[1]
    magnitude1 = math.sqrt(v1[0]**2 + v1[1]**2)
    magnitude2 = math.sqrt(v2[0]**2 + v2[1]**2)
    return dot_product / (magnitude1 * magnitude2)

def draw_text(text, font, color, x, y, align="left"):
    rendered_text = font.render(text, True, color)
    if align == "center":
        x -= rendered_text.get_width() // 2
    elif align == "right":
        x -= rendered_text.get_width()
    screen.blit(rendered_text, (x, y))

def draw_math_box(x, y, width, height):
    pygame.draw.rect(screen, LIGHT_GRAY, (x, y, width, height))
    pygame.draw.rect(screen, BLACK, (x, y, width, height), 2)

running = True
clock = pygame.time.Clock()
show_explanation = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if mouse_x < center_x:
                    vector1 = [mouse_x - center_x, mouse_y - center_y]
                else:
                    vector2 = [mouse_x - center_x, mouse_y - center_y]
            elif event.button == 3:  # Right mouse button
                show_explanation = not show_explanation
        elif event.type == pygame.MOUSEMOTION:
            if pygame.mouse.get_pressed()[0]:  # Left mouse button
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if mouse_x < center_x:
                    vector1 = [mouse_x - center_x, mouse_y - center_y]
                else:
                    vector2 = [mouse_x - center_x, mouse_y - center_y]

    screen.fill(WHITE)

    # Draw title and developer info
    draw_text("Cosine Similarity Demo", title_font, BLACK, WIDTH // 2, 20, "center")
    draw_text("Developed by: Venugopal Adep", text_font, BLACK, WIDTH // 2, 80, "center")

    # Draw coordinate system
    pygame.draw.line(screen, GRAY, (center_x, 0), (center_x, HEIGHT), 1)
    pygame.draw.line(screen, GRAY, (0, center_y), (WIDTH, center_y), 1)

    # Draw vectors
    v1_end = (center_x + vector1[0], center_y + vector1[1])
    v2_end = (center_x + vector2[0], center_y + vector2[1])
    draw_vector((center_x, center_y), v1_end, RED)
    draw_vector((center_x, center_y), v2_end, BLUE)

    # Calculate cosine similarity
    cos_sim = calculate_cosine_similarity(vector1, vector2)

    # Draw angle arc
    angle = math.atan2(vector2[1], vector2[0]) - math.atan2(vector1[1], vector1[0])
    pygame.draw.arc(screen, BLACK, (center_x - 50, center_y - 50, 100, 100), 
                    -math.atan2(vector1[1], vector1[0]), -math.atan2(vector2[1], vector2[0]), 2)

    # Display cosine similarity and angle
    draw_text(f"Cosine Similarity: {cos_sim:.4f}", text_font, BLACK, 20, HEIGHT - 60)
    draw_text(f"Angle: {math.degrees(abs(angle)):.2f}°", text_font, BLACK, 20, HEIGHT - 30)

    # Display instructions
    draw_text("Left-click and drag to move vectors", text_font, BLACK, WIDTH - 20, HEIGHT - 60, "right")
    draw_text("Right-click to toggle explanation", text_font, BLACK, WIDTH - 20, HEIGHT - 30, "right")

    if show_explanation:
        # Draw explanation box
        explanation_width, explanation_height = 600, 400
        explanation_x = (WIDTH - explanation_width) // 2
        explanation_y = (HEIGHT - explanation_height) // 2
        draw_math_box(explanation_x, explanation_y, explanation_width, explanation_height)

        # Explanation text
        explanation = [
            "Cosine Similarity Explained:",
                       "Cosine similarity measures the cosine of the angle between two vectors.",
            "It ranges from -1 (opposite directions) to 1 (same direction).",
            "",
            "Formula:",
            "cos(θ) = (A · B) / (||A|| * ||B||)",
            "",
            "Where:",
            "A · B = dot product of vectors A and B",
            "||A|| and ||B|| = magnitudes (lengths) of vectors A and B",
            "",
            "Applications:",
            "- Text analysis: Compare document similarities",
            "- Recommendation systems: Find similar items or users",
            "- Image recognition: Compare feature vectors",
        ]

        for i, line in enumerate(explanation):
            draw_text(line, math_font, BLACK, explanation_x + 20, explanation_y + 20 + i * 25)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()