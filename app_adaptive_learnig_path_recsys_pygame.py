import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 1600, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Adaptive Learning Path Recommendation Demo")

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
text_font = pygame.font.Font(None, 32)
small_font = pygame.font.Font(None, 24)

# User data
user = {
    "progress": 0,
    "performance": 50,
    "goal": "Web Development"
}

# Courses
courses = [
    {"name": "HTML Basics", "difficulty": 1, "category": "Web Development"},
    {"name": "CSS Fundamentals", "difficulty": 2, "category": "Web Development"},
    {"name": "JavaScript Essentials", "difficulty": 3, "category": "Web Development"},
    {"name": "React Framework", "difficulty": 4, "category": "Web Development"},
    {"name": "Node.js Backend", "difficulty": 4, "category": "Web Development"},
    {"name": "Python Programming", "difficulty": 2, "category": "Programming"},
    {"name": "Data Structures", "difficulty": 3, "category": "Computer Science"},
    {"name": "Machine Learning Basics", "difficulty": 4, "category": "Data Science"}
]

recommended_courses = []

def update_recommendations():
    global recommended_courses
    recommended_courses = []
    for course in courses:
        if (course["category"] == user["goal"] and
            course["difficulty"] <= user["performance"] // 10 + 1):
            recommended_courses.append(course)
    
    recommended_courses = sorted(recommended_courses, key=lambda x: x["difficulty"])[:3]

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

def draw_progress_bar(x, y, width, height, progress, color):
    pygame.draw.rect(screen, GRAY, (x, y, width, height))
    pygame.draw.rect(screen, color, (x, y, int(width * progress / 100), height))

def draw_button(x, y, width, height, text):
    pygame.draw.rect(screen, GRAY, (x, y, width, height))
    pygame.draw.rect(screen, BLACK, (x, y, width, height), 2)
    draw_text(text, small_font, BLACK, x + width // 2, y + height // 2, "center")

def main():
    clock = pygame.time.Clock()
    update_recommendations()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if 100 <= x <= 300 and 300 <= y <= 330:
                    user["progress"] = max(0, user["progress"] - 10)
                elif 350 <= x <= 550 and 300 <= y <= 330:
                    user["progress"] = min(100, user["progress"] + 10)
                elif 100 <= x <= 300 and 400 <= y <= 430:
                    user["performance"] = max(0, user["performance"] - 10)
                elif 350 <= x <= 550 and 400 <= y <= 430:
                    user["performance"] = min(100, user["performance"] + 10)
                elif 100 <= x <= 300 and 500 <= y <= 530:
                    user["goal"] = "Web Development"
                elif 350 <= x <= 550 and 500 <= y <= 530:
                    user["goal"] = "Data Science"
                update_recommendations()

        screen.fill(WHITE)

        # Draw title and developer name
        draw_text("Adaptive Learning Path Recommendation Demo", title_font, BLACK, WIDTH // 2, 50, "center")
        draw_text("Developed by: Venugopal Adep", small_font, BLACK, WIDTH // 2, 90, "center")

        # Draw user information
        draw_text("User Profile", text_font, BLACK, 100, 150)
        draw_text(f"Progress: {user['progress']}%", text_font, BLACK, 100, 200)
        draw_progress_bar(100, 240, 450, 30, user["progress"], BLUE)
        draw_button(100, 300, 200, 30, "Decrease Progress")
        draw_button(350, 300, 200, 30, "Increase Progress")

        draw_text(f"Performance: {user['performance']}%", text_font, BLACK, 100, 350)
        draw_progress_bar(100, 390, 450, 30, user["performance"], GREEN)
        draw_button(100, 400, 200, 30, "Decrease Performance")
        draw_button(350, 400, 200, 30, "Increase Performance")

        draw_text(f"Learning Goal: {user['goal']}", text_font, BLACK, 100, 450)
        draw_button(100, 500, 200, 30, "Web Development")
        draw_button(350, 500, 200, 30, "Data Science")

        # Draw recommended courses
        draw_text("Recommended Courses", text_font, BLACK, 800, 150)
        for i, course in enumerate(recommended_courses):
            y = 200 + i * 100
            pygame.draw.rect(screen, YELLOW, (800, y, 700, 80))
            draw_text(course["name"], text_font, BLACK, 820, y + 10)
            draw_text(f"Difficulty: {course['difficulty']}", small_font, BLACK, 820, y + 50)
            draw_text(f"Category: {course['category']}", small_font, BLACK, 1200, y + 50)

        # Draw explanation
        draw_text("How it works:", text_font, BLACK, 100, 600)
        draw_text("1. User progress affects the number of courses recommended", small_font, BLACK, 100, 640)
        draw_text("2. User performance influences the difficulty of recommended courses", small_font, BLACK, 100, 670)
        draw_text("3. Learning goal determines the category of recommended courses", small_font, BLACK, 100, 700)
        draw_text("Interact with the user profile to see how recommendations change!", small_font, RED, 100, 730)

        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()