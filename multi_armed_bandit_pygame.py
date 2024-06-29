import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 1600, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Multi-Armed Bandits Recommendation System")

# Colors
BACKGROUND = (15, 23, 42)  # Dark blue
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 99, 71)  # Tomato
GREEN = (46, 204, 113)  # Emerald
BLUE = (52, 152, 219)  # Dodger Blue
YELLOW = (241, 196, 15)  # Sun Flower
PURPLE = (155, 89, 182)  # Amethyst
GRAY = (149, 165, 166)  # Asbestos

# Fonts
title_font = pygame.font.Font(None, 48)
subtitle_font = pygame.font.Font(None, 36)
text_font = pygame.font.Font(None, 24)

# Bandits (recommendation options)
class Bandit:
    def __init__(self, name, true_mean, color):
        self.name = name
        self.true_mean = true_mean
        self.estimated_mean = 0
        self.pulls = 0
        self.color = color

    def pull(self):
        return random.gauss(self.true_mean, 0.1)

bandits = [
    Bandit("Product A", 0.3, RED),
    Bandit("Product B", 0.5, GREEN),
    Bandit("Product C", 0.7, BLUE),
    Bandit("Product D", 0.4, YELLOW),
    Bandit("Product E", 0.6, PURPLE)
]

# Game variables
total_reward = 0
rounds = 0
epsilon = 0.1
auto_play = False
auto_play_speed = 1  # rounds per second
show_help = False

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

def draw_bandits():
    for i, bandit in enumerate(bandits):
        x = 150 + i * 270
        y = 650
        pygame.draw.rect(screen, bandit.color, (x-100, y-150, 200, 250), border_radius=20)
        pygame.draw.rect(screen, WHITE, (x-100, y-150, 200, 250), border_radius=20, width=2)
        draw_text(bandit.name, subtitle_font, WHITE, x, y-120, align="center")
        draw_text(f"Est. Mean: {bandit.estimated_mean:.3f}", text_font, WHITE, x, y-80, align="center")
        draw_text(f"Pulls: {bandit.pulls}", text_font, WHITE, x, y-50, align="center")
        pygame.draw.rect(screen, WHITE, (x-80, y+50, 160, 40), border_radius=20)
        draw_text("RECOMMEND", text_font, BLACK, x, y+70, align="center")

def select_bandit():
    if random.random() < epsilon:
        return random.choice(bandits)
    else:
        return max(bandits, key=lambda b: b.estimated_mean)

def update_bandit(bandit, reward):
    bandit.pulls += 1
    bandit.estimated_mean += (reward - bandit.estimated_mean) / bandit.pulls

def draw_graph():
    graph_rect = pygame.Rect(50, 150, 700, 300)
    pygame.draw.rect(screen, WHITE, graph_rect, border_radius=10)
    pygame.draw.rect(screen, GRAY, graph_rect, border_radius=10, width=2)
    
    max_pulls = max(bandit.pulls for bandit in bandits) if any(bandit.pulls for bandit in bandits) else 1
    for i, bandit in enumerate(bandits):
        x = graph_rect.left + 70 + i * 140
        y = graph_rect.bottom - 50
        height = (bandit.pulls / max_pulls) * 200 if max_pulls > 0 else 0
        pygame.draw.rect(screen, bandit.color, (x-30, y-height, 60, height))
        draw_text(bandit.name, text_font, BLACK, x, y+20, align="center")
    
    draw_text("Product Recommendations", subtitle_font, BLACK, graph_rect.centerx, graph_rect.top + 30, align="center")

def draw_help_button():
    help_button_rect = pygame.Rect(WIDTH - 100, 20, 80, 40)
    pygame.draw.rect(screen, BLUE, help_button_rect, border_radius=10)
    draw_text("HELP", text_font, WHITE, WIDTH - 60, 40, align="center")
    return help_button_rect

