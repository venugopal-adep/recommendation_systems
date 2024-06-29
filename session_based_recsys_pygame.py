import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 1920, 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Advanced Session-Based Recommendations Visualizer")

# Colors
BACKGROUND = (15, 20, 30)
WHITE = (240, 240, 240)
BLACK = (10, 10, 10)
GRAY = (100, 100, 100)
BLUE = (41, 128, 185)
GREEN = (39, 174, 96)
RED = (231, 76, 60)
YELLOW = (241, 196, 15)
PURPLE = (142, 68, 173)

# Fonts
title_font = pygame.font.Font(None, 64)
subtitle_font = pygame.font.Font(None, 36)
text_font = pygame.font.Font(None, 28)

# Product categories
categories = ["Electronics", "Books", "Clothing", "Home", "Sports"]
products = {
    "Electronics": ["Laptop", "Smartphone", "Headphones", "Tablet", "Camera", "Smartwatch", "Speaker"],
    "Books": ["Fiction", "Non-fiction", "Science", "History", "Biography", "Fantasy", "Mystery"],
    "Clothing": ["T-shirt", "Jeans", "Dress", "Shoes", "Jacket", "Sweater", "Accessories"],
    "Home": ["Furniture", "Decor", "Kitchenware", "Bedding", "Lighting", "Appliances", "Storage"],
    "Sports": ["Running Shoes", "Yoga Mat", "Tennis Racket", "Basketball", "Weights", "Bicycle", "Swimming Gear"]
}

# Session state
current_session = []
recommendations = []

# Button class
class Button:
    def __init__(self, x, y, width, height, text, color, text_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.text_color = text_color
        self.hover_color = tuple(min(c + 30, 255) for c in color)

    def draw(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, self.hover_color, self.rect, border_radius=10)
        else:
            pygame.draw.rect(screen, self.color, self.rect, border_radius=10)
        pygame.draw.rect(screen, WHITE, self.rect, 2, border_radius=10)
        text_surface = text_font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# Create category buttons
category_buttons = [Button(50 + i * 300, 150, 250, 50, category, BLUE, WHITE) for i, category in enumerate(categories)]

# Create product buttons (initially hidden)
product_buttons = []

# Create "Clear Session" button
clear_button = Button(WIDTH - 250, HEIGHT - 100, 200, 60, "Clear Session", RED, WHITE)

# Function to generate recommendations based on the current session
def generate_recommendations():
    global recommendations
    if not current_session:
        recommendations = []
        return

    last_category = current_session[-1][0]
    last_product = current_session[-1][1]
    
    # Enhanced recommendation logic
    if len(current_session) == 1:
        # If only one item in session, suggest from the same category
        recommendations = random.sample([p for p in products[last_category] if p != last_product], min(3, len(products[last_category]) - 1))
    else:
        # Consider the last two items for more context
        second_last_category = current_session[-2][0]
        if second_last_category == last_category:
            # If same category, suggest from a different category
            other_categories = [c for c in categories if c != last_category]
            rec_category = random.choice(other_categories)
            recommendations = random.sample(products[rec_category], 3)
        else:
            # If different categories, suggest a mix
            rec_from_last = random.sample([p for p in products[last_category] if p != last_product], 2)
            rec_from_second_last = random.sample(products[second_last_category], 1)
            recommendations = rec_from_last + rec_from_second_last

# Function to draw a panel
def draw_panel(x, y, width, height, title, items):
    pygame.draw.rect(screen, GRAY, (x, y, width, height), border_radius=10)
    pygame.draw.rect(screen, WHITE, (x, y, width, height), 2, border_radius=10)
    title_surface = subtitle_font.render(title, True, WHITE)
    screen.blit(title_surface, (x + 10, y + 10))
    for i, item in enumerate(items):
        item_text = text_font.render(f"{i + 1}. {item}", True, WHITE)
        screen.blit(item_text, (x + 20, y + 50 + i * 30))

# Main game loop
running = True
selected_category = None

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            
            # Check category buttons
            for button in category_buttons:
                if button.is_clicked(pos):
                    selected_category = button.text
                    product_buttons = [Button(50 + i * 230, 250, 200, 50, product, GREEN, BLACK) for i, product in enumerate(products[selected_category])]
            
            # Check product buttons
            for button in product_buttons:
                if button.is_clicked(pos):
                    current_session.append((selected_category, button.text))
                    generate_recommendations()
            
            # Check clear button
            if clear_button.is_clicked(pos):
                current_session = []
                recommendations = []
                selected_category = None
                product_buttons = []

    # Clear the screen
    screen.fill(BACKGROUND)

    # Draw title and subtitle
    title_text = title_font.render("Advanced Session-Based Recommendations Visualizer", True, WHITE)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 20))

    subtitle_text = subtitle_font.render("Developed by: Venugopal Adep", True, GRAY)
    screen.blit(subtitle_text, (WIDTH // 2 - subtitle_text.get_width() // 2, 80))

    # Draw category buttons
    for button in category_buttons:
        button.draw()

    # Draw product buttons if a category is selected
    if selected_category:
        for button in product_buttons:
            button.draw()

    # Draw clear button
    clear_button.draw()

    # Display current session
    draw_panel(50, 350, 600, 300, "Current Session", [f"{category}: {product}" for category, product in current_session])

    # Display recommendations
    draw_panel(700, 350, 600, 300, "Recommendations", recommendations)

    # Draw explanation
    explanation_text = [
        "This demo showcases session-based recommendations.",
        "Select a category, then click on products to add them to your session.",
        "The system will generate recommendations based on your choices.",
        "Try different combinations to see how recommendations change!"
    ]
    for i, line in enumerate(explanation_text):
        text_surface = text_font.render(line, True, WHITE)
        screen.blit(text_surface, (50, HEIGHT - 150 + i * 30))

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()