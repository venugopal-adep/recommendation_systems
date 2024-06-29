import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 1600, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("A/B Testing in Recommendation Systems Demo")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 20, 60)
BLUE = (30, 144, 255)
YELLOW = (255, 255, 0)
LIGHT_GRAY = (240, 240, 240)
DARK_GRAY = (100, 100, 100)
HEADER_BG = (50, 50, 50)

# Fonts
font_title = pygame.font.Font(None, 48)
font_subtitle = pygame.font.Font(None, 32)
font_text = pygame.font.Font(None, 24)

# Product class
class Product:
    def __init__(self, name, category, price):
        self.name = name
        self.category = category
        self.price = price

# User class
class User:
    def __init__(self, x, y, group):
        self.x = x
        self.y = y
        self.group = group  # 'A' or 'B'
        self.purchases = []
        self.satisfaction = random.uniform(0.5, 1.0)

    def draw(self):
        color = RED if self.group == 'A' else BLUE
        pygame.draw.circle(screen, color, (self.x, self.y), 8)
        pygame.draw.circle(screen, WHITE, (self.x, self.y), 8, 2)

# Create products
products = [
    Product("Laptop", "Electronics", 1000),
    Product("Smartphone", "Electronics", 500),
    Product("Headphones", "Electronics", 100),
    Product("T-shirt", "Clothing", 20),
    Product("Jeans", "Clothing", 50),
    Product("Sneakers", "Clothing", 80),
    Product("Book", "Media", 15),
    Product("Movie", "Media", 20),
    Product("Game", "Media", 60)
]

# Create users
users = []
for _ in range(200):
    x = random.randint(50, WIDTH - 50)
    y = random.randint(250, HEIGHT - 250)
    group = 'A' if random.random() < 0.5 else 'B'
    users.append(User(x, y, group))

# Recommendation algorithms
def recommend_a(user):
    # Algorithm A: Recommend based on most popular category
    category_counts = {}
    for purchase in user.purchases:
        category_counts[purchase.category] = category_counts.get(purchase.category, 0) + 1
    if category_counts:
        popular_category = max(category_counts, key=category_counts.get)
        recommendations = [p for p in products if p.category == popular_category and p not in user.purchases]
    else:
        recommendations = [p for p in products if p not in user.purchases]
    return random.choice(recommendations) if recommendations else random.choice(products)

def recommend_b(user):
    # Algorithm B: Recommend based on price range of previous purchases
    if user.purchases:
        avg_price = sum(p.price for p in user.purchases) / len(user.purchases)
        recommendations = [p for p in products if 0.8 * avg_price <= p.price <= 1.2 * avg_price and p not in user.purchases]
    else:
        recommendations = [p for p in products if p not in user.purchases]
    return random.choice(recommendations) if recommendations else random.choice(products)

# Simulation variables
day = 0
max_days = 30
purchases_a = 0
purchases_b = 0
revenue_a = 0
revenue_b = 0
satisfaction_a = 0
satisfaction_b = 0

# Helper function to draw rounded rectangle
def draw_rounded_rect(surface, rect, color, corner_radius):
    pygame.draw.rect(surface, color, rect, border_radius=corner_radius)

# Main game loop
running = True
clock = pygame.time.Clock()
show_explanation = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                show_explanation = not show_explanation

    # Clear the screen
    screen.fill(LIGHT_GRAY)

    # Draw header
    pygame.draw.rect(screen, HEADER_BG, (0, 0, WIDTH, 100))
    title_text = font_title.render("A/B Testing in Recommendation Systems Demo", True, WHITE)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 20))
    dev_text = font_subtitle.render("Developed by: Venugopal Adep", True, WHITE)
    screen.blit(dev_text, (WIDTH // 2 - dev_text.get_width() // 2, 70))

    # Simulate a day
    if day < max_days:
        day += 1
        for user in users:
            if random.random() < user.satisfaction:
                if user.group == 'A':
                    recommendation = recommend_a(user)
                else:
                    recommendation = recommend_b(user)
                
                if random.random() < 0.7:  # 70% chance of purchasing
                    user.purchases.append(recommendation)
                    if user.group == 'A':
                        purchases_a += 1
                        revenue_a += recommendation.price
                    else:
                        purchases_b += 1
                        revenue_b += recommendation.price
                    
                    user.satisfaction = min(1.0, user.satisfaction + 0.05)
                else:
                    user.satisfaction = max(0.1, user.satisfaction - 0.05)
                
                if user.group == 'A':
                    satisfaction_a += user.satisfaction
                else:
                    satisfaction_b += user.satisfaction

    # Draw users
    for user in users:
        user.draw()

    # Draw results
    draw_rounded_rect(screen, (50, 150, 700, 300), WHITE, 20)
    draw_rounded_rect(screen, (850, 150, 700, 300), WHITE, 20)

    results_a = [
        f"Group A (Red)",
        f"Algorithm: Popular Category",
        f"Total Purchases: {purchases_a}",
        f"Total Revenue: ${revenue_a:.2f}",
        f"Avg Satisfaction: {satisfaction_a / (len(users) // 2) / day:.2f}"
    ]

    results_b = [
        f"Group B (Blue)",
        f"Algorithm: Price Range",
        f"Total Purchases: {purchases_b}",
        f"Total Revenue: ${revenue_b:.2f}",
        f"Avg Satisfaction: {satisfaction_b / (len(users) // 2) / day:.2f}"
    ]

    for i, text in enumerate(results_a):
        text_surface = font_text.render(text, True, BLACK)
        screen.blit(text_surface, (70, 170 + i * 40))

    for i, text in enumerate(results_b):
        text_surface = font_text.render(text, True, BLACK)
        screen.blit(text_surface, (870, 170 + i * 40))

    # Draw day counter
    day_text = font_subtitle.render(f"Day: {day}/{max_days}", True, BLACK)
    screen.blit(day_text, (WIDTH // 2 - day_text.get_width() // 2, 110))

    # Draw explanation
    if show_explanation:
        draw_rounded_rect(screen, (50, HEIGHT - 200, WIDTH - 100, 180), WHITE, 20)
        explanation = [
            "This demo simulates A/B testing for two recommendation algorithms:",
            "Algorithm A (Red): Recommends based on the most popular category of previous purchases.",
            "Algorithm B (Blue): Recommends based on the price range of previous purchases.",
            "Users' satisfaction increases with successful recommendations and decreases with unsuccessful ones.",
            "Watch as the simulation runs to see which algorithm performs better over time.",
            "Press SPACE to toggle this explanation."
        ]

        for i, line in enumerate(explanation):
            text_surface = font_text.render(line, True, BLACK)
            screen.blit(text_surface, (70, HEIGHT - 180 + i * 25))
    else:
        toggle_text = font_text.render("Press SPACE to show explanation", True, BLACK)
        screen.blit(toggle_text, (WIDTH // 2 - toggle_text.get_width() // 2, HEIGHT - 30))

    # Update the display
    pygame.display.flip()

    # Control the simulation speed
    clock.tick(5)  # Adjust this value to change the speed of the simulation

# Quit Pygame
pygame.quit()