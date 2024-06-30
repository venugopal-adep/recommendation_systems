import pygame
import math

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 1600, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Memory-Based Collaborative Filtering Demo")

# Colors
BACKGROUND = (230, 230, 250)  # Lavender
ACCENT = (106, 90, 205)  # Slate Blue
TEXT = (25, 25, 112)  # Midnight Blue
BUTTON_NORMAL = (135, 206, 250)  # Light Sky Blue
BUTTON_HOVER = (70, 130, 180)  # Steel Blue
BUTTON_ACTIVE = (255, 182, 193)  # Light Pink
HIGHLIGHT = (255, 99, 71)  # Tomato
BOX_BG = (240, 248, 255)  # Alice Blue
MATRIX_BG = (255, 228, 196)  # Bisque

# Fonts
title_font = pygame.font.Font(None, 48)
text_font = pygame.font.Font(None, 24)
small_font = pygame.font.Font(None, 24)

# Rating data
ratings = {
    "Alice": {"Action": 5, "Comedy": 3, "Drama": 4, "Sci-Fi": 2, "Mystery": 4},
    "Bob": {"Action": 4, "Comedy": 5, "Drama": 2, "Sci-Fi": 3, "Mystery": 4},
    "Charlie": {"Action": 3, "Comedy": 4, "Drama": 5, "Sci-Fi": 1, "Mystery": 3},
    "David": {"Action": 2, "Comedy": 3, "Drama": 3, "Sci-Fi": 5, "Mystery": 4},
    "Eve": {"Action": 5, "Comedy": 2, "Drama": 4, "Sci-Fi": 4, "Mystery": 3}
}

active_user = "Alice"
active_item = "Action"
method = "User-Based"

