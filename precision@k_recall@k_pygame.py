import pygame
import pygame_gui
import random
import math

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 1800, 1000
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Precision@k, Recall@k, and F1-score@k Demo")

# Colors
BACKGROUND = (240, 240, 245)
TEXT = (50, 50, 50)
RELEVANT = (255, 107, 107)
NON_RELEVANT = (107, 161, 255)
RECOMMENDED = (107, 255, 161)
TOP_K = (255, 215, 0)

# Fonts
font = pygame.font.Font(None, 28)
large_font = pygame.font.Font(None, 48)
small_font = pygame.font.Font(None, 24)

# GUI manager
manager = pygame_gui.UIManager((WIDTH, HEIGHT))

# Sliders
k_slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect((WIDTH - 500, HEIGHT - 180), (300, 20)),
    start_value=5,
    value_range=(1, 20),
    manager=manager
)

items_slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect((WIDTH - 500, HEIGHT - 120), (300, 20)),
    start_value=20,
    value_range=(10, 50),
    manager=manager
)

# Labels for sliders
k_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((WIDTH - 500, HEIGHT - 210), (300, 30)),
    text="k (Top recommendations): 5",
    manager=manager
)

items_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((WIDTH - 500, HEIGHT - 150), (300, 30)),
    text="Number of Items: 20",
    manager=manager
)

# Regenerate button
regenerate_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((WIDTH - 300, HEIGHT - 60), (180, 40)),
    text="Regenerate Items",
    manager=manager
)

# Item class
class Item:
    def __init__(self, x, y, is_relevant, is_recommended, rank):
        self.x = x
        self.y = y
        self.is_relevant = is_relevant
        self.is_recommended = is_recommended
        self.rank = rank
        self.radius = 20

    def draw(self):
        color = RELEVANT if self.is_relevant else NON_RELEVANT
        pygame.draw.circle(screen, color, (self.x, self.y), self.radius)
        if self.is_recommended:
            pygame.draw.circle(screen, RECOMMENDED, (self.x, self.y), self.radius, 3)
        if self.rank is not None:
            rank_text = small_font.render(str(self.rank + 1), True, TEXT)
            screen.blit(rank_text, (self.x - rank_text.get_width() // 2, self.y - rank_text.get_height() // 2))

# Generate items
items = []

def generate_items():
    global items
    items = []
    num_items = int(items_slider.get_current_value())
    relevant_count = random.randint(num_items // 3, num_items // 2)
    recommended_count = random.randint(num_items // 3, num_items // 2)
    
    relevant_items = random.sample(range(num_items), relevant_count)
    recommended_items = random.sample(range(num_items), recommended_count)
    
    for i in range(num_items):
        x = 100 + (i % 10) * 80
        y = 150 + (i // 10) * 80
        is_relevant = i in relevant_items
        is_recommended = i in recommended_items
        rank = recommended_items.index(i) if is_recommended else None
        items.append(Item(x, y, is_relevant, is_recommended, rank))

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
                if event.ui_element == k_slider:
                    k_label.set_text(f"k (Top recommendations): {int(event.value)}")
                elif event.ui_element == items_slider:
                    items_label.set_text(f"Number of Items: {int(event.value)}")

        manager.process_events(event)

    manager.update(time_delta)

    screen.fill(BACKGROUND)

    # Draw items
    for item in items:
        item.draw()

    # Calculate metrics
    k = int(k_slider.get_current_value())
    relevant = sum(1 for item in items if item.is_relevant)
    recommended = sum(1 for item in items if item.is_recommended)
    top_k = sorted([item for item in items if item.is_recommended], key=lambda x: x.rank)[:k]
    
    true_positive_k = sum(1 for item in top_k if item.is_relevant)
    
    precision_at_k = true_positive_k / k if k > 0 else 0
    recall_at_k = true_positive_k / relevant if relevant > 0 else 0
    f1_score_at_k = 2 * (precision_at_k * recall_at_k) / (precision_at_k + recall_at_k) if (precision_at_k + recall_at_k) > 0 else 0

    # Draw top-k rectangle
    top_k_width = min(k * 80, 800)
    pygame.draw.rect(screen, TOP_K, (50, 100, top_k_width, HEIGHT - 200), 3)
    top_k_text = font.render(f"Top {k} Recommendations", True, TEXT)
    screen.blit(top_k_text, (50, 70))

    # Draw legend
    legend_x = WIDTH - 500
    pygame.draw.circle(screen, RELEVANT, (legend_x, 50), 10)
    screen.blit(font.render("Relevant Item", True, TEXT), (legend_x + 20, 40))
    pygame.draw.circle(screen, NON_RELEVANT, (legend_x, 80), 10)
    screen.blit(font.render("Non-Relevant Item", True, TEXT), (legend_x + 20, 70))
    pygame.draw.circle(screen, RECOMMENDED, (legend_x, 110), 10, 3)
    screen.blit(font.render("Recommended Item", True, TEXT), (legend_x + 20, 100))

    # Draw metrics
    metrics_text = [
        f"Precision@{k}: {precision_at_k:.2f}",
        f"Recall@{k}: {recall_at_k:.2f}",
        f"F1-score@{k}: {f1_score_at_k:.2f}",
        f"Relevant Items: {relevant}",
        f"Recommended Items: {recommended}",
        f"True Positives in top {k}: {true_positive_k}"
    ]
    
    for i, text in enumerate(metrics_text):
        screen.blit(font.render(text, True, TEXT), (legend_x, 150 + i * 30))

    # Draw explanations
    explanations = [
        f"Precision@k: Fraction of relevant items in top {k}",
        f"Recall@k: Fraction of relevant items found in top {k}",
        "F1-score@k: Harmonic mean of Precision@k and Recall@k"
    ]

    for i, text in enumerate(explanations):
        screen.blit(font.render(text, True, TEXT), (legend_x, 350 + i * 30))

    # Draw formulas
    formulas = [
        f"Precision@{k} = (Relevant items in top {k}) / {k}",
        f"Recall@{k} = (Relevant items in top {k}) / (Total relevant items)",
        f"F1@{k} = 2 * (Precision@{k} * Recall@{k}) / (Precision@{k} + Recall@{k})"
    ]

    for i, text in enumerate(formulas):
        screen.blit(small_font.render(text, True, TEXT), (legend_x, 470 + i * 25))

    # Draw title and developer info
    title = large_font.render("Precision@k, Recall@k, and F1-score@k Demo", True, TEXT)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 10))
    developer = small_font.render("Developed by: Venugopal Adep", True, TEXT)
    screen.blit(developer, (WIDTH // 2 - developer.get_width() // 2, 60))

    manager.draw_ui(screen)

    pygame.display.flip()

pygame.quit()