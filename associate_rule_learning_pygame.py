import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 1600, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Association Rule Learning Demo")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Fonts
title_font = pygame.font.Font(None, 64)
subtitle_font = pygame.font.Font(None, 32)
item_font = pygame.font.Font(None, 24)
explanation_font = pygame.font.Font(None, 20)

# Items
items = ["Bread", "Milk", "Eggs", "Cheese", "Butter", "Jam", "Coffee", "Tea", "Sugar", "Cereal"]
item_colors = [RED, GREEN, BLUE, (255, 165, 0), (255, 192, 203), (128, 0, 128), (165, 42, 42), (0, 128, 0), (255, 255, 0), (255, 140, 0)]

# Shopping baskets
baskets = []
selected_items = []

# Association rules
rules = {}

class Item:
    def __init__(self, name, color, x, y):
        self.name = name
        self.color = color
        self.rect = pygame.Rect(x, y, 100, 40)

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)
        text = item_font.render(self.name, True, BLACK)
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)

class Button:
    def __init__(self, x, y, width, height, text, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)
        text = item_font.render(self.text, True, BLACK)
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)

def generate_items():
    return [Item(items[i], item_colors[i], 50 + (i % 5) * 150, 200 + (i // 5) * 100) for i in range(len(items))]

def generate_basket():
    return random.sample(item_objects, random.randint(2, 5))

def update_rules():
    global rules
    rules = {}
    for basket in baskets:
        for item1 in basket:
            for item2 in basket:
                if item1 != item2:
                    if item1.name not in rules:
                        rules[item1.name] = {}
                    if item2.name not in rules[item1.name]:
                        rules[item1.name][item2.name] = 0
                    rules[item1.name][item2.name] += 1

def draw_rules():
    y = 550
    for item1, associated_items in rules.items():
        text = subtitle_font.render(f"{item1} is often bought with:", True, BLACK)
        screen.blit(text, (1000, y))
        y += 30
        for item2, count in sorted(associated_items.items(), key=lambda x: x[1], reverse=True)[:3]:
            text = item_font.render(f"  - {item2} ({count} times)", True, BLACK)
            screen.blit(text, (1020, y))
            y += 25
        y += 20

def draw_explanation():
    explanations = [
        "Association Rule Learning is a method used in recommendation systems.",
        "It identifies patterns in data to predict future associations.",
        "In this demo:",
        "1. Each basket represents a customer's purchase.",
        "2. The system learns which items are frequently bought together.",
        "3. These patterns form 'rules' used for recommendations.",
        "4. More data (baskets) leads to more accurate rules.",
        "Real-world applications include:",
        "- 'Customers who bought X also bought Y'",
        "- Product placement in stores",
        "- Personalized marketing campaigns"
    ]
    y = 50
    for explanation in explanations:
        text = explanation_font.render(explanation, True, BLACK)
        screen.blit(text, (1000, y))
        y += 25

def reset_demo():
    global baskets, selected_items, rules
    baskets = []
    selected_items = []
    rules = {}

# Main game loop
running = True
item_objects = generate_items()
reset_button = Button(1400, 700, 150, 50, "Reset Demo", GRAY)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for item in item_objects:
                if item.rect.collidepoint(event.pos):
                    if item in selected_items:
                        selected_items.remove(item)
                    else:
                        selected_items.append(item)
            if reset_button.rect.collidepoint(event.pos):
                reset_demo()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if selected_items:
                    baskets.append(selected_items.copy())
                    selected_items.clear()
                    update_rules()
            elif event.key == pygame.K_SPACE:
                new_basket = generate_basket()
                baskets.append(new_basket)
                update_rules()

    # Clear the screen
    screen.fill(WHITE)

    # Draw title and subtitle
    title_text = title_font.render("Association Rule Learning Demo", True, BLACK)
    subtitle_text = subtitle_font.render("Developed by: Venugopal Adep", True, BLACK)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 20))
    screen.blit(subtitle_text, (WIDTH // 2 - subtitle_text.get_width() // 2, 80))

    # Draw items
    for item in item_objects:
        item.draw()

    # Draw selected items
    for i, item in enumerate(selected_items):
        pygame.draw.rect(screen, item.color, (50 + i * 110, 450, 100, 40))
        text = item_font.render(item.name, True, BLACK)
        screen.blit(text, (55 + i * 110, 460))

    # Draw instructions
    instructions = [
        "Click on items to add/remove from basket",
        "Press ENTER to confirm basket",
        "Press SPACE to generate random basket",
        "Watch the association rules update!"
    ]
    for i, instruction in enumerate(instructions):
        text = item_font.render(instruction, True, BLACK)
        screen.blit(text, (50, 520 + i * 30))

    # Draw rules
    draw_rules()

    # Draw explanation
    draw_explanation()

    # Draw reset button
    reset_button.draw()

    # Draw basket count
    basket_count_text = subtitle_font.render(f"Total Baskets: {len(baskets)}", True, BLACK)
    screen.blit(basket_count_text, (50, 650))

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()