# Button class
class Button:
    def __init__(self, x, y, width, height, text, color, hover_color, active_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.active_color = active_color
        self.is_hovered = False
        self.is_active = False

    def draw(self):
        if self.is_active:
            color = self.active_color
        elif self.is_hovered:
            color = self.hover_color
        else:
            color = self.color
        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        pygame.draw.rect(screen, ACCENT, self.rect, 2, border_radius=10)
        text_surface = text_font.render(self.text, True, TEXT)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

    def update(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)

# Create buttons
user_buttons = [Button(50 + i * 160, 120, 140, 40, user, BUTTON_NORMAL, BUTTON_HOVER, BUTTON_ACTIVE) for i, user in enumerate(ratings)]
item_buttons = [Button(50 + i * 160, 180, 140, 40, item, BUTTON_NORMAL, BUTTON_HOVER, BUTTON_ACTIVE) for i, item in enumerate(ratings["Alice"])]
method_button = Button(50, 240, 200, 40, "Switch to Item-Based", BUTTON_NORMAL, BUTTON_HOVER, BUTTON_ACTIVE)

# Helper functions
def calculate_similarity(entity1, entity2, is_user_based):
    if is_user_based:
        common_items = set(ratings[entity1].keys()) & set(ratings[entity2].keys())
        if not common_items:
            return 0
        sum_xx, sum_yy, sum_xy = 0, 0, 0
        for item in common_items:
            x = ratings[entity1][item]
            y = ratings[entity2][item]
            sum_xx += x * x
            sum_yy += y * y
            sum_xy += x * y
    else:
        common_users = [user for user in ratings if entity1 in ratings[user] and entity2 in ratings[user]]
        if not common_users:
            return 0
        sum_xx, sum_yy, sum_xy = 0, 0, 0
        for user in common_users:
            x = ratings[user][entity1]
            y = ratings[user][entity2]
            sum_xx += x * x
            sum_yy += y * y
            sum_xy += x * y
    
    if sum_xx == 0 or sum_yy == 0:
        return 0
    
    return sum_xy / math.sqrt(sum_xx * sum_yy)

def get_recommendation():
    is_user_based = method == "User-Based"
    if is_user_based:
        similarities = {user: calculate_similarity(active_user, user, True) for user in ratings if user != active_user}
        weighted_ratings = {user: similarities[user] * ratings[user].get(active_item, 0) for user in similarities}
    else:
        similarities = {item: calculate_similarity(active_item, item, False) for item in ratings[active_user] if item != active_item}
        weighted_ratings = {item: similarities[item] * ratings[active_user][item] for item in similarities}
    
    total_similarity = sum(similarities.values())
    
    if total_similarity == 0:
        return 0, similarities, weighted_ratings, 0
    
    recommendation = sum(weighted_ratings.values()) / total_similarity
    return recommendation, similarities, weighted_ratings, total_similarity

# Main game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            for button in user_buttons:
                if button.is_clicked(pos):
                    active_user = button.text
            for button in item_buttons:
                if button.is_clicked(pos):
                    active_item = button.text
            if method_button.is_clicked(pos):
                method = "Item-Based" if method == "User-Based" else "User-Based"
                method_button.text = f"Switch to {'User-Based' if method == 'Item-Based' else 'Item-Based'}"

    # Clear the screen
    screen.fill(BACKGROUND)

    # Draw title and developer info
    title_surface = title_font.render("Memory-Based Collaborative Filtering Demo", True, ACCENT)
    screen.blit(title_surface, (WIDTH // 2 - title_surface.get_width() // 2, 20))

    dev_surface = text_font.render("Developed by: Venugopal Adep", True, TEXT)
    screen.blit(dev_surface, (WIDTH // 2 - dev_surface.get_width() // 2, 70))

    # Update and draw buttons
    mouse_pos = pygame.mouse.get_pos()
    for button in user_buttons + item_buttons + [method_button]:
        button.update(mouse_pos)
        button.draw()

    for button in user_buttons:
        button.is_active = button.text == active_user

    for button in item_buttons:
        button.is_active = button.text == active_item

    # Draw rating matrix
    matrix_box = pygame.Rect(50, 300, 700, 300)
    pygame.draw.rect(screen, MATRIX_BG, matrix_box, border_radius=10)
    pygame.draw.rect(screen, ACCENT, matrix_box, 2, border_radius=10)

    matrix_title = text_font.render("Rating Matrix", True, TEXT)
    screen.blit(matrix_title, (matrix_box.centerx - matrix_title.get_width() // 2, matrix_box.top + 10))

    for i, (user, items) in enumerate(ratings.items()):
        y_offset = 340 + i * 50
        user_text = text_font.render(f"{user}:", True, TEXT)
        screen.blit(user_text, (60, y_offset))
        
        for j, (item, rating) in enumerate(items.items()):
            rating_text = text_font.render(f"{item}: {rating}", True, TEXT)
            screen.blit(rating_text, (160 + j * 120, y_offset))

    # Calculate and display recommendation with explanation
    recommendation, similarities, weighted_ratings, total_similarity = get_recommendation()
    
    # Draw explanation box
    explanation_box = pygame.Rect(850, 120, 700, 730)
    pygame.draw.rect(screen, BOX_BG, explanation_box, border_radius=10)
    pygame.draw.rect(screen, ACCENT, explanation_box, 2, border_radius=10)

    y_offset = 140
    method_text = text_font.render(f"Current Method: {method}", True, TEXT)
    screen.blit(method_text, (870, y_offset))

    y_offset += 40
    if method == "User-Based":
        rec_text = text_font.render(f"Recommended rating for {active_user} - {active_item}: {recommendation:.2f}", True, HIGHLIGHT)
    else:
        rec_text = text_font.render(f"Recommended rating for {active_item} by {active_user}: {recommendation:.2f}", True, HIGHLIGHT)
    screen.blit(rec_text, (870, y_offset))
    
    y_offset += 40
    explanation_text = text_font.render("Calculation Steps:", True, TEXT)
    screen.blit(explanation_text, (870, y_offset))
    
    y_offset += 30
    for entity, similarity in similarities.items():
        if method == "User-Based":
            sim_text = small_font.render(f"Similarity({active_user}, {entity}) = {similarity:.2f}", True, TEXT)
        else:
            sim_text = small_font.render(f"Similarity({active_item}, {entity}) = {similarity:.2f}", True, TEXT)
        screen.blit(sim_text, (870, y_offset))
        y_offset += 25

    y_offset += 25
    for entity, weighted_rating in weighted_ratings.items():
        if method == "User-Based":
            weight_text = small_font.render(f"Weighted Rating({entity}) = {similarities[entity]:.2f} * {ratings[entity].get(active_item, 0)} = {weighted_rating:.2f}", True, TEXT)
        else:
            weight_text = small_font.render(f"Weighted Rating({entity}) = {similarities[entity]:.2f} * {ratings[active_user][entity]} = {weighted_rating:.2f}", True, TEXT)
        screen.blit(weight_text, (870, y_offset))
        y_offset += 25

    y_offset += 25
    total_sim_text = small_font.render(f"Total Similarity = {total_similarity:.2f}", True, TEXT)
    screen.blit(total_sim_text, (870, y_offset))
    
    y_offset += 35
    final_calc_text = small_font.render(f"Final Recommendation = Sum of Weighted Ratings / Total Similarity", True, TEXT)
    screen.blit(final_calc_text, (870, y_offset))
    y_offset += 25
    final_calc_text2 = small_font.render(f"= {sum(weighted_ratings.values()):.2f} / {total_similarity:.2f} = {recommendation:.2f}", True, TEXT)
    screen.blit(final_calc_text2, (890, y_offset))

    # Update the display
    pygame.display.flip()
    clock.tick(60)

# Quit Pygame
pygame.quit()
