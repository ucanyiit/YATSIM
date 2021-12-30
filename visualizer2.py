from typing import List, Tuple

import pygame

from yatsim.cell import Direction


class Visualizer:
    def __init__(self, height: int, width: int, view: List[List[str]]):
        """Visualizes the game grid using an endless loop."""
        pygame.init()
        self.block_size = 64
        self.height = height
        self.width = width
        self.window_height = height * self.block_size
        self.window_width = width * self.block_size
        self.view = view
        self.trains = []
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        self.clock = pygame.time.Clock()

    def load_image(self, category: str, category_type: int, orientation: Direction):
        """Loads the image for the train/cell and rotates it"""
        path = f"assets/{category}s/type{category_type}.png"
        cell = pygame.image.load(path).convert_alpha()
        cell = pygame.transform.scale(cell, (self.block_size, self.block_size))
        cell = pygame.transform.rotate(cell, -90 * orientation)
        return cell

    def _draw_cell(self, x: int, y: int):
        cell_type, orientation = self.view[y][x]
        image = self.load_image("cell", cell_type, orientation)
        self.screen.blit(image, (x * self.block_size, y * self.block_size))

    def _draw(self):
        """Draws the grid."""

        # Draw the new cell elements
        for y in range(0, self.height):
            for x in range(0, self.width):
                self._draw_cell(x, y)

        # Draw trains on the grid
        for train in self.trains:
            (x, y, train_type, orientation) = train
            image = self.load_image("train", train_type, orientation)
            self.screen.blit(image, (x * self.block_size, y * self.block_size))

    def update_cell(self, x: int, y: int, view: Tuple[int, int]):
        self.view[y][x] = view
        self._draw()

    def update_trains(self, trains: List[Tuple[int, int, int, int]]):
        """Updates and draws the given trains list."""
        self.trains = trains
        self._draw()

    def update(self):
        pygame.display.update()
        self.draw_grid()
