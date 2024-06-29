import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 1600, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Advanced Recommendation System Demo")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 50, 50)
GREEN = (50, 255, 50)
BLUE = (50, 50, 255)
YELLOW = (255, 255, 50)
GRAY = (200, 200, 200)
LIGHT_GRAY = (230, 230, 230)
DARK_GRAY = (100, 100, 100)
PURPLE = (180, 0, 180)
ORANGE = (255, 165, 0)
CYAN = (0, 255, 255)

# Fonts
title_font = pygame.font.Font(None, 48)
subtitle_font = pygame.font.Font(None, 36)
text_font = pygame.font.Font(None, 24)

# Product class
class Product:
    def __init__(self, name, category, price):
        self.name = name
        self.category = category
        self.price = price
        self.explicit_rating = 0
        self.view_time = 0
        self.purchases = 0

# Create products
products = [
    Product("Laptop", "Electronics", 999),
    Product("Smartphone", "Electronics", 699),
    Product("Headphones", "Audio", 199),
    Product("Smartwatch", "Wearables", 299),
    Product("Tablet", "Electronics", 499),
    Product("Camera", "Electronics", 599),
    Product("Speaker", "Audio", 149),
    Product("Fitness Tracker", "Wearables", 99)
]

# Game variables
current_product = 0
viewing_start_time = pygame.time.get_ticks()
is_viewing = True
show_explanation = False

# Helper functions
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

def draw_product(product, x, y):
    pygame.draw.rect(screen, LIGHT_GRAY, (x - 150, y - 120, 300, 240), border_radius=10)
    pygame.draw.rect(screen, DARK_GRAY, (x - 150, y - 120, 300, 240), 2, border_radius=10)
    
    draw_text(product.name, subtitle_font, BLACK, x, y - 90, align="center")
    draw_text(f"Category: {product.category}", text_font, DARK_GRAY, x, y - 50, align="center")
    draw_text(f"Price: ${product.price}", text_font, DARK_GRAY, x, y - 20, align="center")
    
    # Explicit feedback (star rating)
    for i in range(5):
        if i < product.explicit_rating:
            color = YELLOW
        else:
            color = GRAY
        pygame.draw.polygon(screen, color, 
                            [(x - 60 + i*30, y + 20), 
                             (x - 50 + i*30, y + 40), 
                             (x - 60 + i*30, y + 60), 
                             (x - 70 + i*30, y + 40)])

    # Implicit feedback
    draw_text(f"View time: {product.view_time:.1f}s", text_font, DARK_GRAY, x, y + 80, align="center")
    draw_text(f"Purchases: {product.purchases}", text_font, DARK_GRAY, x, y + 110, align="center")

def draw_buttons():
    pygame.draw.rect(screen, GREEN, (WIDTH - 250, HEIGHT - 180, 220, 50), border_radius=10)
    draw_text("Purchase", subtitle_font, BLACK, WIDTH - 140, HEIGHT - 155, align="center")
    
    pygame.draw.rect(screen, BLUE, (WIDTH - 250, HEIGHT - 120, 220, 50), border_radius=10)
    draw_text("Next Product", subtitle_font, BLACK, WIDTH - 140, HEIGHT - 95, align="center")

