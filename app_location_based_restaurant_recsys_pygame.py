import pygame
import sys
import random
import math

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 1600, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Restaurant Finder")

# Colors
PRIMARY = (41, 128, 185)  # Blue
SECONDARY = (39, 174, 96)  # Green
ACCENT = (231, 76, 60)  # Red
BG_COLOR = (236, 240, 241)  # Light Gray
TEXT_COLOR = (52, 73, 94)  # Dark Gray
LIGHT_TEXT = (236, 240, 241)  # Light Gray

# Fonts
pygame.font.init()
FONT_FAMILY = "Arial"
title_font = pygame.font.SysFont(FONT_FAMILY, 48, bold=True)
subtitle_font = pygame.font.SysFont(FONT_FAMILY, 36)
text_font = pygame.font.SysFont(FONT_FAMILY, 24)

# Restaurants
restaurants = [
    {"name": "Pizzeria Uno", "cuisine": "Italian", "x": 900, "y": 300},
    {"name": "Sushi Palace", "cuisine": "Japanese", "x": 1100, "y": 400},
    {"name": "Burger Joint", "cuisine": "American", "x": 1300, "y": 200},
    {"name": "Taco Town", "cuisine": "Mexican", "x": 1000, "y": 600},
    {"name": "Curry House", "cuisine": "Indian", "x": 1200, "y": 500},
    {"name": "Noodle Bar", "cuisine": "Chinese", "x": 800, "y": 500},
    {"name": "Steakhouse", "cuisine": "American", "x": 1400, "y": 300},
    {"name": "Falafel Hut", "cuisine": "Middle Eastern", "x": 900, "y": 700},
]

# User preferences
user_x, user_y = 1000, 400
user_cuisine = "Italian"
dining_history = []

# Buttons
cuisine_buttons = [
    {"text": "Italian", "rect": pygame.Rect(50, 200, 150, 50)},
    {"text": "Japanese", "rect": pygame.Rect(210, 200, 150, 50)},
    {"text": "American", "rect": pygame.Rect(370, 200, 150, 50)},
    {"text": "Mexican", "rect": pygame.Rect(50, 260, 150, 50)},
    {"text": "Indian", "rect": pygame.Rect(210, 260, 150, 50)},
    {"text": "Chinese", "rect": pygame.Rect(370, 260, 150, 50)},
]

recommend_button = pygame.Rect(50, 350, 200, 50)

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

def draw_button(button, text, color=SECONDARY, text_color=LIGHT_TEXT):
    pygame.draw.rect(screen, color, button["rect"], border_radius=5)
    pygame.draw.rect(screen, TEXT_COLOR, button["rect"], 2, border_radius=5)
    draw_text(text, text_font, text_color, button["rect"].centerx, button["rect"].centery, align="center")

def draw_panel(rect, color=LIGHT_TEXT, border_color=TEXT_COLOR):
    pygame.draw.rect(screen, color, rect, border_radius=10)
    pygame.draw.rect(screen, border_color, rect, 2, border_radius=10)

def distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def get_recommendations():
    global dining_history
    recommendations = []
    for restaurant in restaurants:
        score = 0
        dist = distance(user_x, user_y, restaurant["x"], restaurant["y"])
        score += 1000 / (dist + 1)  # Distance score
        if restaurant["cuisine"] == user_cuisine:
            score += 500  # Cuisine preference score
        if restaurant["name"] not in dining_history:
            score += 250  # New restaurant bonus
        recommendations.append((restaurant, score))
    
    recommendations.sort(key=lambda x: x[1], reverse=True)
    return [r[0] for r in recommendations[:3]]

# Main game loop
running = True
recommendations = []

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            for button in cuisine_buttons:
                if button["rect"].collidepoint(pos):
                    user_cuisine = button["text"]
            if recommend_button.collidepoint(pos):
                recommendations = get_recommendations()
                if recommendations:
                    dining_history.append(recommendations[0]["name"])
                    if len(dining_history) > 3:
                        dining_history.pop(0)
            elif 600 < pos[0] < 1500 and 150 < pos[1] < 750:  # Map area
                user_x, user_y = pos

    # Clear the screen
    screen.fill(BG_COLOR)

    # Draw title and subtitle
    draw_text("Restaurant Finder", title_font, PRIMARY, WIDTH // 2, 50, align="center")
    draw_text("Find your next favorite spot", subtitle_font, TEXT_COLOR, WIDTH // 2, 100, align="center")

    # Draw buttons
    draw_text("Cuisine Preference:", text_font, TEXT_COLOR, 50, 170)
    for button in cuisine_buttons:
        draw_button(button, button["text"], SECONDARY if button["text"] == user_cuisine else PRIMARY)

    draw_button({"rect": recommend_button}, "Get Recommendations", ACCENT)

    # Draw map
    map_rect = pygame.Rect(600, 150, 900, 600)
    draw_panel(map_rect)
    for restaurant in restaurants:
        pygame.draw.circle(screen, ACCENT, (restaurant["x"], restaurant["y"]), 10)
        draw_text(restaurant["name"], text_font, TEXT_COLOR, restaurant["x"] + 15, restaurant["y"] - 15)

    # Draw user location
    pygame.draw.circle(screen, PRIMARY, (user_x, user_y), 15)
    draw_text("You", text_font, PRIMARY, user_x + 20, user_y - 20)

    # Draw recommendations
    rec_panel = pygame.Rect(50, 450, 500, 200)
    draw_panel(rec_panel)
    draw_text("Recommendations:", subtitle_font, TEXT_COLOR, 70, 470)
    for i, rec in enumerate(recommendations):
        draw_text(f"{i+1}. {rec['name']} ({rec['cuisine']})", text_font, TEXT_COLOR, 70, 520 + i * 30)

    # Draw dining history
    history_panel = pygame.Rect(50, 670, 500, 110)
    draw_panel(history_panel)
    draw_text("Dining History:", subtitle_font, TEXT_COLOR, 70, 690)
    for i, restaurant in enumerate(dining_history):
        draw_text(f"{i+1}. {restaurant}", text_font, TEXT_COLOR, 70, 730 + i * 30)

    # Draw explanation
    explain_panel = pygame.Rect(1150, 20, 430, 110)
    draw_panel(explain_panel)
    draw_text("How to use:", text_font, TEXT_COLOR, 1170, 30)
    draw_text("1. Select your preferred cuisine", text_font, TEXT_COLOR, 1170, 60)
    draw_text("2. Click on the map to set your location", text_font, TEXT_COLOR, 1170, 85)
    draw_text("3. Click 'Get Recommendations'", text_font, TEXT_COLOR, 1170, 110)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()