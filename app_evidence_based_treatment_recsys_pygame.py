import pygame
import sys
import pygame_gui

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 1600, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Evidence-Based Treatment Recommendation System")

# Colors
BACKGROUND = pygame.Color('#F0F0F0')
PRIMARY = pygame.Color('#1A5F7A')
SECONDARY = pygame.Color('#159895')
ACCENT = pygame.Color('#FFA500')
WHITE = pygame.Color('#FFFFFF')
BLACK = pygame.Color('#000000')

# Create GUI manager
manager = pygame_gui.UIManager((WIDTH, HEIGHT))

# Fonts
title_font = pygame.font.Font(None, 48)
subtitle_font = pygame.font.Font(None, 36)
text_font = pygame.font.Font(None, 24)

# Patient data (unchanged)
patients = [
    {
        "name": "John Doe",
        "data": {
            "Age": 45,
            "Gender": "Male",
            "BMI": 28.5,
            "Blood Pressure": "140/90",
            "Cholesterol": 220,
            "Smoking": "Yes",
            "Diabetes": "No"
        },
        "history": [
            "Hypertension (5 years)",
            "Family history of heart disease",
            "Occasional chest pain"
        ],
        "recommendations": [
            "Prescribe antihypertensive medication",
            "Recommend low-fat, low-sodium diet",
            "Advise smoking cessation program",
            "Suggest regular exercise routine",
            "Schedule follow-up in 3 months"
        ]
    },
    {
        "name": "Jane Smith",
        "data": {
            "Age": 38,
            "Gender": "Female",
            "BMI": 24.2,
            "Blood Pressure": "120/80",
            "Cholesterol": 190,
            "Smoking": "No",
            "Diabetes": "Yes"
        },
        "history": [
            "Type 2 Diabetes (3 years)",
            "Gestational diabetes during pregnancy",
            "Mild asthma"
        ],
        "recommendations": [
            "Continue current diabetes medication",
            "Recommend regular blood sugar monitoring",
            "Suggest Mediterranean diet",
            "Advise moderate aerobic exercise",
            "Schedule diabetes education session"
        ]
    }
]

# Clinical guidelines (unchanged)
clinical_guidelines = [
    "If BP > 140/90, consider medication",
    "If cholesterol > 200, recommend lifestyle changes",
    "If smoking, advise cessation",
    "If BMI > 25, suggest weight loss",
    "If diabetes, monitor blood sugar closely"
]

# Create UI elements
patient_list = pygame_gui.elements.UISelectionList(
    relative_rect=pygame.Rect((20, 100), (300, 600)),
    item_list=[f"{p['name']} ({p['data']['Age']} y/o {p['data']['Gender']})" for p in patients],
    manager=manager
)

# Replace tab group with buttons
patient_data_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((340, 100), (200, 50)),
    text='Patient Data',
    manager=manager
)

medical_history_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((550, 100), (200, 50)),
    text='Medical History',
    manager=manager
)

clinical_guidelines_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((760, 100), (200, 50)),
    text='Clinical Guidelines',
    manager=manager
)

generate_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((1260, 100), (300, 50)),
    text='Generate Recommendations',
    manager=manager
)

search_box = pygame_gui.elements.UITextEntryLine(
    relative_rect=pygame.Rect((1260, 170), (300, 50)),
    manager=manager
)

# Main game loop
def main():
    clock = pygame.time.Clock()
    current_patient_index = 0
    recommendations_generated = False
    active_section = 'Patient Data'

    while True:
        time_delta = clock.tick(60)/1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame_gui.UI_SELECTION_LIST_NEW_SELECTION:
                if event.ui_element == patient_list:
                    selected_patient = patient_list.get_single_selection()
                    if selected_patient is not None:
                        current_patient_index = next(i for i, p in enumerate(patients) if f"{p['name']} ({p['data']['Age']} y/o {p['data']['Gender']})" == selected_patient)
                    recommendations_generated = False

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == generate_button:
                    recommendations_generated = True
                elif event.ui_element == patient_data_button:
                    active_section = 'Patient Data'
                elif event.ui_element == medical_history_button:
                    active_section = 'Medical History'
                elif event.ui_element == clinical_guidelines_button:
                    active_section = 'Clinical Guidelines'

            manager.process_events(event)

        manager.update(time_delta)

        screen.fill(BACKGROUND)

        # Draw title
        title_text = title_font.render("Evidence-Based Treatment Recommendation System", True, PRIMARY)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 20))

        # Draw subtitle
        subtitle_text = subtitle_font.render("Developed by: Venugopal Adep", True, SECONDARY)
        screen.blit(subtitle_text, (WIDTH // 2 - subtitle_text.get_width() // 2, 70))

        # Display content
        content_rect = pygame.Rect((340, 160), (900, 540))
        pygame.draw.rect(screen, WHITE, content_rect)
        pygame.draw.rect(screen, PRIMARY, content_rect, 2)

        if active_section == 'Patient Data':
            for i, (key, value) in enumerate(patients[current_patient_index]['data'].items()):
                text = text_font.render(f"{key}: {value}", True, BLACK)
                screen.blit(text, (360, 180 + i * 30))
        elif active_section == 'Medical History':
            for i, item in enumerate(patients[current_patient_index]['history']):
                text = text_font.render(f"- {item}", True, BLACK)
                screen.blit(text, (360, 180 + i * 30))
        elif active_section == 'Clinical Guidelines':
            for i, guideline in enumerate(clinical_guidelines):
                text = text_font.render(f"- {guideline}", True, BLACK)
                screen.blit(text, (360, 180 + i * 30))

        # Display recommendations
        if recommendations_generated:
            recommendations_rect = pygame.Rect((1260, 240), (300, 460))
            pygame.draw.rect(screen, WHITE, recommendations_rect)
            pygame.draw.rect(screen, ACCENT, recommendations_rect, 2)

            recommendations_text = subtitle_font.render("Recommendations:", True, PRIMARY)
            screen.blit(recommendations_text, (1270, 250))

            for i, recommendation in enumerate(patients[current_patient_index]['recommendations']):
                text = text_font.render(f"- {recommendation}", True, BLACK)
                screen.blit(text, (1270, 290 + i * 30))

        manager.draw_ui(screen)

        pygame.display.flip()

if __name__ == "__main__":
    main()