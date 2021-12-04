import sys
import time

import pygame

from yatsim.cell_element import Direction, StatefulCell
from yatsim.game_grid import GameGridWithTrains
from yatsim.train import Train

BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
BLOCK_SIZE = 64
WINDOW_HEIGHT = 640
WINDOW_WIDTH = 640
GAME_GRID: GameGridWithTrains = None
SCREEN = None
CLOCK = None


def main(game_grid: GameGridWithTrains):
    global SCREEN, CLOCK, GAME_GRID, WINDOW_HEIGHT, WINDOW_WIDTH
    pygame.init()
    GAME_GRID = game_grid
    WINDOW_HEIGHT = GAME_GRID.height * BLOCK_SIZE
    WINDOW_WIDTH = GAME_GRID.width * BLOCK_SIZE
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    CLOCK = pygame.time.Clock()
    SCREEN.fill(BLACK)

    while True:
        draw_grid()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()
        time.sleep(2)

        GAME_GRID.move_trains()


def load_image(category: str, category_type: int, orientation: Direction):
    path = f"assets/{category}s/type{category_type}.png"
    cell = pygame.image.load(path).convert_alpha()
    cell = pygame.transform.scale(cell, (BLOCK_SIZE, BLOCK_SIZE))
    cell = pygame.transform.rotate(cell, 90 * orientation)
    return cell


def draw_grid():
    GAME_GRID.update_view()
    display = GAME_GRID.display()

    for y in range(0, GAME_GRID.height):
        for x in range(0, GAME_GRID.width):
            cell_type, orientation = display[y][x]
            image = load_image("cell", cell_type, orientation)
            SCREEN.blit(image, (x * BLOCK_SIZE, y * BLOCK_SIZE))

    for train in GAME_GRID.trains:
        wagoons = train.get_geometry()
        for (x, y, train_type, orientation) in wagoons:
            image = load_image("train", train_type, orientation)
            SCREEN.blit(image, (x * BLOCK_SIZE, y * BLOCK_SIZE))


test_grid_1 = GameGridWithTrains(5, 5)

test_grid_1.add_element(StatefulCell(1, 1), 1, 1)
test_grid_1.add_element(StatefulCell(1, 2), 1, 2)
test_grid_1.add_element(StatefulCell(1, 3), 1, 3)
test_grid_1.add_element(StatefulCell(1, 4), 1, 4)
test_grid_1.add_element(StatefulCell(3, 1), 3, 1)
test_grid_1.add_element(StatefulCell(3, 2), 3, 2)
test_grid_1.add_element(StatefulCell(3, 3), 3, 3)
test_grid_1.add_element(StatefulCell(3, 4), 3, 4)

train_1: Train = Train(0, 2, StatefulCell(1, 4))
train_2: Train = Train(1, 2, StatefulCell(3, 4))

test_grid_1.add_train(train_1)
test_grid_1.add_train(train_2)

main(test_grid_1)
