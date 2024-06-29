import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 1600, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Content-Based Filtering: Item Profile Visualization")

# Colors
BACKGROUND = (240, 248, 255)  # Alice Blue
TEXT_COLOR = (47, 79, 79)  # Dark Slate Gray
ITEM_COLORS = [
    (255, 182, 193),  # Light Pink
    (173, 216, 230),  # Light Blue
    (144, 238, 144),  # Light Green
    (255, 218, 185),  # Peach Puff
    (221, 160, 221),  # Plum
]
FEATURE_COLOR = (255, 215, 0)  # Gold
HIGHLIGHT_COLOR = (255, 99, 71)  # Tomato
INFO_BOX_COLOR = (245, 245, 245)  # White Smoke
BUTTON_COLOR = (70, 130, 180)  # Steel Blue

# Fonts
title_font = pygame.font.Font(None, 56)
text_font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 28)

# Item class
class Item:
    def __init__(self, name, features):
        self.name = name
        self.features = features
        self.x = random.randint(100, WIDTH - 400)
        self.y = random.randint(250, HEIGHT - 100)
        self.radius = 40
        self.color = random.choice(ITEM_COLORS)
        
    def draw(self, selected=False):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
        if selected:
            pygame.draw.circle(screen, HIGHLIGHT_COLOR, (self.x, self.y), self.radius + 5, 3)
        name_text = small_font.render(self.name, True, TEXT_COLOR)
        screen.blit(name_text, (self.x - name_text.get_width() // 2, self.y - self.radius - 25))

# Feature class
class Feature:
    def __init__(self, name):
        self.name = name
        self.x = random.randint(WIDTH - 350, WIDTH - 100)
        self.y = random.randint(250, HEIGHT - 100)
        self.radius = 30
        
    def draw(self):
        pygame.draw.circle(screen, FEATURE_COLOR, (self.x, self.y), self.radius)
        name_text = small_font.render(self.name, True, TEXT_COLOR)
        screen.blit(name_text, (self.x - name_text.get_width() // 2, self.y - self.radius - 25))

# Button class
class Button:
    def __init__(self, x, y, width, height, text, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, TEXT_COLOR, self.rect, 2)
        text_surf = text_font.render(self.text, True, TEXT_COLOR)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# Create items and features
items = [
    Item("Movie A", ["Action", "Sci-Fi"]),
    Item("Movie B", ["Romance", "Comedy"]),
    Item("Movie C", ["Drama", "Thriller"]),
    Item("Movie D", ["Action", "Comedy"]),
    Item("Movie E", ["Sci-Fi", "Thriller"]),
]

features = [Feature(f) for f in ["Action", "Sci-Fi", "Romance", "Comedy", "Drama", "Thriller"]]

# Create reset button
reset_button = Button(WIDTH - 150, 20, 130, 50, "Reset", BUTTON_COLOR)

# Main game loop
running = True
selected_item = None
show_connections = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                mouse_pos = pygame.mouse.get_pos()
                if reset_button.is_clicked(mouse_pos):
                    selected_item = None
                    show_connections = False
                else:
                    for item in items:
                        distance = math.sqrt((mouse_pos[0] - item.x)**2 + (mouse_pos[1] - item.y)**2)
                        if distance <= item.radius:
                            selected_item = item
                            show_connections = True
                            break
                    else:
                        selected_item = None
                        show_connections = False

    # Clear the screen
    screen.fill(BACKGROUND)

    # Draw title and developer info
    title_text = title_font.render("Content-Based Filtering: Item Profile Visualization", True, TEXT_COLOR)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 30))
    
    dev_text = text_font.render("Developed by: Venugopal Adep", True, TEXT_COLOR)
    screen.blit(dev_text, (WIDTH // 2 - dev_text.get_width() // 2, 90))

    # Draw items and features
    for item in items:
        item.draw(item == selected_item)
    
    for feature in features:
        feature.draw()

    # Draw connections
    if show_connections and selected_item:
        for feature in features:
            if feature.name in selected_item.features:
                pygame.draw.line(screen, HIGHLIGHT_COLOR, (selected_item.x, selected_item.y), (feature.x, feature.y), 2)

    # Draw information box
    if selected_item:
        info_box = pygame.Rect(20, HEIGHT - 220, 300, 200)
        pygame.draw.rect(screen, INFO_BOX_COLOR, info_box)
        pygame.draw.rect(screen, TEXT_COLOR, info_box, 2)
        
        item_name = text_font.render(f"Item: {selected_item.name}", True, TEXT_COLOR)
        screen.blit(item_name, (info_box.x + 10, info_box.y + 10))
        
        feature_text = text_font.render("Features:", True, TEXT_COLOR)
        screen.blit(feature_text, (info_box.x + 10, info_box.y + 50))
        
        for i, feature in enumerate(selected_item.features):
            feature_item = small_font.render(f"- {feature}", True, TEXT_COLOR)
            screen.blit(feature_item, (info_box.x + 20, info_box.y + 90 + i * 30))

    # Draw instructions
    instructions = [
        "Instructions:",
        "- Click on an item to see its profile and connections",
        "- Click the Reset button or empty space to clear selection",
        "- Explore the relationships between items and features"
    ]
    
    instruction_box = pygame.Rect(WIDTH - 420, HEIGHT - 150, 400, 130)
    pygame.draw.rect(screen, INFO_BOX_COLOR, instruction_box)
    pygame.draw.rect(screen, TEXT_COLOR, instruction_box, 2)
    
    for i, instruction in enumerate(instructions):
        inst_text = small_font.render(instruction, True, TEXT_COLOR)
        screen.blit(inst_text, (instruction_box.x + 10, instruction_box.y + 10 + i * 30))

    # Draw reset button
    reset_button.draw()

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()