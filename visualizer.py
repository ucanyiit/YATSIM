import sys
import time

import pygame

from yatsim.cell_element import Direction
from yatsim.game_grid import GameGridWithTrains

BLOCK_SIZE = 64
WINDOW_HEIGHT = 640
WINDOW_WIDTH = 640
GAME_GRID: GameGridWithTrains = None
SCREEN = None
CLOCK = None


def start_visualizer(game_grid: GameGridWithTrains, speed: float):
    """Visualizes the game grid using an endless loop."""
    global SCREEN, CLOCK, GAME_GRID, WINDOW_HEIGHT, WINDOW_WIDTH
    pygame.init()
    GAME_GRID = game_grid
    WINDOW_HEIGHT = GAME_GRID.height * BLOCK_SIZE
    WINDOW_WIDTH = GAME_GRID.width * BLOCK_SIZE
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    CLOCK = pygame.time.Clock()

    while True:
        draw_grid()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()
        time.sleep(speed)

        GAME_GRID.move_trains()


def load_image(category: str, category_type: int, orientation: Direction):
    """Loads the image for the train/cell and rotates it"""
    path = f"assets/{category}s/type{category_type}.png"
    cell = pygame.image.load(path).convert_alpha()
    cell = pygame.transform.scale(cell, (BLOCK_SIZE, BLOCK_SIZE))
    cell = pygame.transform.rotate(cell, 90 * orientation)
    return cell


def draw_grid():
    """Updates and draws the given grid."""
    GAME_GRID.update_view()
    display = GAME_GRID.display()

    # Draw the new cell elements
    for y in range(0, GAME_GRID.height):
        for x in range(0, GAME_GRID.width):
            cell_type, orientation = display[y][x]
            image = load_image("cell", cell_type, orientation)
            SCREEN.blit(image, (x * BLOCK_SIZE, y * BLOCK_SIZE))

    # Draw trains on the grid
    for train in GAME_GRID.trains:
        wagoons = train.get_geometry()
        for (x, y, train_type, orientation) in wagoons:
            image = load_image("train", train_type, orientation)
            SCREEN.blit(image, (x * BLOCK_SIZE, y * BLOCK_SIZE))
