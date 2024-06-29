import pygame
import random
from datetime import datetime, timedelta

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 1400, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("YouTube Recommendation System")

# Colors
BACKGROUND = (245, 245, 245)
TEXT_COLOR = (50, 50, 50)
HIGHLIGHT = (255, 165, 0)  # Orange
BUTTON_COLOR = (70, 130, 180)  # Steel Blue
BUTTON_HOVER = (100, 160, 210)
HELP_COLOR = (60, 179, 113)  # Medium Sea Green
HELP_HOVER = (90, 209, 143)
VIDEO_COLORS = [
    (255, 200, 200),  # Light Red
    (200, 255, 200),  # Light Green
    (200, 200, 255),  # Light Blue
    (255, 255, 200),  # Light Yellow
    (255, 200, 255),  # Light Magenta
    (200, 255, 255),  # Light Cyan
]
EXPLANATION_BG = (230, 230, 230)

# Fonts
font_small = pygame.font.Font(None, 22)
font_medium = pygame.font.Font(None, 26)
font_large = pygame.font.Font(None, 32)
font_title = pygame.font.Font(None, 48)

class Video:
    def __init__(self, x, y, width, height, category):
        self.rect = pygame.Rect(x, y, width, height)
        self.views = random.randint(100000, 1000000)
        self.likes = int(self.views * random.uniform(0.01, 0.1))
        self.upload_date = datetime.now() - timedelta(days=random.randint(1, 365))
        self.category = category
        self.color = random.choice(VIDEO_COLORS)
        self.watched = False
        self.duration = random.randint(180, 1200)  # 3-20 minutes
        self.creator_popularity = random.uniform(0.1, 1.0)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        pygame.draw.rect(surface, TEXT_COLOR, self.rect, 2)
        if self.watched:
            pygame.draw.rect(surface, HIGHLIGHT, self.rect, 4)
        
        text_category = font_medium.render(self.category, True, TEXT_COLOR)
        text_views = font_small.render(f"{self.views:,} views", True, TEXT_COLOR)
        text_likes = font_small.render(f"{self.likes:,} likes", True, TEXT_COLOR)
        text_date = font_small.render(self.upload_date.strftime("%Y-%m-%d"), True, TEXT_COLOR)
        text_duration = font_small.render(f"{self.duration // 60}:{self.duration % 60:02d}", True, TEXT_COLOR)
        
        surface.blit(text_category, (self.rect.x + 5, self.rect.y + 5))
        surface.blit(text_views, (self.rect.x + 5, self.rect.y + 35))
        surface.blit(text_likes, (self.rect.x + 5, self.rect.y + 55))
        surface.blit(text_date, (self.rect.x + 5, self.rect.y + 75))
        surface.blit(text_duration, (self.rect.x + 5, self.rect.y + 95))

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
        text_surf = font_large.render(self.text, True, TEXT_COLOR)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# Create videos
videos = []
categories = ["Music", "Gaming", "Sports", "News", "Education", "Comedy", "Technology", "Cooking"]
for i in range(5):
    for j in range(3):
        videos.append(Video(i * 220 + 20, j * 200 + 160, 200, 180, random.choice(categories)))

viewed_videos = []

def calculate_scores(videos, viewed_videos):
    scores = {}
    for video in videos:
        if video not in viewed_videos:
            score = 0
            explanations = []

            engagement_score = sum(1 for v in viewed_videos if v.category == video.category) / max(len(viewed_videos), 1)
            engagement_weight = 0.25
            score += engagement_score * engagement_weight
            explanations.append(f"Engagement: {engagement_score:.2f} * {engagement_weight} = {engagement_score * engagement_weight:.2f}")

            popularity_score = (video.views / 1000000) * 0.4 + (video.likes / 100000) * 0.6
            popularity_weight = 0.25
            score += popularity_score * popularity_weight
            explanations.append(f"Popularity: {popularity_score:.2f} * {popularity_weight} = {popularity_score * popularity_weight:.2f}")

            days_old = (datetime.now() - video.upload_date).days
            freshness_score = max(0, 1 - (days_old / 365))
            freshness_weight = 0.15
            score += freshness_score * freshness_weight
            explanations.append(f"Freshness: {freshness_score:.2f} * {freshness_weight} = {freshness_score * freshness_weight:.2f}")

            watched_categories = set(v.category for v in viewed_videos)
            diversity_score = 1 if video.category not in watched_categories else 0
            diversity_weight = 0.15
            score += diversity_score * diversity_weight
            explanations.append(f"Diversity: {diversity_score:.2f} * {diversity_weight} = {diversity_score * diversity_weight:.2f}")

            creator_weight = 0.1
            score += video.creator_popularity * creator_weight
            explanations.append(f"Creator Popularity: {video.creator_popularity:.2f} * {creator_weight} = {video.creator_popularity * creator_weight:.2f}")

            duration_score = 1 - abs(600 - video.duration) / 600  # Prefer videos around 10 minutes
            duration_weight = 0.1
            score += duration_score * duration_weight
            explanations.append(f"Duration: {duration_score:.2f} * {duration_weight} = {duration_score * duration_weight:.2f}")

            scores[video] = (score, explanations)
    return scores

