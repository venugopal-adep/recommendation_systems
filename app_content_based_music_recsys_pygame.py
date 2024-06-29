import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 1600, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Content-Based Music Rec System")

# Colors
BACKGROUND = (240, 248, 255)  # AliceBlue
TEXT_COLOR = (47, 79, 79)     # DarkSlateGray
ACCENT_1 = (70, 130, 180)     # SteelBlue
ACCENT_2 = (255, 182, 193)    # LightPink
ACCENT_3 = (144, 238, 144)    # LightGreen
BUTTON_COLOR = (65, 105, 225)  # RoyalBlue
BUTTON_HOVER = (30, 144, 255)  # DodgerBlue

# Fonts
pygame.font.init()
title_font = pygame.font.Font(None, 36)
subtitle_font = pygame.font.Font(None, 30)
text_font = pygame.font.Font(None, 24)

# Music attributes
genres = ["Pop", "Rock", "Hip Hop", "Electronic", "Classical"]
tempos = ["Slow", "Medium", "Fast"]
artists = ["Artist A", "Artist B", "Artist C", "Artist D", "Artist E"]

# Song class
class Song:
    def __init__(self, title, genre, tempo, artist):
        self.title = title
        self.genre = genre
        self.tempo = tempo
        self.artist = artist

# Create a list of sample songs
songs = [
    Song("Song 1", "Pop", "Medium", "Artist A"),
    Song("Song 2", "Rock", "Fast", "Artist B"),
    Song("Song 3", "Hip Hop", "Medium", "Artist C"),
    Song("Song 4", "Electronic", "Fast", "Artist D"),
    Song("Song 5", "Classical", "Slow", "Artist E"),
    Song("Song 6", "Pop", "Slow", "Artist B"),
    Song("Song 7", "Rock", "Medium", "Artist C"),
    Song("Song 8", "Hip Hop", "Fast", "Artist A"),
    Song("Song 9", "Electronic", "Medium", "Artist E"),
    Song("Song 10", "Classical", "Slow", "Artist D"),
]

current_song = random.choice(songs)

def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    screen.blit(text_surface, text_rect)

def draw_button(text, x, y, width, height, color, hover_color):
    mouse_pos = pygame.mouse.get_pos()
    if x < mouse_pos[0] < x + width and y < mouse_pos[1] < y + height:
        pygame.draw.rect(screen, hover_color, (x, y, width, height), border_radius=10)
    else:
        pygame.draw.rect(screen, color, (x, y, width, height), border_radius=10)
    text_surf = text_font.render(text, True, BACKGROUND)
    text_rect = text_surf.get_rect(center=((x + width/2), (y + height/2)))
    screen.blit(text_surf, text_rect)

def get_similarity_score(song1, song2):
    score = 0
    if song1.genre == song2.genre:
        score += 3
    if song1.tempo == song2.tempo:
        score += 2
    if song1.artist == song2.artist:
        score += 1
    return score

def get_recommendations(current_song, all_songs):
    recommendations = []
    for song in all_songs:
        if song != current_song:
            score = get_similarity_score(current_song, song)
            recommendations.append((song, score))
    recommendations.sort(key=lambda x: x[1], reverse=True)
    return recommendations[:5]

def draw_song_node(song, x, y, radius, color):
    pygame.draw.circle(screen, color, (x, y), radius)
    draw_text(song.title, text_font, TEXT_COLOR, x - 30, y - 10)

def draw_recommendation_graph(current_song, recommendations):
    center_x, center_y = 1200, 450
    current_radius = 60
    rec_radius = 50
    draw_song_node(current_song, center_x, center_y, current_radius, ACCENT_2)
    
    for i, (rec_song, score) in enumerate(recommendations):
        angle = i * (2 * math.pi / 5)
        x = center_x + int(250 * math.cos(angle))
        y = center_y + int(250 * math.sin(angle))
        draw_song_node(rec_song, x, y, rec_radius, ACCENT_1)
        
        # Draw connection line
        pygame.draw.line(screen, TEXT_COLOR, (center_x, center_y), (x, y), 2)
        
        # Draw similarity score
        mid_x = (center_x + x) // 2
        mid_y = (center_y + y) // 2
        draw_text(str(score), text_font, ACCENT_3, mid_x, mid_y)

def draw_panel(x, y, width, height, color):
    pygame.draw.rect(screen, color, (x, y, width, height), border_radius=10)

def main():
    global current_song

    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill(BACKGROUND)

        # Draw panels
        draw_panel(20, 20, 560, HEIGHT - 40, ACCENT_1)
        draw_panel(600, 20, WIDTH - 620, HEIGHT - 40, ACCENT_1)

        # Draw title and developer info
        draw_text("Content-Based Music Recommend System", title_font, TEXT_COLOR, 40, 40)
        draw_text("Developed by: Venugopal Adep", subtitle_font, TEXT_COLOR, 40, 90)

        # Draw current song info
        draw_text("Current Song:", subtitle_font, TEXT_COLOR, 40, 150)
        draw_text(f"Title: {current_song.title}", text_font, TEXT_COLOR, 40, 190)
        draw_text(f"Genre: {current_song.genre}", text_font, TEXT_COLOR, 40, 220)
        draw_text(f"Tempo: {current_song.tempo}", text_font, TEXT_COLOR, 40, 250)
        draw_text(f"Artist: {current_song.artist}", text_font, TEXT_COLOR, 40, 280)

        # Get and draw recommendations
        recommendations = get_recommendations(current_song, songs)
        draw_text("Recommended Songs:", subtitle_font, TEXT_COLOR, 40, 340)
        for i, (song, score) in enumerate(recommendations):
            draw_text(f"{song.title} (Score: {score})", text_font, TEXT_COLOR, 40, 380 + i * 30)

        # Draw recommendation graph
        draw_recommendation_graph(current_song, recommendations)

        # Draw action button
        draw_button("Change Current Song", 40, HEIGHT - 100, 200, 40, BUTTON_COLOR, BUTTON_HOVER)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if 40 <= x <= 240 and HEIGHT - 100 <= y <= HEIGHT - 60:
                    current_song = random.choice(songs)

        # Draw explanation
        draw_text("Explanation:", subtitle_font, TEXT_COLOR, 620, 40)
        draw_text("- The current song is shown in pink", text_font, TEXT_COLOR, 620, 80)
        draw_text("- Recommended songs are shown in blue", text_font, TEXT_COLOR, 620, 110)
        draw_text("- The numbers on the lines represent similarity scores:", text_font, TEXT_COLOR, 620, 140)
        draw_text("  +3 for matching genre, +2 for matching tempo, +1 for matching artist", text_font, TEXT_COLOR, 620, 170)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()