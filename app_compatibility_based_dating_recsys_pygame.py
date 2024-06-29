import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 1600, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dating App Recommendation Demo")

# Colors
BACKGROUND = (240, 248, 255)  # Alice Blue
TEXT_COLOR = (47, 79, 79)  # Dark Slate Gray
PRIMARY = (70, 130, 180)  # Steel Blue
SECONDARY = (255, 182, 193)  # Light Pink
ACCENT = (255, 140, 0)  # Dark Orange
BUTTON_INACTIVE = (176, 196, 222)  # Light Steel Blue
BUTTON_HOVER = (135, 206, 250)  # Light Sky Blue
BUTTON_ACTIVE = (100, 149, 237)  # Cornflower Blue

# Fonts
title_font = pygame.font.Font(None, 58)
subtitle_font = pygame.font.Font(None, 42)
text_font = pygame.font.Font(None, 28)

# User class
class User:
    def __init__(self, x, y, name, age, interests):
        self.x = x
        self.y = y
        self.radius = 35
        self.name = name
        self.age = age
        self.interests = interests
        self.color = (random.randint(100, 200), random.randint(100, 200), random.randint(100, 200))

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(screen, TEXT_COLOR, (int(self.x), int(self.y)), self.radius, 2)
        name_text = text_font.render(self.name, True, TEXT_COLOR)
        screen.blit(name_text, (self.x - name_text.get_width() // 2, self.y + self.radius + 5))

    def is_clicked(self, mouse_pos):
        distance = math.sqrt((mouse_pos[0] - self.x)**2 + (mouse_pos[1] - self.y)**2)
        return distance <= self.radius

# Create users
users = [
    User(400, 300, "Alice", 28, ["music", "sports", "travel"]),
    User(800, 500, "Bob", 32, ["movies", "cooking", "art"]),
    User(1200, 300, "Charlie", 25, ["sports", "technology", "photography"]),
    User(400, 700, "Diana", 30, ["travel", "food", "music"]),
    User(800, 200, "Eve", 27, ["art", "literature", "technology"]),
    User(1200, 700, "Frank", 35, ["cooking", "fitness", "travel"])
]

main_user = User(WIDTH // 2, HEIGHT // 2, "You", 29, ["music", "travel", "technology"])

# Function to calculate compatibility
def calculate_compatibility(user1, user2):
    common_interests = set(user1.interests) & set(user2.interests)
    return len(common_interests) / len(set(user1.interests + user2.interests))

# Function to draw a button
def draw_button(x, y, width, height, text, color, hover_color, action=None):
    mouse_pos = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x < mouse_pos[0] < x + width and y < mouse_pos[1] < y + height:
        pygame.draw.rect(screen, hover_color, (x, y, width, height), border_radius=10)
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(screen, color, (x, y, width, height), border_radius=10)

    text_surface = text_font.render(text, True, TEXT_COLOR)
    text_rect = text_surface.get_rect(center=(x + width/2, y + height/2))
    screen.blit(text_surface, text_rect)

# Main game loop
running = True
clock = pygame.time.Clock()
selected_user = None
showing_info = False

interest_options = ["music", "sports", "travel", "movies", "cooking", "art", "technology", "photography", "food", "literature", "fitness"]

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            
            # Check if a user is clicked
            for user in users:
                if user.is_clicked(mouse_pos):
                    selected_user = user
                    showing_info = True
                    break
            
            # Check if "Close" button is clicked
            if showing_info and 1350 <= mouse_pos[0] <= 1550 and 750 <= mouse_pos[1] <= 790:
                showing_info = False
            
            # Check if interest buttons are clicked
            if 20 <= mouse_pos[0] <= 220:
                for i, interest in enumerate(interest_options):
                    if 200 + i*40 <= mouse_pos[1] <= 230 + i*40:
                        if interest in main_user.interests:
                            main_user.interests.remove(interest)
                        else:
                            main_user.interests.append(interest)

    # Clear the screen
    screen.fill(BACKGROUND)

    # Draw title and subtitle
    title_text = title_font.render("Dating App Recommendation Demo", True, PRIMARY)
    subtitle_text = subtitle_font.render("Developed by: Venugopal Adep", True, SECONDARY)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 20))
    screen.blit(subtitle_text, (WIDTH // 2 - subtitle_text.get_width() // 2, 80))

    # Draw main user
    main_user.draw()
    pygame.draw.circle(screen, ACCENT, (int(main_user.x), int(main_user.y)), main_user.radius + 5, 3)

    # Draw other users and calculate compatibility
    for user in users:
        user.draw()
        compatibility = calculate_compatibility(main_user, user)
        
        # Draw connection line
        line_color = (int(255 * (1 - compatibility)), int(255 * compatibility), 0)
        pygame.draw.line(screen, line_color, (main_user.x, main_user.y), (user.x, user.y), 3)
        
        # Display compatibility percentage
        compatibility_text = text_font.render(f"{int(compatibility * 100)}%", True, TEXT_COLOR)
        midpoint = ((main_user.x + user.x) // 2, (main_user.y + user.y) // 2)
        screen.blit(compatibility_text, midpoint)

    # Display user interests
    interests_text = text_font.render(f"Your interests:", True, TEXT_COLOR)
    screen.blit(interests_text, (20, 160))

    # Display legend
    legend_text = text_font.render("Connection color: Red (Low Compatibility) to Green (High Compatibility)", True, TEXT_COLOR)
    screen.blit(legend_text, (WIDTH - legend_text.get_width() - 20, HEIGHT - 40))

    # Draw interest selection buttons
    for i, interest in enumerate(interest_options):
        color = BUTTON_ACTIVE if interest in main_user.interests else BUTTON_INACTIVE
        draw_button(20, 200 + i*40, 200, 30, interest, color, BUTTON_HOVER)

    # Show selected user info
    if showing_info and selected_user:
        info_surface = pygame.Surface((300, 700), pygame.SRCALPHA)
        info_surface.fill((255, 255, 255, 220))
        screen.blit(info_surface, (1250, 100))
        
        name_text = text_font.render(f"Name: {selected_user.name}", True, TEXT_COLOR)
        age_text = text_font.render(f"Age: {selected_user.age}", True, TEXT_COLOR)
        interests_text = text_font.render(f"Interests:", True, TEXT_COLOR)
        compatibility = calculate_compatibility(main_user, selected_user)
        compatibility_text = text_font.render(f"Compatibility: {int(compatibility * 100)}%", True, TEXT_COLOR)
        
        screen.blit(name_text, (1270, 120))
        screen.blit(age_text, (1270, 150))
        screen.blit(interests_text, (1270, 180))
        for i, interest in enumerate(selected_user.interests):
            interest_text = text_font.render(f"- {interest}", True, TEXT_COLOR)
            screen.blit(interest_text, (1290, 210 + i*30))
        screen.blit(compatibility_text, (1270, 350))
        
        draw_button(1300, 750, 200, 40, "Close", BUTTON_INACTIVE, BUTTON_HOVER)

    # Update the display
    pygame.display.flip()
    clock.tick(60)

# Quit Pygame
pygame.quit()