reset_button = Button(1200, 80, 180, 50, "Reset", BUTTON_COLOR, BUTTON_HOVER)
help_button = Button(1300, 20, 80, 40, "Help", HELP_COLOR, HELP_HOVER)

running = True
turn = 0
explanation_text = "Welcome to the YouTube Recommendation System! Click on a video to watch it and see how recommendations are calculated."
scores = {}
show_help = False

help_text = [
    "How YouTube Recommendations Work (Simplified):",
    "",
    "1. Engagement: If you watch lots of gaming videos, you'll see more gaming videos.",
    "   Example: 2 out of 4 watched videos are gaming. Score: 2/4 * 0.25 = 0.125",
    "",
    "2. Popularity: Videos with more views and likes are recommended more.",
    "   Example: 500,000 views and 50,000 likes. Score: (0.5 * 0.4) + (0.5 * 0.6) * 0.25 = 0.125",
    "",
    "3. Freshness: Newer videos get a boost.",
    "   Example: 3-month-old video. Score: (1 - 90/365) * 0.15 = 0.11",
    "",
    "4. Diversity: Sometimes recommends videos from categories you haven't watched.",
    "   Example: New category. Score: 1 * 0.15 = 0.15",
    "",
    "5. Creator Popularity: Videos from popular creators are recommended more.",
    "   Example: Creator popularity 0.8. Score: 0.8 * 0.1 = 0.08",
    "",
    "6. Duration: Prefers videos around 10 minutes long.",
    "   Example: 8-minute video. Score: (1 - |480 - 600|/600) * 0.1 = 0.08",
    "",
    "Total Score: Sum of all factors = 0.67",
    "",
    "The system recommends videos with the highest total scores."
]

while running:
    mouse_pos = pygame.mouse.get_pos()
    reset_button.check_hover(mouse_pos)
    help_button.check_hover(mouse_pos)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if help_button.is_clicked(mouse_pos):
                show_help = not show_help
            elif reset_button.is_clicked(mouse_pos):
                turn = 0
                viewed_videos = []
                explanation_text = "System reset. Click on a video to start again."
                scores = {}
                for video in videos:
                    video.watched = False
            elif turn < 5 and not show_help:
                for video in videos:
                    if video.rect.collidepoint(mouse_pos) and not video.watched:
                        video.watched = True
                        viewed_videos.append(video)
                        turn += 1
                        explanation_text = f"Turn {turn}: You watched a {video.category} video.\nRecommendation scores:"
                        scores = calculate_scores(videos, viewed_videos)
                        break

    screen.fill(BACKGROUND)

    # Draw title and developer info
    title_text = font_title.render("YouTube Recommendation System", True, TEXT_COLOR)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 20))
    dev_text = font_large.render("Developed by: Venugopal Adep", True, TEXT_COLOR)
    screen.blit(dev_text, (WIDTH // 2 - dev_text.get_width() // 2, 80))

    # Draw videos
    for video in videos:
        video.draw(screen)

    # Draw explanation panel
    explanation_panel = pygame.Rect(1100, 160, 280, 720)
    pygame.draw.rect(screen, EXPLANATION_BG, explanation_panel)
    pygame.draw.rect(screen, TEXT_COLOR, explanation_panel, 2)

    # Draw turn counter
    turn_text = font_large.render(f"Turn: {turn}/5", True, TEXT_COLOR)
    screen.blit(turn_text, (1120, 170))

    # Draw reset button
    reset_button.draw(screen)

    # Draw help button
    help_button.draw(screen)

    if show_help:
        help_panel = pygame.Rect(100, 100, WIDTH - 200, HEIGHT - 200)
        pygame.draw.rect(screen, EXPLANATION_BG, help_panel)
        pygame.draw.rect(screen, TEXT_COLOR, help_panel, 2)

        y_offset = 120
        for line in help_text:
            text_surface = font_medium.render(line, True, TEXT_COLOR)
            screen.blit(text_surface, (120, y_offset))
            y_offset += 30
    else:
        y_offset = 220
        for line in explanation_text.split('\n'):
            text_surface = font_medium.render(line, True, TEXT_COLOR)
            screen.blit(text_surface, (1120, y_offset))
            y_offset += 30

        if turn > 0:
            sorted_scores = sorted(scores.items(), key=lambda x: x[1][0], reverse=True)
            for i, (video, (score, explanation)) in enumerate(sorted_scores[:3]):
                pygame.draw.rect(screen, HIGHLIGHT, video.rect, 4)
                text_surface = font_medium.render(f"#{i+1}: Score {score:.2f}", True, TEXT_COLOR)
                screen.blit(text_surface, (1120, y_offset))
                y_offset += 30
                for line in explanation:
                    text_surface = font_small.render(line, True, TEXT_COLOR)
                    screen.blit(text_surface, (1130, y_offset))
                    y_offset += 25
                y_offset += 10

    pygame.display.flip()

pygame.quit()