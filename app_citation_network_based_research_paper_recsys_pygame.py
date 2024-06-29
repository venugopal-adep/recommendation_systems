import pygame
import sys
import random
import math

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 1600, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Research Paper Recommendation Demo")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
LIGHT_BLUE = (173, 216, 230)

# Fonts
title_font = pygame.font.Font(None, 48)
subtitle_font = pygame.font.Font(None, 32)
text_font = pygame.font.Font(None, 24)

# Research papers
papers = [
    {"id": 1, "title": "Machine Learning Basics", "x": 400, "y": 300, "color": BLUE, "citations": [2, 3], "interests": ["ML"]},
    {"id": 2, "title": "Deep Learning Advances", "x": 700, "y": 200, "color": GREEN, "citations": [3, 4], "interests": ["DL"]},
    {"id": 3, "title": "Natural Language Processing", "x": 700, "y": 400, "color": RED, "citations": [4], "interests": ["NLP"]},
    {"id": 4, "title": "Transformer Architecture", "x": 1000, "y": 300, "color": YELLOW, "citations": [], "interests": ["DL", "NLP"]},
]

# User profile
user_profile = {
    "interests": ["ML"],
    "reading_history": [],
}

# Buttons
buttons = [
    {"text": "Add ML Interest", "x": 50, "y": 600, "width": 200, "height": 50},
    {"text": "Add DL Interest", "x": 50, "y": 660, "width": 200, "height": 50},
    {"text": "Add NLP Interest", "x": 50, "y": 720, "width": 200, "height": 50},
    {"text": "Reset Demo", "x": 50, "y": 780, "width": 200, "height": 50},
]

def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

def draw_paper(paper, is_recommendation=False, is_read=False):
    color = GRAY if is_read else paper["color"]
    pygame.draw.circle(screen, color, (paper["x"], paper["y"]), 50)
    if is_recommendation:
        pygame.draw.circle(screen, WHITE, (paper["x"], paper["y"]), 55, 5)
    draw_text(f"Paper {paper['id']}", text_font, BLACK, paper["x"], paper["y"] - 15)
    draw_text(paper["title"], text_font, BLACK, paper["x"], paper["y"] + 15)

def draw_citations():
    for paper in papers:
        for cited_id in paper["citations"]:
            cited_paper = next(p for p in papers if p["id"] == cited_id)
            pygame.draw.line(screen, GRAY, (paper["x"], paper["y"]), (cited_paper["x"], cited_paper["y"]), 2)

def draw_button(button):
    color = PURPLE if button["text"] == "Reset Demo" else LIGHT_BLUE
    pygame.draw.rect(screen, color, (button["x"], button["y"], button["width"], button["height"]))
    draw_text(button["text"], text_font, BLACK, 
              button["x"] + button["width"] // 2, button["y"] + button["height"] // 2)

def get_recommendations():
    scores = {paper["id"]: 0 for paper in papers}
    
    for paper in papers:
        # Citation network score
        if paper["id"] in user_profile["reading_history"]:
            for cited_id in paper["citations"]:
                scores[cited_id] += 2
        
        # Interest match score
        for interest in paper["interests"]:
            if interest in user_profile["interests"]:
                scores[paper["id"]] += 1
    
    # Remove papers already in reading history
    for read_id in user_profile["reading_history"]:
        scores[read_id] = -1
    
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)[:2]

def reset_demo():
    global user_profile
    user_profile = {
        "interests": ["ML"],
        "reading_history": [],
    }

def draw_explanation():
    explanation_text = [
        "How it works:",
        "1. Papers are represented by colored circles.",
        "2. Lines between circles show citations.",
        "3. Your interests affect paper recommendations.",
        "4. Reading a paper (left-click) influences future recommendations.",
        "5. White outline shows recommended papers.",
        "6. Drag papers (right-click) to rearrange the network.",
        "7. Use buttons to add interests or reset the demo.",
    ]
    for i, line in enumerate(explanation_text):
        draw_text(line, text_font, BLACK, 1200, 600 + i * 30)

def main():
    global user_profile
    
    dragging = False
    selected_paper = None
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for paper in papers:
                    if math.hypot(event.pos[0] - paper["x"], event.pos[1] - paper["y"]) < 50:
                        if event.button == 1:  # Left click
                            if paper["id"] not in user_profile["reading_history"]:
                                user_profile["reading_history"].append(paper["id"])
                        elif event.button == 3:  # Right click
                            dragging = True
                            selected_paper = paper
                
                for button in buttons:
                    if button["x"] <= event.pos[0] <= button["x"] + button["width"] and \
                       button["y"] <= event.pos[1] <= button["y"] + button["height"]:
                        if button["text"] == "Reset Demo":
                            reset_demo()
                        else:
                            interest = button["text"].split()[-1]
                            if interest not in user_profile["interests"]:
                                user_profile["interests"].append(interest)
            
            elif event.type == pygame.MOUSEBUTTONUP:
                dragging = False
                selected_paper = None
            
            elif event.type == pygame.MOUSEMOTION:
                if dragging and selected_paper:
                    selected_paper["x"] = event.pos[0]
                    selected_paper["y"] = event.pos[1]

        # Draw background
        screen.fill(WHITE)

        # Draw title and subtitle
        draw_text("Research Paper Recommendation Demo", title_font, BLACK, WIDTH // 2, 50)
        draw_text("Based on Citation Network and User Interests", subtitle_font, BLACK, WIDTH // 2, 100)

        # Draw citation network
        draw_citations()

        # Draw papers
        recommendations = get_recommendations()
        for paper in papers:
            is_recommendation = paper["id"] in [r[0] for r in recommendations]
            is_read = paper["id"] in user_profile["reading_history"]
            draw_paper(paper, is_recommendation, is_read)

        # Draw buttons
        for button in buttons:
            draw_button(button)

        # Draw user profile
        draw_text("User Profile:", subtitle_font, BLACK, 1400, 200)
        draw_text(f"Interests: {', '.join(user_profile['interests'])}", text_font, BLACK, 1400, 240)
        draw_text(f"Reading History: {', '.join(map(str, user_profile['reading_history']))}", text_font, BLACK, 1400, 280)

        # Draw recommendations
        draw_text("Recommended Papers:", subtitle_font, BLACK, 1400, 340)
        for i, (paper_id, score) in enumerate(recommendations):
            paper = next(p for p in papers if p["id"] == paper_id)
            draw_text(f"{i+1}. {paper['title']} (Score: {score})", text_font, BLACK, 1400, 380 + i * 40)

        # Draw explanation
        draw_explanation()

        pygame.display.flip()

if __name__ == "__main__":
    main()