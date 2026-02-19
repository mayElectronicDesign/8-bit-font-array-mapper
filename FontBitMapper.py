#   Make sure to install pygame in your venv before attempting to run the program.
#   this program outputs a csv which you can use to create an array in a different
#   program for a bitmapped font. I used this to interpolate the zx spectrum's 
#   version of the MICR font for an LED matrix project! If you don't delete, move, or
#   rename your previous csv, new entries will continue to fill the old file, duplicates 
#   aren't handled by this software.

import pygame
import csv
import os

pygame.init()

# UI dimensions
SCREEN_DIM = 550
GRID_OFFSET_Y = 100
GRID_SIZE = 8
CELL_SIZE = 400 // GRID_SIZE
MARGIN = 1

# name your resulting data file here!!
FILENAME = "your_font.csv"


# defining color palette
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (10, 255, 10)
GRAY = (200, 200, 200)
RED = (200, 15, 15)


screen = pygame.display.set_mode((400, SCREEN_DIM))
pygame.display.set_caption("8-bit Font Creator")
font = pygame.font.SysFont("monospace", 20)

grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
font_library = {}
current_char = ""
is_drawing = False
draw_mode = 1

# csv handling
def save_to_csv():
    global grid, current_char
    if not current_char:
        print("Please name your character first!")
        return
    

    hex_values = []
    for row in grid:
        bits = "".join(map(str, row))
        hex_values.append(hex(int(bits, 2)))
    
    row_data = [current_char] + hex_values

    file_exists = os.path.isfile(FILENAME)
    with open(FILENAME, mode='a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(['Char', 'B0', 'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7'])
        writer.writerow(row_data)
        
        print(f"Saved '{current_char}' to {FILENAME}: {hex_values}")
        
        grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        current_char = ""

def clear_grid():
    global grid, current_char
    grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    current_char = ""

running = True
while running:
    screen.fill(BLACK)
    
    # top right buttons
    save_rect = pygame.Rect(210, 10, 180, 40)
    clear_rect = pygame.Rect(210, 60, 180, 40)
    pygame.draw.rect(screen, GREEN, save_rect)
    pygame.draw.rect(screen, RED, clear_rect)
    
    screen.blit(font.render("SAVE & CLEAR", True, BLACK), (225, 20))
    screen.blit(font.render("DISCARD/RESET", True, WHITE), (225, 70))
    
    # text inputs
    pygame.draw.rect(screen, WHITE, [10, 35, 180, 40], 2)
    screen.blit(font.render(f"Char: {current_char}", True, WHITE), (20, 45))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                current_char = current_char[:-1]
            elif len(current_char) < 2 and event.unicode.isprintable():
                current_char += event.unicode

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            
            if save_rect.collidepoint(pos):
                save_to_csv()
            elif clear_rect.collidepoint(pos):
                clear_grid()
            else:
                # dragging handling
                col, row = pos[0] // CELL_SIZE, (pos[1] - GRID_OFFSET_Y) // CELL_SIZE
                if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
                    is_drawing = True
                    # if you click a blank spot, you paint. if you click a green spot, you erase.
                    draw_mode = 1 if grid[row][col] == 0 else 0
                    grid[row][col] = draw_mode

        if event.type == pygame.MOUSEBUTTONUP:
            is_drawing = False

        if event.type == pygame.MOUSEMOTION and is_drawing:
            pos = pygame.mouse.get_pos()
            col, row = pos[0] // CELL_SIZE, (pos[1] - GRID_OFFSET_Y) // CELL_SIZE
            if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
                grid[row][col] = draw_mode

    # drawing the grid
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            color = GREEN if grid[r][c] == 1 else WHITE
            pygame.draw.rect(screen, color, 
                             [c * CELL_SIZE + MARGIN, r * CELL_SIZE + MARGIN + GRID_OFFSET_Y, 
                              CELL_SIZE - MARGIN*2, CELL_SIZE - MARGIN*2])
            
    pygame.display.flip()

pygame.quit()