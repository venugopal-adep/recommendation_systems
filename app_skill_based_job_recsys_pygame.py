import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 1600, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Skill-Based Job Recommendation System Demo")

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

# Skills and job categories
skills = ["Python", "Java", "JavaScript", "SQL", "Machine Learning", "Data Analysis", "Web Development", "DevOps", "UI/UX Design", "Project Management"]
job_categories = ["Software Development", "Data Science", "Web Design", "IT Operations", "Product Management"]

# User class
class User:
    def __init__(self, name, skills, experience, preferred_categories):
        self.name = name
        self.skills = skills
        self.experience = experience
        self.preferred_categories = preferred_categories

# Job class
class Job:
    def __init__(self, title, company, required_skills, category, experience_level):
        self.title = title
        self.company = company
        self.required_skills = required_skills
        self.category = category
        self.experience_level = experience_level

# Create sample users
users = [
    User("Alice", ["Python", "Machine Learning", "Data Analysis"], 3, ["Data Science", "Software Development"]),
    User("Bob", ["JavaScript", "HTML", "CSS", "UI/UX Design"], 2, ["Web Design", "Software Development"]),
    User("Charlie", ["Java", "SQL", "DevOps"], 5, ["IT Operations", "Software Development"])
]

current_user = random.choice(users)

# Create sample jobs
jobs = [
    Job("Data Scientist", "TechCorp", ["Python", "Machine Learning", "SQL"], "Data Science", 3),
    Job("Front-end Developer", "WebSolutions", ["JavaScript", "HTML", "CSS"], "Web Design", 2),
    Job("Java Developer", "SoftwareInc", ["Java", "SQL", "Spring"], "Software Development", 4),
    Job("DevOps Engineer", "CloudTech", ["Linux", "AWS", "Docker"], "IT Operations", 3),
    Job("Product Manager", "InnovateCo", ["Project Management", "Agile", "Data Analysis"], "Product Management", 5),
    Job("Full Stack Developer", "StartupX", ["JavaScript", "Python", "SQL", "React"], "Software Development", 3),
    Job("UX Designer", "DesignPro", ["UI/UX Design", "Figma", "User Research"], "Web Design", 2),
    Job("Machine Learning Engineer", "AILabs", ["Python", "Machine Learning", "TensorFlow"], "Data Science", 4),
    Job("Database Administrator", "DataCo", ["SQL", "Oracle", "Database Management"], "IT Operations", 5),
    Job("Scrum Master", "AgileTeam", ["Project Management", "Agile", "JIRA"], "Product Management", 3)
]

def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    screen.blit(text_surface, text_rect)

def draw_button(text, x, y, width, height, color):
    pygame.draw.rect(screen, color, (x, y, width, height))
    draw_text(text, text_font, BLACK, x + 10, y + 10)

def get_job_score(job, user):
    score = 0
    skill_match = len(set(job.required_skills) & set(user.skills))
    score += skill_match * 2  # 2 points for each matching skill
    if job.category in user.preferred_categories:
        score += 3  # 3 points for matching job category
    experience_diff = abs(job.experience_level - user.experience)
    score += max(0, 3 - experience_diff)  # 0-3 points based on experience match
    return score

def get_recommendations(user, all_jobs):
    scored_jobs = [(job, get_job_score(job, user)) for job in all_jobs]
    scored_jobs.sort(key=lambda x: x[1], reverse=True)
    return scored_jobs[:5]

def draw_job_listings(recommendations, x, y):
    for i, (job, score) in enumerate(recommendations):
        pygame.draw.rect(screen, GRAY, (x, y + i * 70, 700, 60))
        draw_text(f"{job.title} at {job.company}", text_font, BLACK, x + 10, y + i * 70 + 5)
        draw_text(f"Required Skills: {', '.join(job.required_skills)}", small_font, BLACK, x + 10, y + i * 70 + 25)
        draw_text(f"Category: {job.category}", small_font, BLACK, x + 10, y + i * 70 + 45)
        draw_text(f"Experience: {job.experience_level} years", small_font, BLACK, x + 350, y + i * 70 + 45)
        draw_text(f"Match Score: {score}", small_font, RED, x + 600, y + i * 70 + 25)

def main():
    global current_user

    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill(WHITE)

        # Draw title and developer info
        draw_text("Skill-Based Job Recommendation System Demo", title_font, BLACK, 20, 20)
        draw_text("Developed by: Venugopal Adep", text_font, BLACK, 20, 70)

        # Draw current user info
        draw_text(f"Current User: {current_user.name}", text_font, BLACK, 20, 120)
        draw_text(f"Skills: {', '.join(current_user.skills)}", text_font, BLACK, 20, 150)
        draw_text(f"Experience: {current_user.experience} years", text_font, BLACK, 20, 180)
        draw_text(f"Preferred Job Categories: {', '.join(current_user.preferred_categories)}", text_font, BLACK, 20, 210)

        # Get and draw recommendations
        recommendations = get_recommendations(current_user, jobs)
        draw_text("Recommended Jobs:", text_font, BLACK, 800, 120)
        draw_job_listings(recommendations, 800, 150)

        # Draw action button
        draw_button("Switch User", 20, 250, 200, 40, GREEN)

        # Draw explanation
        draw_text("How job recommendations are scored:", text_font, BLACK, 20, 550)
        draw_text("- +2 points for each matching skill", small_font, BLACK, 20, 580)
        draw_text("- +3 points if the job category matches user preferences", small_font, BLACK, 20, 605)
        draw_text("- 0-3 points based on how closely the required experience matches the user's experience", small_font, BLACK, 20, 630)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if 20 <= x <= 220 and 250 <= y <= 290:  # Switch User
                    current_user = random.choice(users)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()