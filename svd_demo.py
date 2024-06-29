import pygame
import numpy as np
from scipy.linalg import svd

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 1600, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Singular Value Decomposition (SVD) Demo")

# Colors
BACKGROUND = (240, 240, 245)
TEXT_COLOR = (50, 50, 50)
MATRIX_BG = (255, 255, 255)
MATRIX_BORDER = (100, 100, 100)
BUTTON_COLOR = (70, 130, 180)
BUTTON_HOVER = (100, 160, 210)
HIGHLIGHT_COLOR = (255, 215, 0)

# Fonts
font_large = pygame.font.Font(None, 56)
font_medium = pygame.font.Font(None, 40)
font_small = pygame.font.Font(None, 28)

# SVD parameters
matrix_size = 3
original_matrix = np.random.rand(matrix_size, matrix_size)
U, s, Vt = svd(original_matrix)

# Button parameters
button_width, button_height = 220, 60
button_x, button_y = WIDTH - button_width - 40, HEIGHT - button_height - 40

def draw_matrix(matrix, x, y, title, highlight=False):
    cell_size = 60
    padding = 20
    bg_color = HIGHLIGHT_COLOR if highlight else MATRIX_BG
    pygame.draw.rect(screen, bg_color, (x-padding, y-padding-40, matrix.shape[1]*cell_size+padding*2, matrix.shape[0]*cell_size+padding*2+40), border_radius=10)
    pygame.draw.rect(screen, MATRIX_BORDER, (x-padding, y-padding-40, matrix.shape[1]*cell_size+padding*2, matrix.shape[0]*cell_size+padding*2+40), 2, border_radius=10)
    text = font_medium.render(title, True, TEXT_COLOR)
    screen.blit(text, (x, y-50))
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            value = f"{matrix[i, j]:.2f}"
            text = font_small.render(value, True, TEXT_COLOR)
            text_rect = text.get_rect(center=(x + j*cell_size + cell_size//2, y + i*cell_size + cell_size//2))
            screen.blit(text, text_rect)

def draw_button(text, hover=False):
    color = BUTTON_HOVER if hover else BUTTON_COLOR
    pygame.draw.rect(screen, color, (button_x, button_y, button_width, button_height), border_radius=30)
    text_surface = font_medium.render(text, True, MATRIX_BG)
    text_rect = text_surface.get_rect(center=(button_x + button_width//2, button_y + button_height//2))
    screen.blit(text_surface, text_rect)

def draw_explanation(explanation):
    pygame.draw.rect(screen, MATRIX_BG, (50, HEIGHT-200, WIDTH-100, 180), border_radius=10)
    pygame.draw.rect(screen, MATRIX_BORDER, (50, HEIGHT-200, WIDTH-100, 180), 2, border_radius=10)
    for i, line in enumerate(explanation):
        text = font_small.render(line, True, TEXT_COLOR)
        screen.blit(text, (70, HEIGHT-180 + i * 35))

def main():
    global original_matrix, U, s, Vt
    
    step = 0
    running = True
    clock = pygame.time.Clock()

    while running:
        mouse_pos = pygame.mouse.get_pos()
        button_hover = button_x <= mouse_pos[0] <= button_x + button_width and button_y <= mouse_pos[1] <= button_y + button_height

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_hover:
                    if step < 4:
                        step += 1
                    else:
                        step = 0
                        original_matrix = np.random.rand(matrix_size, matrix_size)
                        U, s, Vt = svd(original_matrix)

        screen.fill(BACKGROUND)

        # Draw title and author
        title = font_large.render("Enhanced Singular Value Decomposition (SVD) Demo", True, TEXT_COLOR)
        author = font_medium.render("Developed by: Venugopal Adep", True, TEXT_COLOR)
        screen.blit(title, (50, 30))
        screen.blit(author, (50, 90))

        if step == 0:
            draw_matrix(original_matrix, 100, 200, "Original Matrix A", highlight=True)
            explanation = [
                "SVD decomposes a matrix A into the product of three matrices: A = U * Σ * V^T",
                "U and V are orthogonal matrices, and Σ is a diagonal matrix containing the singular values of A.",
                "Click 'Next Step' to see the decomposition process."
            ]
        elif step == 1:
            draw_matrix(original_matrix, 100, 200, "Original Matrix A")
            draw_matrix(U, 600, 200, "Left Singular Vectors (U)", highlight=True)
            explanation = [
                "U is an orthogonal matrix containing the left singular vectors.",
                "These vectors represent the principal directions in the column space of A.",
                "The columns of U form an orthonormal basis for the column space of A."
            ]
        elif step == 2:
            draw_matrix(original_matrix, 100, 200, "Original Matrix A")
            draw_matrix(U, 600, 200, "Left Singular Vectors (U)")
            draw_matrix(np.diag(s), 1100, 200, "Singular Values (Σ)", highlight=True)
            explanation = [
                "Σ is a diagonal matrix containing the singular values.",
                "These values represent the scaling factors along the principal directions.",
                "Larger singular values correspond to more significant features or patterns in the data."
            ]
        elif step == 3:
            draw_matrix(original_matrix, 100, 200, "Original Matrix A")
            draw_matrix(U, 450, 200, "Left Singular Vectors (U)")
            draw_matrix(np.diag(s), 800, 200, "Singular Values (Σ)")
            draw_matrix(Vt, 1150, 200, "Right Singular Vectors (V^T)", highlight=True)
            explanation = [
                "V^T is the transpose of an orthogonal matrix V, containing the right singular vectors.",
                "These vectors represent the principal directions in the row space of A.",
                "The rows of V^T form an orthonormal basis for the row space of A."
            ]
        elif step == 4:
            reconstructed = U @ np.diag(s) @ Vt
            draw_matrix(original_matrix, 100, 200, "Original Matrix A")
            draw_matrix(reconstructed, 600, 200, "Reconstructed Matrix", highlight=True)
            error = np.linalg.norm(original_matrix - reconstructed)
            explanation = [
                f"The original matrix A has been reconstructed using SVD. Reconstruction error: {error:.6f}",
                "SVD can be used for dimensionality reduction, data compression, and feature extraction.",
                "It's particularly useful in applications like image processing, recommendation systems, and machine learning."
            ]

        draw_explanation(explanation)

        if step < 4:
            draw_button("Next Step", hover=button_hover)
        else:
            draw_button("Restart", hover=button_hover)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()