def draw_recommendation():
    recommendations = get_recommendations()
    
    pygame.draw.rect(screen, LIGHT_GRAY, (50, HEIGHT - 250, WIDTH - 100, 200), border_radius=10)
    pygame.draw.rect(screen, DARK_GRAY, (50, HEIGHT - 250, WIDTH - 100, 200), 2, border_radius=10)
    
    draw_text("Top Recommendations", subtitle_font, BLACK, WIDTH // 2, HEIGHT - 220, align="center")
    
    for i, (product, score) in enumerate(recommendations[:3]):
        draw_text(f"{i+1}. {product.name} (Score: {score:.2f})", text_font, BLACK, 100, HEIGHT - 180 + i*40)
    
    draw_text("Recommendation factors: View time (30%), Purchases (30%), Explicit Rating (40%)", 
              text_font, DARK_GRAY, WIDTH // 2, HEIGHT - 80, align="center")

def get_recommendations():
    scores = []
    for product in products:
        view_time_score = min(product.view_time / 10, 5)  # Cap at 5
        purchase_score = min(product.purchases * 2, 5)  # Cap at 5
        explicit_score = product.explicit_rating
        
        total_score = (view_time_score * 0.3) + (purchase_score * 0.3) + (explicit_score * 0.4)
        scores.append((product, total_score))
    
    return sorted(scores, key=lambda x: x[1], reverse=True)

def draw_explanation():
    pygame.draw.rect(screen, LIGHT_GRAY, (50, 50, WIDTH - 100, HEIGHT - 100), border_radius=10)
    pygame.draw.rect(screen, DARK_GRAY, (50, 50, WIDTH - 100, HEIGHT - 100), 2, border_radius=10)
    
    draw_text("Advanced Recommendation System Explanation", title_font, BLACK, WIDTH // 2, 100, align="center")
    
    explanation_text = [
        "This demo showcases a hybrid recommendation system using both implicit and explicit feedback:",
        "",
        "1. Implicit Feedback:",
        "   - View Time: Measures user interest based on time spent viewing a product",
        "   - Purchases: Indicates strong user preference for a product",
        "",
        "2. Explicit Feedback:",
        "   - Star Ratings: Direct user evaluation of a product",
        "",
        "The recommendation algorithm combines these factors with the following weights:",
        "- View Time: 30%",
        "- Purchases: 30%",
        "- Explicit Rating: 40%",
        "",
        "This balanced approach leverages both user behavior and direct feedback to provide",
        "more accurate and personalized recommendations."
    ]
    
    for i, line in enumerate(explanation_text):
        draw_text(line, text_font, BLACK, 100, 180 + i * 30)
    
    draw_text("Click anywhere to close", text_font, BLACK, WIDTH // 2, HEIGHT - 100, align="center")

# Main game loop
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if show_explanation:
                show_explanation = False
            else:
                x, y = pygame.mouse.get_pos()
                
                # Purchase button
                if WIDTH - 250 <= x <= WIDTH - 30 and HEIGHT - 180 <= y <= HEIGHT - 130:
                    products[current_product].purchases += 1
                
                # Next product button
                elif WIDTH - 250 <= x <= WIDTH - 30 and HEIGHT - 120 <= y <= HEIGHT - 70:
                    if is_viewing:
                        products[current_product].view_time += (pygame.time.get_ticks() - viewing_start_time) / 1000
                    current_product = (current_product + 1) % len(products)
                    viewing_start_time = pygame.time.get_ticks()
                    is_viewing = True
                
                # Star rating
                elif WIDTH//2 - 60 <= x <= WIDTH//2 + 90 and HEIGHT//2 - 80 <= y <= HEIGHT//2 - 40:
                    products[current_product].explicit_rating = min(5, max(1, (x - (WIDTH//2 - 60)) // 30 + 1))
                
                # Show explanation
                elif 20 <= x <= 270 and 20 <= y <= 70:
                    show_explanation = True

    # Update view time
    if is_viewing:
        products[current_product].view_time += clock.get_time() / 1000

    # Draw everything
    screen.fill(WHITE)
    
    if show_explanation:
        draw_explanation()
    else:
        # Title and author
        draw_text("Advanced Recommendation System Demo", title_font, BLACK, WIDTH//2, 50, align="center")
        draw_text("Developed by: Venugopal Adep", subtitle_font, PURPLE, WIDTH//2, 100, align="center")

        # Instructions
        draw_text("Click on stars to rate (Explicit). View time and purchases are tracked (Implicit).", text_font, BLACK, WIDTH//2, 150, align="center")

        # Current product
        draw_product(products[current_product], WIDTH // 2, HEIGHT // 2 - 50)

        # Buttons
        draw_buttons()

        # Explanation button
        pygame.draw.rect(screen, ORANGE, (20, 20, 250, 50), border_radius=10)
        draw_text("Show Explanation", subtitle_font, BLACK, 145, 45, align="center")

        # Recommendation
        draw_recommendation()

    # Update display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()