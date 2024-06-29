import pygame
import random
import datetime

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 1600, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Time-Aware Recommendations System")

# Colors
BACKGROUND = (240, 248, 255)  # Alice Blue
TEXT_COLOR = (47, 79, 79)  # Dark Slate Gray
ACCENT_COLOR = (70, 130, 180)  # Steel Blue
HIGHLIGHT_COLOR = (255, 165, 0)  # Orange
BUTTON_COLOR = (60, 179, 113)  # Medium Sea Green
BUTTON_HOVER = (46, 139, 87)  # Sea Green

# Fonts
title_font = pygame.font.Font(None, 56)
subtitle_font = pygame.font.Font(None, 36)
text_font = pygame.font.Font(None, 28)

# User preferences
user_preferences = {
    "morning": ["News", "Coffee", "Exercise", "Breakfast", "Meditation"],
    "afternoon": ["Lunch", "Work", "Shopping", "Learning", "Social Media"],
    "evening": ["Dinner", "Movies", "Music", "Reading", "Gaming"]
}

# Recommendations
recommendations = []

# Time simulation
current_time = datetime.datetime.now().replace(hour=6, minute=0, second=0, microsecond=0)
time_speed = 1

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False

    def draw(self, surface):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        pygame.draw.rect(surface, TEXT_COLOR, self.rect, 2, border_radius=10)
        text_surf = text_font.render(self.text, True, TEXT_COLOR)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

speed_button = Button(WIDTH // 2 - 100, HEIGHT - 80, 200, 50, "Toggle Speed (1x)", BUTTON_COLOR, BUTTON_HOVER)

def get_time_of_day(time):
    hour = time.hour
    if 5 <= hour < 12:
        return "morning"
    elif 12 <= hour < 18:
        return "afternoon"
    else:
        return "evening"

def generate_recommendations(time_of_day):
    global recommendations
    recommendations = random.sample(user_preferences[time_of_day], 3)

def draw_clock(time):
    clock_center = (WIDTH // 4, HEIGHT // 2)
    clock_radius = 150
    pygame.draw.circle(screen, ACCENT_COLOR, clock_center, clock_radius, 4)
    
    for i in range(12):
        angle = i * 30
        start_pos = (clock_center[0] + int(clock_radius * 0.9 * pygame.math.Vector2(1, 0).rotate(-angle).x),
                     clock_center[1] + int(clock_radius * 0.9 * pygame.math.Vector2(1, 0).rotate(-angle).y))
        end_pos = (clock_center[0] + int(clock_radius * pygame.math.Vector2(1, 0).rotate(-angle).x),
                   clock_center[1] + int(clock_radius * pygame.math.Vector2(1, 0).rotate(-angle).y))
        pygame.draw.line(screen, ACCENT_COLOR, start_pos, end_pos, 2)
    
    # Draw hour hand
    hour_angle = (time.hour % 12 + time.minute / 60) * (360 / 12)
    hour_x = clock_center[0] + int(clock_radius * 0.5 * pygame.math.Vector2(1, 0).rotate(-hour_angle).x)
    hour_y = clock_center[1] + int(clock_radius * 0.5 * pygame.math.Vector2(1, 0).rotate(-hour_angle).y)
    pygame.draw.line(screen, TEXT_COLOR, clock_center, (hour_x, hour_y), 6)
    
    # Draw minute hand
    minute_angle = time.minute * (360 / 60)
    minute_x = clock_center[0] + int(clock_radius * 0.7 * pygame.math.Vector2(1, 0).rotate(-minute_angle).x)
    minute_y = clock_center[1] + int(clock_radius * 0.7 * pygame.math.Vector2(1, 0).rotate(-minute_angle).y)
    pygame.draw.line(screen, TEXT_COLOR, clock_center, (minute_x, minute_y), 4)

def draw_recommendations():
    for i, rec in enumerate(recommendations):
        pygame.draw.rect(screen, ACCENT_COLOR, (WIDTH // 2 - 150, 300 + i * 70, 300, 60), border_radius=10)
        text = text_font.render(rec, True, BACKGROUND)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 320 + i * 70))

def draw_explanation():
    explanation_text = [
        "This demo shows how recommendations change based on the time of day.",
        "Morning (5 AM - 11:59 AM): News, Coffee, Exercise, Breakfast, Meditation",
        "Afternoon (12 PM - 5:59 PM): Lunch, Work, Shopping, Learning, Social Media",
        "Evening (6 PM - 4:59 AM): Dinner, Movies, Music, Reading, Gaming",
        "Use the Toggle Speed button to see changes faster."
    ]
    explanation_box = pygame.Rect(WIDTH - 520, 100, 500, 200)
    pygame.draw.rect(screen, BACKGROUND, explanation_box, border_radius=10)
    pygame.draw.rect(screen, ACCENT_COLOR, explanation_box, 2, border_radius=10)
    
    for i, line in enumerate(explanation_text):
        text = text_font.render(line, True, TEXT_COLOR)
        screen.blit(text, (WIDTH - 500, 110 + i * 30))

def main():
    global current_time, time_speed

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        speed_button.check_hover(mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if speed_button.is_clicked(mouse_pos):
                    time_speed = 60 if time_speed == 1 else 1
                    speed_button.text = f"Toggle Speed ({time_speed}x)"

        # Update time
        current_time += datetime.timedelta(minutes=time_speed)
        if current_time.hour >= 24:
            current_time = current_time.replace(hour=0)

        # Generate recommendations based on time of day
        time_of_day = get_time_of_day(current_time)
        generate_recommendations(time_of_day)

        # Clear the screen
        screen.fill(BACKGROUND)

        # Draw title and subtitle
        title = title_font.render("Time-Aware Recommendations System", True, TEXT_COLOR)
        subtitle = subtitle_font.render("Developed by: Venugopal Adep", True, ACCENT_COLOR)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 20))
        screen.blit(subtitle, (WIDTH // 2 - subtitle.get_width() // 2, 70))

        # Draw clock
        draw_clock(current_time)

        # Draw current time
        time_text = subtitle_font.render(current_time.strftime("%I:%M %p"), True, TEXT_COLOR)
        screen.blit(time_text, (WIDTH // 4 - time_text.get_width() // 2, HEIGHT // 2 + 180))

        # Draw time of day
        tod_text = subtitle_font.render(f"Time of Day: {time_of_day.capitalize()}", True, HIGHLIGHT_COLOR)
        screen.blit(tod_text, (WIDTH // 2 - tod_text.get_width() // 2, 200))

        # Draw recommendations
        draw_recommendations()

        # Draw explanation
        draw_explanation()

        # Draw speed button
        speed_button.draw(screen)

        # Update the display
        pygame.display.flip()

        # Control the frame rate
        pygame.time.Clock().tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()