def draw_help_screen():
    help_rect = pygame.Rect(50, 50, WIDTH - 100, HEIGHT - 100)
    pygame.draw.rect(screen, WHITE, help_rect, border_radius=10)
    pygame.draw.rect(screen, GRAY, help_rect, border_radius=10, width=2)

    explanation = [
        "Multi-Armed Bandits Recommendation System Explained:",
        "",
        "Imagine you're at a casino with 5 slot machines (our 'Products A-E'). Each machine has a hidden",
        "average payout (true mean), but you don't know what it is. Your goal is to maximize your total winnings.",
        "",
        "How it works:",
        "1. Exploration: Sometimes (based on 'epsilon'), you try a random machine to learn about its payout.",
        "2. Exploitation: Other times, you pick the machine that has given you the best results so far.",
        "3. Learning: Each time you play, you update your estimate of how good each machine is.",
        "",
        "Example:",
        "- You start by trying each machine a few times.",
        "- Machine C seems to pay out more often, so you play it more.",
        "- But you occasionally try the others, in case they're actually better.",
        "- Over time, you get a good idea of which machine is best and play it most often.",
        "",
        "In our demo:",
        "- Products are like slot machines.",
        "- 'Pulls' show how often a product has been recommended.",
        "- 'Est. Mean' is our current belief about how good each product is.",
        "- The graph shows which products we've recommended most often.",
        "",
        "The goal is to find the best product(s) to recommend while still exploring new options!",
        "",
        "Click anywhere to close this help screen."
    ]

    for i, line in enumerate(explanation):
        draw_text(line, text_font, BLACK, help_rect.left + 20, help_rect.top + 20 + i * 30)

# Main game loop
clock = pygame.time.Clock()
running = True
last_auto_play_time = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if show_help:
                show_help = False
            else:
                x, y = pygame.mouse.get_pos()
                help_button_rect = draw_help_button()
                if help_button_rect.collidepoint(x, y):
                    show_help = True
                else:
                    for i, bandit in enumerate(bandits):
                        bandit_x = 150 + i * 270
                        bandit_y = 650
                        if bandit_x-80 <= x <= bandit_x+80 and bandit_y+50 <= y <= bandit_y+90:
                            reward = bandit.pull()
                            update_bandit(bandit, reward)
                            total_reward += reward
                            rounds += 1
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                auto_play = not auto_play
            elif event.key == pygame.K_UP:
                auto_play_speed = min(10, auto_play_speed + 1)
            elif event.key == pygame.K_DOWN:
                auto_play_speed = max(1, auto_play_speed - 1)

    # Auto-play
    if auto_play and not show_help:
        current_time = pygame.time.get_ticks()
        if current_time - last_auto_play_time > 1000 / auto_play_speed:
            bandit = select_bandit()
            reward = bandit.pull()
            update_bandit(bandit, reward)
            total_reward += reward
            rounds += 1
            last_auto_play_time = current_time

    # Draw everything
    screen.fill(BACKGROUND)
    
    if show_help:
        draw_help_screen()
    else:
        # Title and author
        draw_text("Multi-Armed Bandits Recommendation System", title_font, WHITE, WIDTH//2, 50, align="center")
        draw_text("Developed by: Venugopal Adep", subtitle_font, GRAY, WIDTH//2, 100, align="center")

        # Instructions and Stats
        info_rect = pygame.Rect(800, 150, 750, 300)
        pygame.draw.rect(screen, WHITE, info_rect, border_radius=10)
        pygame.draw.rect(screen, GRAY, info_rect, border_radius=10, width=2)

        instructions = [
            "Instructions:",
            "- Click on a product to recommend it.",
            "- Space: Toggle auto-play",
            "- Up/Down arrows: Change auto-play speed"
        ]
        for i, instruction in enumerate(instructions):
            draw_text(instruction, text_font, BLACK, info_rect.left + 20, info_rect.top + 20 + i * 30)

        stats = [
            f"Total Reward: {total_reward:.2f}",
            f"Rounds: {rounds}",
            f"Epsilon: {epsilon:.2f}",
            f"Auto-play: {'ON' if auto_play else 'OFF'}",
            f"Auto-play Speed: {auto_play_speed}"
        ]
        for i, stat in enumerate(stats):
            draw_text(stat, text_font, BLACK, info_rect.left + 20, info_rect.top + 180 + i * 30)

        # Draw graph
        draw_graph()

        # Draw bandits
        draw_bandits()

        # Draw help button
        draw_help_button()

    # Update display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()