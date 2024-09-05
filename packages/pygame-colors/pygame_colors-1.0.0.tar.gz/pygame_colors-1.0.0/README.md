# pygame_colors

`pygame_colors` is a simple Python module for Pygame that provides pre-defined color names and utility functions to make Pygame scripts easier to read and write.

# Author: Basit Ahmad Ganie 
email : basitahmed1412@gmail.com

## Installation

You can install the package via pip:

```bash
 pip install pygame_colors
 ```
 Example usage:
     
     ```python
import pygame
from pygame_colors import get_color, lighten, darken

# Initialize Pygame
pygame.init()

# Set up screen
screen = pygame.display.set_mode((400, 300))

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Set background color using 'skyblue'
    screen.fill(get_color('skyblue'))

    # Draw a rectangle with a lighter version of 'firebrick'
    pygame.draw.rect(screen, lighten(get_color('firebrick')), (50, 50, 100, 50))

    pygame.display.flip()

pygame.quit()

```
