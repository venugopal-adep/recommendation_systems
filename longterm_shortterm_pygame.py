import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 1600, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("User Interest Recommendation System")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)
LIGHT_GRAY = (220, 220, 220)

# Fonts
title_font = pygame.font.Font(None, 56)
subtitle_font = pygame.font.Font(None, 36)
text_font = pygame.font.Font(None, 28)

# User interests
long_term_interests = ["Science", "Technology", "History", "Art"]
short_term_interests = []

# Recommendation items
items = ["Science Book", "Tech Gadget", "History Documentary", "Art Exhibition",
         "Sports Event", "Cooking Show", "Travel Guide", "Fashion Magazine"]

# Button class
class Button:
    def __init__(self, x, y, width, height, text, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False

    def draw(self):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        pygame.draw.rect(screen, BLACK, self.rect, 2, border_radius=10)
        text_surface = text_font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# Create buttons
short_term_button = Button(50, 200, 250, 60, "Add Short-term Interest", YELLOW, ORANGE)
recommend_button = Button(50, 300, 250, 60, "Get Recommendations", GREEN, CYAN)

# Main game loop
def main():
    clock = pygame.time.Clock()
    recommendations = []

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if short_term_button.is_clicked(event.pos):
                    if len(short_term_interests) < 3:
                        new_interest = random.choice([item for item in items if item not in short_term_interests])
                        short_term_interests.append(new_interest)
                elif recommend_button.is_clicked(event.pos):
                    recommendations = generate_recommendations()
            elif event.type == pygame.MOUSEMOTION:
                short_term_button.check_hover(event.pos)
                recommend_button.check_hover(event.pos)

        # Clear the screen
        screen.fill(LIGHT_GRAY)

        # Draw title and developer info
        draw_text("User Interest Recommendation System", 50, 50, BLACK, title_font)
        draw_text("Developed by: Venugopal Adep", 50, 100, PURPLE, subtitle_font)

        # Draw buttons
        short_term_button.draw()
        recommend_button.draw()

        # Display long-term interests
        draw_section("Long-term Interests", long_term_interests, 50, 400, BLUE)

        # Display short-term interests
        draw_section("Short-term Interests", short_term_interests, 50, 600, RED)

        # Display recommendations
        draw_section("Recommendations", recommendations, 800, 200, GREEN)

        # Draw explanation
        draw_text("How it works:", 800, 600, BLACK, subtitle_font)
        draw_text("- Long-term interests have 70% weight", 820, 650, BLACK, text_font)
        draw_text("- Short-term interests have 30% weight", 820, 690, BLACK, text_font)
        draw_text("- Recommendations are based on weighted random selection", 820, 730, BLACK, text_font)

        # Update the display
        pygame.display.flip()
        clock.tick(60)

def draw_text(text, x, y, color, font):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

def draw_section(title, items, x, y, color):
    pygame.draw.rect(screen, WHITE, (x-10, y-10, 700, 180), border_radius=10)
    pygame.draw.rect(screen, color, (x-10, y-10, 700, 180), 3, border_radius=10)
    draw_text(title, x, y, color, subtitle_font)
    for i, item in enumerate(items):
        draw_text(f"- {item}", x + 20, y + 40 + i * 35, BLACK, text_font)

def generate_recommendations():
    all_interests = long_term_interests + short_term_interests
    weights = [0.7] * len(long_term_interests) + [0.3] * len(short_term_interests)
    recommendations = random.choices(all_interests, weights=weights, k=5)
    return recommendations

if __name__ == "__main__":
    main()