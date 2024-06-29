import pygame
import sys
import random
import math

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 1600, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Smart Home IoT Dashboard")

# Colors
DARK_BG = (18, 18, 18)
LIGHT_BG = (240, 240, 240)
DARK_TEXT = (220, 220, 220)
LIGHT_TEXT = (18, 18, 18)
ACCENT = (0, 123, 255)
ACCENT_HOVER = (0, 86, 179)
GRAY = (128, 128, 128)

# Fonts
title_font = pygame.font.Font(None, 48)
subtitle_font = pygame.font.Font(None, 32)
text_font = pygame.font.Font(None, 24)

# Home devices
devices = [
    {"name": "Thermostat", "icon": "🌡️", "status": "Off", "recommendation": "", "color": ACCENT},
    {"name": "Lights", "icon": "💡", "status": "Off", "recommendation": "", "color": (255, 200, 0)},
    {"name": "TV", "icon": "📺", "status": "Off", "recommendation": "", "color": (255, 0, 0)},
    {"name": "Security", "icon": "🔒", "status": "Off", "recommendation": "", "color": (0, 200, 0)},
]

# User behavior patterns
user_patterns = {
    "wake_time": 7,
    "sleep_time": 22,
    "preferred_temp": 22,
    "tv_time": 20,
}

# Environmental data
env_data = {
    "temperature": 20,
    "time": 12,
    "light_level": 50,
}

# Dark mode toggle
dark_mode = False

def draw_text(text, font, color, x, y, align="center"):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    if align == "center":
        text_rect.center = (x, y)
    elif align == "left":
        text_rect.midleft = (x, y)
    elif align == "right":
        text_rect.midright = (x, y)
    screen.blit(text_surface, text_rect)

def draw_button(text, x, y, width, height, color, text_color, hover_color):
    mouse_pos = pygame.mouse.get_pos()
    button_rect = pygame.Rect(x, y, width, height)
    
    if button_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, hover_color, button_rect, border_radius=10)
    else:
        pygame.draw.rect(screen, color, button_rect, border_radius=10)
    
    draw_text(text, text_font, text_color, x + width // 2, y + height // 2)
    return button_rect

def draw_device(device, x, y, width, height):
    color = device["color"] if device["status"] == "On" else GRAY
    pygame.draw.rect(screen, color, (x, y, width, height), border_radius=15)
    draw_text(f"{device['icon']} {device['name']}", subtitle_font, DARK_TEXT, x + width // 2, y + 30)
    draw_text(f"Status: {device['status']}", text_font, DARK_TEXT, x + width // 2, y + 70)
    draw_text(device['recommendation'], text_font, DARK_TEXT, x + width // 2, y + height - 30)

def update_recommendations():
    # Thermostat
    if env_data["temperature"] < user_patterns["preferred_temp"]:
        devices[0]["recommendation"] = "Increase temperature"
    elif env_data["temperature"] > user_patterns["preferred_temp"]:
        devices[0]["recommendation"] = "Decrease temperature"
    else:
        devices[0]["recommendation"] = "Temperature is optimal"

    # Lights
    if env_data["time"] >= user_patterns["sleep_time"] or env_data["time"] < user_patterns["wake_time"]:
        devices[1]["recommendation"] = "Turn off lights"
    elif env_data["light_level"] < 30:
        devices[1]["recommendation"] = "Turn on lights"
    else:
        devices[1]["recommendation"] = "Light level is good"

    # TV
    if env_data["time"] == user_patterns["tv_time"]:
        devices[2]["recommendation"] = "Turn on TV for usual viewing"
    elif env_data["time"] >= user_patterns["sleep_time"]:
        devices[2]["recommendation"] = "Turn off TV for bedtime"
    else:
        devices[2]["recommendation"] = "No TV recommendation"

    # Security Camera
    if env_data["time"] >= user_patterns["sleep_time"] or env_data["time"] < user_patterns["wake_time"]:
        devices[3]["recommendation"] = "Activate night mode"
    else:
        devices[3]["recommendation"] = "Standard monitoring"

def main():
    global dark_mode
    clock = pygame.time.Clock()
    time_speed = 1

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for i, device in enumerate(devices):
                        if device_rects[i].collidepoint(event.pos):
                            device["status"] = "On" if device["status"] == "Off" else "Off"
                    if speed_button.collidepoint(event.pos):
                        time_speed = 5 if time_speed == 1 else 1
                    if reset_button.collidepoint(event.pos):
                        env_data["time"] = 12
                    if mode_toggle.collidepoint(event.pos):
                        dark_mode = not dark_mode

        # Update environmental data
        env_data["time"] = (env_data["time"] + time_speed / 3600) % 24
        env_data["temperature"] += random.uniform(-0.1, 0.1) * time_speed
        env_data["light_level"] = max(0, min(100, env_data["light_level"] + random.uniform(-1, 1) * time_speed))

        update_recommendations()

        # Set colors based on mode
        bg_color = DARK_BG if dark_mode else LIGHT_BG
        text_color = DARK_TEXT if dark_mode else LIGHT_TEXT
        
        # Draw background
        screen.fill(bg_color)

        # Draw title and subtitle
        draw_text("Smart Home IoT Dashboard", title_font, text_color, WIDTH // 2, 50)
        draw_text("Developed by: Venugopal Adep", subtitle_font, text_color, WIDTH // 2, 100)

        # Draw devices
        device_rects = []
        for i, device in enumerate(devices):
            x = 50 + (i % 2) * 400
            y = 200 + (i // 2) * 300
            draw_device(device, x, y, 350, 250)
            device_rects.append(pygame.Rect(x, y, 350, 250))

        # Draw buttons
        speed_button = draw_button(f"{'▶▶' if time_speed == 1 else '▶'} Speed: {time_speed}x", 
                                   WIDTH // 2 - 160, HEIGHT - 80, 150, 50, ACCENT, DARK_TEXT, ACCENT_HOVER)
        reset_button = draw_button("Reset Time", WIDTH // 2 + 10, HEIGHT - 80, 150, 50, ACCENT, DARK_TEXT, ACCENT_HOVER)

        # Draw mode toggle
        mode_toggle = draw_button("Toggle Dark/Light Mode", WIDTH - 250, 20, 200, 40, ACCENT, DARK_TEXT, ACCENT_HOVER)

        # Draw environmental data
        draw_text(f"Time: {int(env_data['time']):02d}:{int(env_data['time'] % 1 * 60):02d}", text_font, text_color, 50, HEIGHT - 120, "left")
        draw_text(f"Temperature: {env_data['temperature']:.1f}°C", text_font, text_color, 50, HEIGHT - 90, "left")
        draw_text(f"Light Level: {env_data['light_level']:.0f}%", text_font, text_color, 50, HEIGHT - 60, "left")

        # Draw user patterns
        draw_text(f"Wake Time: {user_patterns['wake_time']:02d}:00", text_font, text_color, WIDTH - 50, HEIGHT - 120, "right")
        draw_text(f"Sleep Time: {user_patterns['sleep_time']:02d}:00", text_font, text_color, WIDTH - 50, HEIGHT - 90, "right")
        draw_text(f"Preferred Temp: {user_patterns['preferred_temp']}°C", text_font, text_color, WIDTH - 50, HEIGHT - 60, "right")

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()