import pygame
import pygame_gui
import random
import math

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 1800, 1000
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Interactive Recommendation System Demo")

# Colors
BACKGROUND = (240, 240, 245)
TEXT = (50, 50, 50)
RELEVANT = (255, 107, 107)
NON_RELEVANT = (107, 161, 255)
RECOMMENDED = (107, 255, 161)
BUTTON = (200, 200, 200)
BUTTON_HOVER = (180, 180, 180)

# Fonts
font = pygame.font.Font(None, 28)
large_font = pygame.font.Font(None, 48)
small_font = pygame.font.Font(None, 24)

# GUI manager
manager = pygame_gui.UIManager((WIDTH, HEIGHT))

# Slider for number of data points
slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect((WIDTH - 400, HEIGHT - 100), (300, 20)),
    start_value=50,
    value_range=(10, 200),
    manager=manager
)

# Label for slider
slider_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((WIDTH - 400, HEIGHT - 130), (300, 30)),
    text="Number of Data Points: 50",
    manager=manager
)

# Regenerate button
regenerate_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((WIDTH - 200, HEIGHT - 60), (180, 40)),
    text="Regenerate Items",
    manager=manager
)

# Item class
class Item:
    def __init__(self, x, y, actual_rating, predicted_rating):
        self.x = x
        self.y = y
        self.actual_rating = actual_rating
        self.predicted_rating = predicted_rating
        self.radius = 15

    def draw(self):
        color = RELEVANT if self.actual_rating >= 3.5 else NON_RELEVANT
        pygame.draw.circle(screen, color, (self.x, self.y), self.radius)
        if self.predicted_rating >= 3.5:
            pygame.draw.circle(screen, RECOMMENDED, (self.x, self.y), self.radius, 3)

# Generate items
items = []

def generate_items():
    global items
    items = []
    num_items = int(slider.get_current_value())
    for _ in range(num_items):
        x = random.randint(50, WIDTH - 450)
        y = random.randint(150, HEIGHT - 150)
        actual_rating = random.uniform(1, 5)
        predicted_rating = random.uniform(1, 5)
        items.append(Item(x, y, actual_rating, predicted_rating))

generate_items()

# Main game loop
running = True
clock = pygame.time.Clock()

while running:
    time_delta = clock.tick(60)/1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == regenerate_button:
                    generate_items()
            elif event.user_type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                if event.ui_element == slider:
                    slider_label.set_text(f"Number of Data Points: {int(event.value)}")

        manager.process_events(event)

    manager.update(time_delta)

    screen.fill(BACKGROUND)

    # Draw items
    for item in items:
        item.draw()

    # Calculate metrics
    relevant = sum(1 for item in items if item.actual_rating >= 3.5)
    recommended = sum(1 for item in items if item.predicted_rating >= 3.5)
    true_positive = sum(1 for item in items if item.actual_rating >= 3.5 and item.predicted_rating >= 3.5)
    false_negative = sum(1 for item in items if item.actual_rating >= 3.5 and item.predicted_rating < 3.5)
    false_positive = sum(1 for item in items if item.actual_rating < 3.5 and item.predicted_rating >= 3.5)

    recall = true_positive / relevant if relevant > 0 else 0
    precision = true_positive / recommended if recommended > 0 else 0

    # Draw legend
    legend_x = WIDTH - 400
    pygame.draw.circle(screen, RELEVANT, (legend_x, 50), 10)
    screen.blit(font.render("Relevant Item (Actual Rating ≥ 3.5)", True, TEXT), (legend_x + 20, 40))
    pygame.draw.circle(screen, NON_RELEVANT, (legend_x, 80), 10)
    screen.blit(font.render("Non-Relevant Item (Actual Rating < 3.5)", True, TEXT), (legend_x + 20, 70))
    pygame.draw.circle(screen, RECOMMENDED, (legend_x, 110), 10, 3)
    screen.blit(font.render("Recommended Item (Predicted Rating ≥ 3.5)", True, TEXT), (legend_x + 20, 100))

    # Draw metrics
    metrics_text = [
        f"Relevant Items: {relevant}",
        f"Recommended Items: {recommended}",
        f"True Positives: {true_positive}",
        f"False Negatives (FN): {false_negative}",
        f"False Positives (FP): {false_positive}",
        f"Recall: {recall:.2f}",
        f"Precision: {precision:.2f}"
    ]
    
    for i, text in enumerate(metrics_text):
        screen.blit(font.render(text, True, TEXT), (legend_x, 150 + i * 30))

    # Draw explanations
    explanations = [
        "FN: Relevant items not recommended",
        "FP: Non-relevant items recommended",
        "Recall = TP / (TP + FN)",
        "Precision = TP / (TP + FP)",
        "Where TP = True Positives"
    ]

    for i, text in enumerate(explanations):
        screen.blit(font.render(text, True, TEXT), (legend_x, 400 + i * 30))

    # Draw title and developer info
    title = large_font.render("Interactive Recommendation System Demo", True, TEXT)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 10))
    developer = small_font.render("Developed by: Venugopal Adep", True, TEXT)
    screen.blit(developer, (WIDTH // 2 - developer.get_width() // 2, 60))

    manager.draw_ui(screen)

    pygame.display.flip()

pygame.quit()