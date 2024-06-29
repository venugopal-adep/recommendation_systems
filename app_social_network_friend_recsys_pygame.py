import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 1600, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Social Network Friend Recommendation Demo")

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

# Interests
interests = ["Sports", "Music", "Movies", "Technology", "Travel", "Food", "Art", "Books", "Gaming", "Fashion"]

# User class
class User:
    def __init__(self, name, interests):
        self.name = name
        self.interests = interests
        self.friends = set()
        self.interactions = {}

# Create sample users
users = [
    User("Alice", ["Sports", "Music", "Technology"]),
    User("Bob", ["Movies", "Gaming", "Technology"]),
    User("Charlie", ["Travel", "Food", "Art"]),
    User("David", ["Books", "Music", "Art"]),
    User("Eve", ["Fashion", "Travel", "Movies"]),
    User("Frank", ["Sports", "Gaming", "Food"]),
    User("Grace", ["Technology", "Books", "Music"])
]

# Set up some initial friendships and interactions
for user in users:
    for other_user in users:
        if user != other_user:
            if random.random() < 0.3:  # 30% chance of being friends
                user.friends.add(other_user)
                other_user.friends.add(user)
            user.interactions[other_user] = random.randint(0, 10)  # Random interaction count

current_user = random.choice(users)

def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    screen.blit(text_surface, text_rect)

def draw_button(text, x, y, width, height, color):
    pygame.draw.rect(screen, color, (x, y, width, height))
    draw_text(text, text_font, BLACK, x + 10, y + 10)

def get_friend_score(user, other_user):
    score = 0
    mutual_friends = len(user.friends.intersection(other_user.friends))
    score += mutual_friends * 2  # 2 points for each mutual friend
    common_interests = len(set(user.interests).intersection(set(other_user.interests)))
    score += common_interests * 3  # 3 points for each common interest
    score += user.interactions.get(other_user, 0)  # 1 point for each interaction
    return score

def get_recommendations(user, all_users):
    scored_users = [(other_user, get_friend_score(user, other_user)) 
                    for other_user in all_users if other_user not in user.friends and other_user != user]
    scored_users.sort(key=lambda x: x[1], reverse=True)
    return scored_users[:5]

def draw_network(user, recommendations, x, y, radius):
    # Draw current user
    pygame.draw.circle(screen, BLUE, (x, y), 30)
    draw_text(user.name, small_font, WHITE, x - 20, y - 10)
    
    # Draw friends
    friend_positions = {}
    for i, friend in enumerate(user.friends):
        angle = i * (2 * math.pi / len(user.friends))
        fx = x + int(radius * 0.6 * math.cos(angle))
        fy = y + int(radius * 0.6 * math.sin(angle))
        pygame.draw.circle(screen, GREEN, (fx, fy), 20)
        draw_text(friend.name, small_font, BLACK, fx - 20, fy - 10)
        pygame.draw.line(screen, GRAY, (x, y), (fx, fy), 2)
        friend_positions[friend] = (fx, fy)
    
    # Draw recommended users
    for i, (rec_user, score) in enumerate(recommendations):
        angle = i * (2 * math.pi / len(recommendations))
        rx = x + int(radius * math.cos(angle))
        ry = y + int(radius * math.sin(angle))
        pygame.draw.circle(screen, YELLOW, (rx, ry), 25)
        draw_text(rec_user.name, small_font, BLACK, rx - 20, ry - 10)
        draw_text(f"Score: {score}", small_font, BLACK, rx - 20, ry + 10)
        
        # Draw lines to mutual friends
        for friend in user.friends.intersection(rec_user.friends):
            fx, fy = friend_positions[friend]
            pygame.draw.line(screen, RED, (rx, ry), (fx, fy), 1)

def main():
    global current_user

    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill(WHITE)

        # Draw title and developer info
        draw_text("Social Network Friend Recommendation Demo", title_font, BLACK, 20, 20)
        draw_text("Developed by: Venugopal Adep", text_font, BLACK, 20, 70)

        # Draw current user info
        draw_text(f"Current User: {current_user.name}", text_font, BLACK, 20, 120)
        draw_text(f"Interests: {', '.join(current_user.interests)}", text_font, BLACK, 20, 150)
        draw_text(f"Friends: {', '.join([friend.name for friend in current_user.friends])}", text_font, BLACK, 20, 180)

        # Get and draw recommendations
        recommendations = get_recommendations(current_user, users)
        draw_text("Recommended Friends:", text_font, BLACK, 20, 240)
        for i, (user, score) in enumerate(recommendations):
            draw_text(f"{user.name} (Score: {score})", text_font, BLACK, 20, 270 + i * 30)

        # Draw network visualization
        draw_network(current_user, recommendations, 1000, 400, 300)

        # Draw action button
        draw_button("Switch User", 20, 450, 200, 40, GREEN)

        # Draw explanation
        draw_text("How friend recommendations are scored:", text_font, BLACK, 20, 550)
        draw_text("- +2 points for each mutual friend (red lines)", small_font, BLACK, 20, 580)
        draw_text("- +3 points for each common interest", small_font, BLACK, 20, 605)
        draw_text("- +1 point for each previous interaction", small_font, BLACK, 20, 630)
        draw_text("Blue: Current User, Green: Friends, Yellow: Recommendations", small_font, BLACK, 20, 655)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if 20 <= x <= 220 and 450 <= y <= 490:  # Switch User
                    current_user = random.choice(users)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()