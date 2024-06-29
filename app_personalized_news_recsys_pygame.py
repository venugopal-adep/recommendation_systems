import pygame
import random
from datetime import datetime, timedelta

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 1600, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Personalized News Feed Recommendation Demo")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# Fonts
title_font = pygame.font.Font(None, 48)
text_font = pygame.font.Font(None, 24)
small_font = pygame.font.Font(None, 20)

# News categories
categories = ["Politics", "Technology", "Sports", "Entertainment", "Science"]

# User class
class User:
    def __init__(self, name, interests):
        self.name = name
        self.interests = interests
        self.reading_history = []

# Article class
class Article:
    def __init__(self, title, category, date):
        self.title = title
        self.category = category
        self.date = date

# Create sample users
users = [
    User("Alice", ["Politics", "Technology"]),
    User("Bob", ["Sports", "Entertainment"]),
    User("Charlie", ["Science", "Technology"])
]

current_user = random.choice(users)

# Create sample articles
articles = [
    Article("New AI Breakthrough", "Technology", datetime.now() - timedelta(days=1)),
    Article("Election Results", "Politics", datetime.now()),
    Article("Latest Movie Release", "Entertainment", datetime.now() - timedelta(days=2)),
    Article("Sports Team Wins Championship", "Sports", datetime.now() - timedelta(days=1)),
    Article("Discovery on Mars", "Science", datetime.now()),
    Article("Tech Company Launches New Product", "Technology", datetime.now() - timedelta(days=3)),
    Article("Political Debate Highlights", "Politics", datetime.now() - timedelta(days=2)),
    Article("Celebrity Interview", "Entertainment", datetime.now() - timedelta(days=1)),
    Article("Sports Player Transfer", "Sports", datetime.now()),
    Article("Climate Change Study", "Science", datetime.now() - timedelta(days=2))
]

def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    screen.blit(text_surface, text_rect)

def draw_button(text, x, y, width, height, color):
    pygame.draw.rect(screen, color, (x, y, width, height))
    draw_text(text, text_font, BLACK, x + 10, y + 10)

def get_article_score(article, user):
    score = 0
    if article.category in user.interests:
        score += 3
    if article.category in [a.category for a in user.reading_history]:
        score += 2
    days_old = (datetime.now() - article.date).days
    score += max(0, 3 - days_old)  # More recent articles get higher scores
    return score

def get_recommendations(user, all_articles):
    scored_articles = [(article, get_article_score(article, user)) for article in all_articles]
    scored_articles.sort(key=lambda x: x[1], reverse=True)
    return scored_articles[:5]

def draw_news_feed(recommendations, x, y):
    for i, (article, score) in enumerate(recommendations):
        pygame.draw.rect(screen, GRAY, (x, y + i * 60, 400, 50))
        draw_text(article.title, text_font, BLACK, x + 10, y + i * 60 + 5)
        draw_text(f"Category: {article.category}", small_font, BLACK, x + 10, y + i * 60 + 25)
        draw_text(f"Date: {article.date.strftime('%Y-%m-%d')}", small_font, BLACK, x + 200, y + i * 60 + 25)
        draw_text(f"Score: {score}", small_font, RED, x + 350, y + i * 60 + 25)

def main():
    global current_user

    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill(WHITE)

        # Draw title and developer info
        draw_text("Personalized News Feed Recommendation Demo", title_font, BLACK, 20, 20)
        draw_text("Developed by: Venugopal Adep", text_font, BLACK, 20, 70)

        # Draw current user info
        draw_text(f"Current User: {current_user.name}", text_font, BLACK, 20, 120)
        draw_text(f"Interests: {', '.join(current_user.interests)}", text_font, BLACK, 20, 150)

        # Draw reading history
        draw_text("Reading History:", text_font, BLACK, 20, 200)
        for i, article in enumerate(current_user.reading_history[-5:]):
            draw_text(f"- {article.title} ({article.category})", small_font, BLACK, 20, 230 + i * 25)

        # Get and draw recommendations
        recommendations = get_recommendations(current_user, articles)
        draw_text("Recommended Articles:", text_font, BLACK, 500, 120)
        draw_news_feed(recommendations, 500, 150)

        # Draw action buttons
        draw_button("Read Random Article", 20, 400, 200, 40, BLUE)
        draw_button("Switch User", 20, 450, 200, 40, GREEN)

        # Draw explanation
        draw_text("How recommendations are scored:", text_font, BLACK, 20, 550)
        draw_text("- +3 points if the article category matches user interests", small_font, BLACK, 20, 580)
        draw_text("- +2 points if the article category is in the user's reading history", small_font, BLACK, 20, 605)
        draw_text("- +0 to 3 points based on article recency (newer articles score higher)", small_font, BLACK, 20, 630)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if 20 <= x <= 220:
                    if 400 <= y <= 440:  # Read Random Article
                        article = random.choice(articles)
                        current_user.reading_history.append(article)
                        if len(current_user.reading_history) > 10:
                            current_user.reading_history.pop(0)
                    elif 450 <= y <= 490:  # Switch User
                        current_user = random.choice(users)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()