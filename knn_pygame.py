import pygame
import sys
import random
import math

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 1600, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Enhanced 2D KNN Algorithm Demo")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 50, 50)
BLUE = (50, 50, 255)
GREEN = (50, 255, 50)
YELLOW = (255, 255, 50)
PURPLE = (200, 0, 200)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)
LIGHT_GRAY = (220, 220, 220)
DARK_GRAY = (100, 100, 100)

# Fonts
TITLE_FONT = pygame.font.Font(None, 56)
SUBTITLE_FONT = pygame.font.Font(None, 36)
FONT = pygame.font.Font(None, 28)

# Plot dimensions
PLOT_WIDTH, PLOT_HEIGHT = 700, 700
PLOT_X, PLOT_Y = (WIDTH - PLOT_WIDTH) // 2, 100

# Data points
users = []
active_user = None
k = 3

# Movie genres
GENRES = ["Action", "Comedy", "Drama", "Sci-Fi"]

class User:
    def __init__(self, preferences):
        self.preferences = preferences
        self.color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))

def generate_random_user():
    preferences = [random.uniform(0, 5) for _ in range(len(GENRES))]
    return User(preferences)

def calculate_distance(user1, user2):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(user1.preferences, user2.preferences)))

def find_k_nearest_neighbors(active_user, k):
    distances = [(user, calculate_distance(active_user, user)) for user in users]
    return sorted(distances, key=lambda x: x[1])[:k]

def get_recommendations(neighbors):
    total_preferences = [sum(neighbor.preferences[i] for neighbor, _ in neighbors) for i in range(len(GENRES))]
    return [pref / len(neighbors) for pref in total_preferences]

