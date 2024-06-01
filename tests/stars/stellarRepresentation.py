import pygame
import math

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 800, 800
screen = pygame.display.set_mode((width, height))

# Star properties
metallicity = 0.7  # Adjust as needed (0.0 to 1.0)
luminosity = 0.8   # Adjust as needed (0.0 to 1.0)
mass = 0.6         # Adjust as needed (0.0 to 1.0)
color = (255, 255, 0)  # Yellow color

# Define a function to draw the star
def draw_star(surface, color, size, x, y):
    pygame.draw.circle(surface, color, (x, y), size)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Calculate size based on luminosity and mass
    star_size = int(50 * luminosity * mass)

    # Calculate color based on metallicity
    r = int(color[0] * (1 - metallicity))
    g = int(color[1] * (1 - metallicity))
    b = color[2]

    # Draw the star
    draw_star(screen, (r, g, b), star_size, width // 2, height // 2)

    pygame.display.flip()

pygame.quit()