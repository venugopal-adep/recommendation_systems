import pygame
import sys
import random
import math

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pearson Correlation Visualizer")

# Colors
BACKGROUND = (240, 248, 255)  # AliceBlue
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 99, 71)  # Tomato
BLUE = (30, 144, 255)  # DodgerBlue
GRAY = (169, 169, 169)  # DarkGray
GREEN = (46, 139, 87)  # SeaGreen

# Fonts
TITLE_FONT = pygame.font.Font(None, 48)
SUBTITLE_FONT = pygame.font.Font(None, 36)
FONT = pygame.font.Font(None, 24)

# Scatter plot dimensions
PLOT_WIDTH, PLOT_HEIGHT = 600, 600
PLOT_X, PLOT_Y = (WIDTH - PLOT_WIDTH) // 2, (HEIGHT - PLOT_HEIGHT) // 2 + 50

# Data points and correlation
points = []
correlation = 0

def generate_correlated_data(num_points, correlation):
    data = []
    for _ in range(num_points):
        x = random.uniform(0, 1)
        y = correlation * x + math.sqrt(1 - correlation**2) * random.gauss(0, 1)
        data.append((x, y))
    return data

def calculate_correlation(points):
    if len(points) < 2:
        return 0
    
    n = len(points)
    sum_x = sum(p[0] for p in points)
    sum_y = sum(p[1] for p in points)
    sum_xy = sum(p[0] * p[1] for p in points)
    sum_x_sq = sum(p[0]**2 for p in points)
    sum_y_sq = sum(p[1]**2 for p in points)
    
    numerator = n * sum_xy - sum_x * sum_y
    denominator = math.sqrt((n * sum_x_sq - sum_x**2) * (n * sum_y_sq - sum_y**2))
    
    return numerator / denominator if denominator != 0 else 0

def draw_scatter_plot():
    pygame.draw.rect(screen, WHITE, (PLOT_X, PLOT_Y, PLOT_WIDTH, PLOT_HEIGHT))
    pygame.draw.rect(screen, BLACK, (PLOT_X, PLOT_Y, PLOT_WIDTH, PLOT_HEIGHT), 2)
    
    # Draw grid lines
    for i in range(1, 10):
        x = PLOT_X + i * PLOT_WIDTH // 10
        y = PLOT_Y + i * PLOT_HEIGHT // 10
        pygame.draw.line(screen, GRAY, (x, PLOT_Y), (x, PLOT_Y + PLOT_HEIGHT), 1)
        pygame.draw.line(screen, GRAY, (PLOT_X, y), (PLOT_X + PLOT_WIDTH, y), 1)
    
    for point in points:
        x = PLOT_X + int(point[0] * PLOT_WIDTH)
        y = PLOT_Y + PLOT_HEIGHT - int(point[1] * PLOT_HEIGHT)
        pygame.draw.circle(screen, BLUE, (x, y), 5)

def draw_correlation_line():
    if len(points) < 2:
        return
    
    x_values = [p[0] for p in points]
    y_values = [p[1] for p in points]
    
    mean_x = sum(x_values) / len(x_values)
    mean_y = sum(y_values) / len(y_values)
    
    numerator = sum((x - mean_x) * (y - mean_y) for x, y in zip(x_values, y_values))
    denominator_x = sum((x - mean_x)**2 for x in x_values)
    
    if denominator_x == 0:
        return
    
    slope = numerator / denominator_x
    intercept = mean_y - slope * mean_x
    
    start_x = 0
    start_y = intercept
    end_x = 1
    end_y = slope + intercept
    
    start_point = (PLOT_X + int(start_x * PLOT_WIDTH), PLOT_Y + PLOT_HEIGHT - int(start_y * PLOT_HEIGHT))
    end_point = (PLOT_X + int(end_x * PLOT_WIDTH), PLOT_Y + PLOT_HEIGHT - int(end_y * PLOT_HEIGHT))
    
    pygame.draw.line(screen, RED, start_point, end_point, 2)

def draw_ui():
    # Title
    title = TITLE_FONT.render("Pearson Correlation Visualizer", True, BLACK)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 10))
    
    # Subtitle
    subtitle = SUBTITLE_FONT.render("Developed by: Venugopal Adep", True, BLACK)
    screen.blit(subtitle, (WIDTH // 2 - subtitle.get_width() // 2, 60))
    
    # Instructions
    instructions = [
        "Left-click: Add data points",
        "Right-click: Remove data points",
        "Scroll wheel: Adjust correlation",
        "Space: Generate new data set",
        "R: Reset demo"
    ]
    
    for i, instruction in enumerate(instructions):
        text = FONT.render(instruction, True, BLACK)
        screen.blit(text, (20, HEIGHT - 150 + i * 30))
    
    # Correlation value
    corr_text = FONT.render(f"Correlation: {correlation:.2f}", True, BLACK)
    screen.blit(corr_text, (WIDTH - 200, HEIGHT - 150))
    
    # Draw correlation indicator
    indicator_width = 180
    indicator_height = 20
    indicator_x = WIDTH - 200
    indicator_y = HEIGHT - 120
    pygame.draw.rect(screen, BLACK, (indicator_x, indicator_y, indicator_width, indicator_height), 1)
    indicator_pos = int((correlation + 1) / 2 * indicator_width)
    pygame.draw.rect(screen, GREEN, (indicator_x + indicator_pos - 2, indicator_y, 4, indicator_height))
    
    # Correlation labels
    neg_label = FONT.render("-1", True, BLACK)
    zero_label = FONT.render("0", True, BLACK)
    pos_label = FONT.render("1", True, BLACK)
    screen.blit(neg_label, (indicator_x - 20, indicator_y + indicator_height))
    screen.blit(zero_label, (indicator_x + indicator_width // 2 - 5, indicator_y + indicator_height))
    screen.blit(pos_label, (indicator_x + indicator_width + 5, indicator_y + indicator_height))

def main():
    global points, correlation
    
    clock = pygame.time.Clock()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left-click
                    x, y = event.pos
                    if PLOT_X <= x <= PLOT_X + PLOT_WIDTH and PLOT_Y <= y <= PLOT_Y + PLOT_HEIGHT:
                        normalized_x = (x - PLOT_X) / PLOT_WIDTH
                        normalized_y = 1 - (y - PLOT_Y) / PLOT_HEIGHT
                        points.append((normalized_x, normalized_y))
                elif event.button == 3:  # Right-click
                    if points:
                        points.pop()
                elif event.button == 4:  # Scroll up
                    correlation = min(1, correlation + 0.1)
                elif event.button == 5:  # Scroll down
                    correlation = max(-1, correlation - 0.1)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    points = generate_correlated_data(50, correlation)
                elif event.key == pygame.K_r:
                    points = []
                    correlation = 0
        
        screen.fill(BACKGROUND)
        
        draw_scatter_plot()
        draw_correlation_line()
        draw_ui()
        
        correlation = calculate_correlation(points)
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()