def draw_2d_plot():
    pygame.draw.rect(screen, WHITE, (PLOT_X-10, PLOT_Y-10, PLOT_WIDTH+20, PLOT_HEIGHT+20))
    pygame.draw.rect(screen, BLACK, (PLOT_X, PLOT_Y, PLOT_WIDTH, PLOT_HEIGHT))
    
    # Draw grid
    for i in range(6):
        x = PLOT_X + i * PLOT_WIDTH // 5
        y = PLOT_Y + i * PLOT_HEIGHT // 5
        pygame.draw.line(screen, DARK_GRAY, (x, PLOT_Y), (x, PLOT_Y + PLOT_HEIGHT))
        pygame.draw.line(screen, DARK_GRAY, (PLOT_X, y), (PLOT_X + PLOT_WIDTH, y))
    
    # Label axes
    for i in range(6):
        value = i * 5 // 5
        x_text = FONT.render(str(value), True, BLACK)
        y_text = FONT.render(str(5 - value), True, BLACK)
        screen.blit(x_text, (PLOT_X + i * PLOT_WIDTH // 5 - 10, PLOT_Y + PLOT_HEIGHT + 10))
        screen.blit(y_text, (PLOT_X - 30, PLOT_Y + i * PLOT_HEIGHT // 5 - 10))
    
    screen.blit(FONT.render(GENRES[0], True, BLACK), (PLOT_X + PLOT_WIDTH + 10, PLOT_Y + PLOT_HEIGHT - 10))
    screen.blit(FONT.render(GENRES[1], True, BLACK), (PLOT_X - 60, PLOT_Y - 30))
    
    for user in users:
        x = PLOT_X + int(user.preferences[0] / 5 * PLOT_WIDTH)
        y = PLOT_Y + PLOT_HEIGHT - int(user.preferences[1] / 5 * PLOT_HEIGHT)
        pygame.draw.circle(screen, user.color, (x, y), 6)
    
    if active_user:
        x = PLOT_X + int(active_user.preferences[0] / 5 * PLOT_WIDTH)
        y = PLOT_Y + PLOT_HEIGHT - int(active_user.preferences[1] / 5 * PLOT_HEIGHT)
        pygame.draw.circle(screen, RED, (x, y), 10)
        
        neighbors = find_k_nearest_neighbors(active_user, k)
        for neighbor, distance in neighbors:
            nx = PLOT_X + int(neighbor.preferences[0] / 5 * PLOT_WIDTH)
            ny = PLOT_Y + PLOT_HEIGHT - int(neighbor.preferences[1] / 5 * PLOT_HEIGHT)
            pygame.draw.line(screen, YELLOW, (x, y), (nx, ny), 2)

def draw_preferences(user, x, y, width, height, title, color):
    pygame.draw.rect(screen, WHITE, (x-10, y-40, width+20, height+80))
    pygame.draw.rect(screen, color, (x-10, y-40, width+20, height+80), 3)
    
    title_text = SUBTITLE_FONT.render(title, True, color)
    screen.blit(title_text, (x + width // 2 - title_text.get_width() // 2, y - 35))
    
    bar_width = width // len(GENRES)
    for i, pref in enumerate(user.preferences):
        bar_height = (pref / 5) * height
        pygame.draw.rect(screen, color, (x + i * bar_width, y + height - bar_height, bar_width - 2, bar_height))
        
        genre_text = FONT.render(GENRES[i], True, BLACK)
        screen.blit(genre_text, (x + i * bar_width + 5, y + height + 5))
        
        pref_text = FONT.render(f"{pref:.2f}", True, BLACK)
        screen.blit(pref_text, (x + i * bar_width + 5, y + height - bar_height - 25))
        
        label_text = FONT.render(GENRES[i], True, WHITE)
        label_rect = label_text.get_rect(center=(x + i * bar_width + bar_width // 2, y + height - bar_height // 2))
        screen.blit(label_text, label_rect)

def draw_calculations(neighbors, recommendations):
    calc_x = 50
    calc_y = HEIGHT - 280
    pygame.draw.rect(screen, WHITE, (calc_x-10, calc_y-10, WIDTH - 80, 270))
    pygame.draw.rect(screen, PURPLE, (calc_x-10, calc_y-10, WIDTH - 80, 270), 3)
    
    title = SUBTITLE_FONT.render("Calculations", True, PURPLE)
    screen.blit(title, (calc_x + (WIDTH - 100) // 2 - title.get_width() // 2, calc_y))
    
    y_offset = 40
    for i, (neighbor, distance) in enumerate(neighbors):
        text = FONT.render(f"Neighbor {i+1}: " + ", ".join(f"{GENRES[j]}={neighbor.preferences[j]:.2f}" for j in range(len(GENRES))) + f", Distance={distance:.2f}", True, BLACK)
        screen.blit(text, (calc_x + 10, calc_y + y_offset))
        y_offset += 30
    
    y_offset += 10
    sum_prefs = [sum(neighbor.preferences[i] for neighbor, _ in neighbors) for i in range(len(GENRES))]
    sum_text = FONT.render("Sum of preferences: " + ", ".join(f"{GENRES[i]}={sum_prefs[i]:.2f}" for i in range(len(GENRES))), True, BLACK)
    screen.blit(sum_text, (calc_x + 10, calc_y + y_offset))
    y_offset += 30
    
    avg_text = FONT.render("Average (Recommendations): " + ", ".join(f"{GENRES[i]}={recommendations[i]:.2f}" for i in range(len(GENRES))), True, BLACK)
    screen.blit(avg_text, (calc_x + 10, calc_y + y_offset))

def draw_ui():
    screen.fill(LIGHT_GRAY)
    
    # Title
    title = TITLE_FONT.render("Enhanced 2D KNN Algorithm Demo", True, BLACK)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 10))
    
    # Subtitle
    subtitle = SUBTITLE_FONT.render("Developed by: Venugopal Adep", True, PURPLE)
    screen.blit(subtitle, (WIDTH // 2 - subtitle.get_width() // 2, 60))
    
    # Instructions
    instructions = [
        "Left-click: Set active user",
        "Right-click: Add new user",
        "Up/Down arrows: Adjust K value",
        "R: Reset demo"
    ]
    
    for i, instruction in enumerate(instructions):
        text = FONT.render(instruction, True, BLACK)
        screen.blit(text, (20, 120 + i * 30))
    
    # K value
    k_text = SUBTITLE_FONT.render(f"K = {k}", True, BLUE)
    screen.blit(k_text, (WIDTH - 100, 120))

def main():
    global users, active_user, k
    
    clock = pygame.time.Clock()
    
    # Generate initial users
    users = [generate_random_user() for _ in range(20)]
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if PLOT_X <= event.pos[0] <= PLOT_X + PLOT_WIDTH and PLOT_Y <= event.pos[1] <= PLOT_Y + PLOT_HEIGHT:
                    if event.button == 1:  # Left-click
                        x = (event.pos[0] - PLOT_X) / PLOT_WIDTH * 5
                        y = 5 - (event.pos[1] - PLOT_Y) / PLOT_HEIGHT * 5
                        active_user = User([x, y] + [random.uniform(0, 5) for _ in range(len(GENRES)-2)])
                    elif event.button == 3:  # Right-click
                        users.append(generate_random_user())
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    k = min(10, k + 1)
                elif event.key == pygame.K_DOWN:
                    k = max(1, k - 1)
                elif event.key == pygame.K_r:
                    users = [generate_random_user() for _ in range(20)]
                    active_user = None
                    k = 3
        
        draw_ui()
        draw_2d_plot()
        
        if active_user:
            draw_preferences(active_user, 50, HEIGHT - 480, 400, 200, "Active User Preferences", BLUE)
            
            neighbors = find_k_nearest_neighbors(active_user, k)
            recommendations = get_recommendations(neighbors)
            draw_preferences(User(recommendations), WIDTH - 450, HEIGHT - 480, 400, 200, "Recommendations", GREEN)
            draw_calculations(neighbors, recommendations)
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()