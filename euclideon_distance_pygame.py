import pygame
import math
import random

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 1600, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Euclidean Distance Visualizer")

# Colors
BACKGROUND = (240, 248, 255)  # Alice Blue
TITLE = (70, 130, 180)  # Steel Blue
TEXT = (47, 79, 79)  # Dark Slate Gray
POINT1 = (255, 99, 71)  # Tomato
POINT2 = (65, 105, 225)  # Royal Blue
LINE = (50, 205, 50)  # Lime Green
COMPONENT = (255, 165, 0)  # Orange

# Fonts
title_font = pygame.font.Font(None, 72)
text_font = pygame.font.Font(None, 36)

# Points
point1 = [400, 450]
point2 = [800, 450]

# Function to calculate Euclidean distance
def euclidean_distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

# Button class
class Button:
    def __init__(self, x, y, width, height, text, color, text_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.text_color = text_color

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect, border_radius=10)
        text_surf = text_font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# Create buttons
toggle_components_button = Button(20, HEIGHT - 180, 300, 50, "Toggle Components", TITLE, BACKGROUND)
random_points_button = Button(20, HEIGHT - 120, 300, 50, "Random Points", TITLE, BACKGROUND)

# Main game loop
running = True
dragging = None
show_components = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if math.dist(mouse_pos, point1) < 20:
                dragging = point1
            elif math.dist(mouse_pos, point2) < 20:
                dragging = point2
            elif toggle_components_button.is_clicked(mouse_pos):
                show_components = not show_components
            elif random_points_button.is_clicked(mouse_pos):
                point1 = [random.randint(100, WIDTH-100), random.randint(100, HEIGHT-200)]
                point2 = [random.randint(100, WIDTH-100), random.randint(100, HEIGHT-200)]
        elif event.type == pygame.MOUSEBUTTONUP:
            dragging = None

    # Update point position if dragging
    if dragging:
        dragging[0], dragging[1] = pygame.mouse.get_pos()

    # Clear the screen
    screen.fill(BACKGROUND)

    # Draw title and developer info
    title_text = title_font.render("Euclidean Distance Visualizer", True, TITLE)
    screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, 20))
    
    dev_text = text_font.render("Developed by: Venugopal Adep", True, TEXT)
    screen.blit(dev_text, (WIDTH//2 - dev_text.get_width()//2, 100))

    # Draw points
    pygame.draw.circle(screen, POINT1, point1, 20)
    pygame.draw.circle(screen, POINT2, point2, 20)

    # Draw line between points
    pygame.draw.line(screen, LINE, point1, point2, 3)

    # Calculate and display distance
    distance = euclidean_distance(point1, point2)
    distance_text = text_font.render(f"Distance: {distance:.2f}", True, TEXT)
    screen.blit(distance_text, (WIDTH//2 - distance_text.get_width()//2, HEIGHT - 50))

    # Show distance components
    if show_components:
        pygame.draw.line(screen, COMPONENT, (point1[0], point1[1]), (point2[0], point1[1]), 2)
        pygame.draw.line(screen, COMPONENT, (point2[0], point1[1]), point2, 2)
        
        dx = abs(point2[0] - point1[0])
        dy = abs(point2[1] - point1[1])
        
        dx_text = text_font.render(f"dx: {dx:.2f}", True, TEXT)
        dy_text = text_font.render(f"dy: {dy:.2f}", True, TEXT)
        
        screen.blit(dx_text, (WIDTH//2 - dx_text.get_width()//2, HEIGHT - 120))
        screen.blit(dy_text, (WIDTH//2 - dy_text.get_width()//2, HEIGHT - 80))

    # Draw buttons
    toggle_components_button.draw()
    random_points_button.draw()

    # Display instructions
    instructions = [
        "Drag the red and blue points to see distance change",
        "Use buttons to toggle components or randomize points"
    ]
    for i, instruction in enumerate(instructions):
        inst_text = text_font.render(instruction, True, TEXT)
        screen.blit(inst_text, (WIDTH - inst_text.get_width() - 20, HEIGHT - 80 + i * 40))

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()