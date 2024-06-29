import pygame
import sys
import random
import math

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 1600, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game Recommendation Engine")

# Colors
DARK_BG = (18, 18, 18)
LIGHT_BG = (240, 240, 240)
DARK_TEXT = (220, 220, 220)
LIGHT_TEXT = (18, 18, 18)
ACCENT = (0, 123, 255)
ACCENT_HOVER = (0, 86, 179)

# Fonts
title_font = pygame.font.Font(None, 48)
subtitle_font = pygame.font.Font(None, 32)
text_font = pygame.font.Font(None, 24)

# Game genres and their attributes
genres = {
    "Action": {"intensity": 0.8, "strategy": 0.3, "story": 0.4},
    "RPG": {"intensity": 0.5, "strategy": 0.7, "story": 0.9},
    "Strategy": {"intensity": 0.3, "strategy": 0.9, "story": 0.6},
    "Simulation": {"intensity": 0.2, "strategy": 0.8, "story": 0.5},
    "Adventure": {"intensity": 0.6, "strategy": 0.5, "story": 0.8},
}

# Player profile
player_profile = {
    "intensity": 0.5,
    "strategy": 0.5,
    "story": 0.5,
}

# Game history
game_history = []

# Recommendation
recommendation = ""

# Dark mode toggle
dark_mode = False

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

def draw_button(text, x, y, width, height, color, text_color, hover_color):
    mouse_pos = pygame.mouse.get_pos()
    button_rect = pygame.Rect(x, y, width, height)
    
    if button_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, hover_color, button_rect, border_radius=10)
    else:
        pygame.draw.rect(screen, color, button_rect, border_radius=10)
    
    draw_text(text, text_font, text_color, x + width // 2, y + height // 2, align="center")
    return button_rect

def update_player_profile():
    global player_profile
    for attribute in player_profile:
        total = sum(genres[game][attribute] for game in game_history)
        player_profile[attribute] = total / len(game_history) if game_history else 0.5

def get_recommendation():
    global recommendation
    scores = {}
    for genre, attributes in genres.items():
        score = sum(abs(attributes[attr] - player_profile[attr]) for attr in attributes)
        scores[genre] = score
    recommendation = min(scores, key=scores.get)

def draw_radar_chart(center_x, center_y, radius):
    attributes = list(player_profile.keys())
    num_attributes = len(attributes)
    angle_step = 2 * math.pi / num_attributes
    
    # Draw background
    pygame.draw.circle(screen, ACCENT, (center_x, center_y), radius, 1)
    for i in range(1, 5):
        pygame.draw.circle(screen, ACCENT, (center_x, center_y), radius * i / 4, 1)
    
    # Draw axes
    for i in range(num_attributes):
        angle = i * angle_step
        end_x = center_x + radius * math.cos(angle - math.pi / 2)
        end_y = center_y + radius * math.sin(angle - math.pi / 2)
        pygame.draw.line(screen, ACCENT, (center_x, center_y), (end_x, end_y), 1)
        draw_text(attributes[i], text_font, ACCENT, end_x, end_y, align="center")
    
    # Draw player profile
    points = []
    for i, attr in enumerate(attributes):
        angle = i * angle_step
        r = player_profile[attr] * radius
        x = center_x + r * math.cos(angle - math.pi / 2)
        y = center_y + r * math.sin(angle - math.pi / 2)
        points.append((x, y))
    
    pygame.draw.polygon(screen, ACCENT + (100,), points)
    for point in points:
        pygame.draw.circle(screen, ACCENT, point, 5)

def main():
    global game_history, recommendation, dark_mode

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for genre, rect in genre_buttons.items():
                        if rect.collidepoint(event.pos):
                            if len(game_history) >= 3:
                                game_history.pop(0)
                            game_history.append(genre)
                            update_player_profile()
                            get_recommendation()
                    if mode_toggle_rect.collidepoint(event.pos):
                        dark_mode = not dark_mode

        bg_color = DARK_BG if dark_mode else LIGHT_BG
        text_color = DARK_TEXT if dark_mode else LIGHT_TEXT
        screen.fill(bg_color)

        # Draw title and subtitle
        draw_text("Game Recommendation Engine", title_font, text_color, WIDTH // 2, 50, align="center")
        draw_text("Developed by: Venugopal Adep", subtitle_font, text_color, WIDTH // 2, 100, align="center")

        # Draw instructions
        draw_text("Select genres you've played:", text_font, text_color, 50, 150)

        # Draw genre buttons
        genre_buttons = {}
        for i, genre in enumerate(genres):
            button = draw_button(genre, 50 + (i % 3) * 220, 200 + (i // 3) * 70, 200, 50, ACCENT, DARK_TEXT, ACCENT_HOVER)
            genre_buttons[genre] = button

        # Draw player profile
        draw_text("Player Profile:", text_font, text_color, 50, 350)
        draw_radar_chart(250, 500, 150)

        # Draw game history
        draw_text("Game History:", text_font, text_color, 500, 350)
        for i, game in enumerate(game_history):
            draw_text(game, text_font, text_color, 500, 380 + i * 30)

        # Draw recommendation
        draw_text("Recommendation:", text_font, text_color, 500, 500)
        draw_text(recommendation, text_font, ACCENT, 500, 530)

        # Draw explanation
        draw_text("How it works:", text_font, text_color, 900, 200)
        draw_text("1. Click genre buttons to build your gaming history.", text_font, text_color, 900, 230)
        draw_text("2. Your player profile updates based on played genres.", text_font, text_color, 900, 260)
        draw_text("3. The system suggests a genre matching your profile.", text_font, text_color, 900, 290)
        draw_text("4. Experiment with different combinations!", text_font, text_color, 900, 320)

        # Draw mode toggle
        mode_toggle_rect = draw_button("Toggle Dark/Light Mode", WIDTH - 250, HEIGHT - 50, 200, 40, ACCENT, DARK_TEXT, ACCENT_HOVER)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()