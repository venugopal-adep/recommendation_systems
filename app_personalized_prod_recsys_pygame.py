import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 1600, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Personalized Financial Product Recommendation Demo")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Fonts
title_font = pygame.font.Font(None, 48)
subtitle_font = pygame.font.Font(None, 36)
text_font = pygame.font.Font(None, 24)

# Financial products
products = [
    {"name": "High-Yield Savings Account", "risk": "Low", "income": "Any", "goal": "Savings"},
    {"name": "Certificate of Deposit", "risk": "Low", "income": "Any", "goal": "Savings"},
    {"name": "Index Fund", "risk": "Medium", "income": "Medium", "goal": "Growth"},
    {"name": "Mutual Fund", "risk": "Medium", "income": "Medium", "goal": "Growth"},
    {"name": "Individual Stocks", "risk": "High", "income": "High", "goal": "Growth"},
    {"name": "Real Estate Investment Trust", "risk": "Medium", "income": "Medium", "goal": "Income"},
    {"name": "Corporate Bonds", "risk": "Medium", "income": "Medium", "goal": "Income"},
    {"name": "Government Bonds", "risk": "Low", "income": "Any", "goal": "Savings"},
    {"name": "Robo-Advisor", "risk": "Medium", "income": "Any", "goal": "Growth"},
    {"name": "Cryptocurrency", "risk": "High", "income": "High", "goal": "Growth"},
]

# User preferences
user_income = "Medium"
user_risk = "Medium"
user_goal = "Growth"

# Buttons
income_buttons = [
    {"text": "Low", "rect": pygame.Rect(50, 200, 100, 50)},
    {"text": "Medium", "rect": pygame.Rect(160, 200, 100, 50)},
    {"text": "High", "rect": pygame.Rect(270, 200, 100, 50)},
]

risk_buttons = [
    {"text": "Low", "rect": pygame.Rect(50, 300, 100, 50)},
    {"text": "Medium", "rect": pygame.Rect(160, 300, 100, 50)},
    {"text": "High", "rect": pygame.Rect(270, 300, 100, 50)},
]

goal_buttons = [
    {"text": "Savings", "rect": pygame.Rect(50, 400, 100, 50)},
    {"text": "Growth", "rect": pygame.Rect(160, 400, 100, 50)},
    {"text": "Income", "rect": pygame.Rect(270, 400, 100, 50)},
]

recommend_button = pygame.Rect(50, 500, 200, 50)

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

def draw_button(button, text):
    pygame.draw.rect(screen, GRAY, button["rect"])
    pygame.draw.rect(screen, BLACK, button["rect"], 2)
    draw_text(text, text_font, BLACK, button["rect"].centerx, button["rect"].centery, align="center")

def get_recommendations():
    recommendations = []
    for product in products:
        score = 0
        if product["income"] == user_income or product["income"] == "Any":
            score += 1
        if product["risk"] == user_risk:
            score += 1
        if product["goal"] == user_goal:
            score += 1
        if score > 0:
            recommendations.append((product["name"], score))
    
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
            for button in income_buttons:
                if button["rect"].collidepoint(pos):
                    user_income = button["text"]
            for button in risk_buttons:
                if button["rect"].collidepoint(pos):
                    user_risk = button["text"]
            for button in goal_buttons:
                if button["rect"].collidepoint(pos):
                    user_goal = button["text"]
            if recommend_button.collidepoint(pos):
                recommendations = get_recommendations()

    # Clear the screen
    screen.fill(WHITE)

    # Draw title and subtitle
    draw_text("Personalized Financial Product Recommendation Demo", title_font, BLACK, WIDTH // 2, 50, align="center")
    draw_text("Developed by: Venugopal Adep", subtitle_font, BLACK, WIDTH // 2, 100, align="center")

    # Draw buttons
    draw_text("Income Level:", text_font, BLACK, 50, 170)
    for button in income_buttons:
        draw_button(button, button["text"])
        if button["text"] == user_income:
            pygame.draw.rect(screen, GREEN, button["rect"], 3)

    draw_text("Risk Tolerance:", text_font, BLACK, 50, 270)
    for button in risk_buttons:
        draw_button(button, button["text"])
        if button["text"] == user_risk:
            pygame.draw.rect(screen, GREEN, button["rect"], 3)

    draw_text("Financial Goal:", text_font, BLACK, 50, 370)
    for button in goal_buttons:
        draw_button(button, button["text"])
        if button["text"] == user_goal:
            pygame.draw.rect(screen, GREEN, button["rect"], 3)

    pygame.draw.rect(screen, BLUE, recommend_button)
    draw_text("Get Recommendations", text_font, WHITE, recommend_button.centerx, recommend_button.centery, align="center")

    # Draw recommendations
    draw_text("Recommended Financial Products:", subtitle_font, BLACK, 500, 200)
    for i, rec in enumerate(recommendations):
        draw_text(f"{i+1}. {rec}", text_font, BLACK, 500, 250 + i * 30)

    # Draw explanation
    draw_text("How It Works:", subtitle_font, BLACK, 500, 400)
    draw_text("1. Income Level: Determines which products you can afford and access.", text_font, BLACK, 500, 450)
    draw_text("2. Risk Tolerance: Affects the balance between potential returns and stability.", text_font, BLACK, 500, 480)
    draw_text("3. Financial Goal: Guides the selection of products aligned with your objectives.", text_font, BLACK, 500, 510)
    draw_text("The recommendation system considers these factors to suggest suitable financial products.", text_font, BLACK, 500, 540)

    # Draw visual representation
    pygame.draw.rect(screen, GRAY, (1000, 200, 500, 500))
    
    # Income representation
    income_height = 150 if user_income == "Low" else 300 if user_income == "Medium" else 450
    pygame.draw.rect(screen, GREEN, (1050, 650 - income_height, 100, income_height))
    draw_text("Income", text_font, BLACK, 1100, 670, align="center")

    # Risk representation
    risk_height = 150 if user_risk == "Low" else 300 if user_risk == "Medium" else 450
    pygame.draw.rect(screen, RED, (1200, 650 - risk_height, 100, risk_height))
    draw_text("Risk", text_font, BLACK, 1250, 670, align="center")

    # Goal representation
    goal_color = BLUE if user_goal == "Savings" else YELLOW if user_goal == "Growth" else GREEN
    pygame.draw.circle(screen, goal_color, (1450, 400), 100)
    draw_text("Goal", text_font, BLACK, 1450, 520, align="center")

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()