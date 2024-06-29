import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 1600, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("E-commerce Personalized Product Recommendations")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (240, 240, 240)
LIGHT_BLUE = (230, 240, 250)
DARK_BLUE = (0, 80, 155)
RED = (220, 60, 60)
GREEN = (60, 180, 75)
ORANGE = (255, 165, 0)

# Fonts
title_font = pygame.font.Font(None, 54)
subtitle_font = pygame.font.Font(None, 40)
text_font = pygame.font.Font(None, 28)

# Product categories and items
categories = ["Electronics", "Clothing", "Books", "Home & Garden"]
products = {
    "Electronics": ["Smartphone", "Laptop", "Headphones", "Smartwatch", "Tablet"],
    "Clothing": ["T-shirt", "Jeans", "Dress", "Jacket", "Shoes"],
    "Books": ["Fiction", "Non-fiction", "Science", "History", "Self-help"],
    "Home & Garden": ["Plant", "Furniture", "Kitchenware", "Decor", "Tools"]
}

# User profiles
users = [
    {"name": "Alice", "interests": ["Electronics", "Books"]},
    {"name": "Bob", "interests": ["Clothing", "Home & Garden"]},
    {"name": "Charlie", "interests": ["Books", "Electronics"]}
]

current_user = random.choice(users)
browsing_history = []
purchase_history = []
recommendations = []
recommendation_timer = 0
RECOMMENDATION_DELAY = 5000  # 5 seconds

def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    screen.blit(text_surface, text_rect)

def draw_button(text, x, y, width, height, color, hover_color, text_color=BLACK):
    mouse_pos = pygame.mouse.get_pos()
    if x <= mouse_pos[0] <= x + width and y <= mouse_pos[1] <= y + height:
        pygame.draw.rect(screen, hover_color, (x, y, width, height))
    else:
        pygame.draw.rect(screen, color, (x, y, width, height))
    pygame.draw.rect(screen, DARK_BLUE, (x, y, width, height), 2)
    text_rect = text_font.render(text, True, text_color).get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text_font.render(text, True, text_color), text_rect)

def get_recommendations():
    recommendations = []
    for category in current_user["interests"]:
        recommendations.extend(random.sample(products[category], 2))
    return recommendations

def draw_section(title, items, x, y, width, height):
    pygame.draw.rect(screen, LIGHT_BLUE, (x, y, width, height))
    pygame.draw.rect(screen, DARK_BLUE, (x, y, width, height), 2)
    draw_text(title, subtitle_font, DARK_BLUE, x + 20, y + 20)
    for i, item in enumerate(items[-5:]):
        draw_text(f"• {item}", text_font, BLACK, x + 30, y + 70 + i * 40)

def main():
    global current_user, browsing_history, purchase_history, recommendations, recommendation_timer

    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill(WHITE)

        # Draw title and developer info
        pygame.draw.rect(screen, LIGHT_BLUE, (0, 0, WIDTH, 100))
        draw_text("E-commerce Personalized Product Recommendations", title_font, DARK_BLUE, 20, 30)
        draw_text("Developed by: Venugopal Adep", text_font, BLACK, 20, 80)

        # Draw user info section
        pygame.draw.rect(screen, GRAY, (20, 120, 760, 100))
        draw_text(f"Current User: {current_user['name']}", subtitle_font, DARK_BLUE, 40, 130)
        draw_text(f"Interests: {', '.join(current_user['interests'])}", text_font, BLACK, 40, 180)

        # Draw browsing and purchase history sections
        draw_section("Browsing History", browsing_history, 20, 240, 370, 300)
        draw_section("Purchase History", purchase_history, 410, 240, 370, 300)

        # Draw recommendations section
        pygame.draw.rect(screen, LIGHT_BLUE, (800, 120, 780, 620))
        pygame.draw.rect(screen, DARK_BLUE, (800, 120, 780, 620), 2)
        draw_text("Recommended Products", subtitle_font, DARK_BLUE, 820, 130)
        
        current_time = pygame.time.get_ticks()
        if current_time - recommendation_timer > RECOMMENDATION_DELAY:
            recommendations = get_recommendations()
            recommendation_timer = current_time

        for i, item in enumerate(recommendations):
            draw_button(item, 820, 180 + i * 70, 300, 60, WHITE, GRAY)

        # Draw action buttons
        draw_button("Browse Random Product", 20, 560, 250, 60, ORANGE, LIGHT_BLUE)
        draw_button("Purchase Random Product", 290, 560, 250, 60, GREEN, LIGHT_BLUE)
        draw_button("Switch User", 560, 560, 250, 60, RED, LIGHT_BLUE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if 20 <= x <= 270 and 560 <= y <= 620:  # Browse Random Product
                    category = random.choice(categories)
                    product = random.choice(products[category])
                    browsing_history.append(product)
                elif 290 <= x <= 540 and 560 <= y <= 620:  # Purchase Random Product
                    category = random.choice(categories)
                    product = random.choice(products[category])
                    purchase_history.append(product)
                elif 560 <= x <= 810 and 560 <= y <= 620:  # Switch User
                    current_user = random.choice(users)
                    browsing_history = []
                    purchase_history = []
                    recommendations = get_recommendations()
                    recommendation_timer = pygame.time.get_ticks()
                # Check if a recommended product is clicked
                for i, item in enumerate(recommendations):
                    if 820 <= x <= 1120 and 180 + i * 70 <= y <= 240 + i * 70:
                        browsing_history.append(item)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()