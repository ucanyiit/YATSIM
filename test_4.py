"""Double loop (8) Test"""

from typing import List

from visualizer import start_visualizer
from yatsim.cell import cell_factory
from yatsim.cell.cell_element import CellElement
from yatsim.cell.cell_factory import SimpleTimedCellFactory
from yatsim.game_grid import GameGridWithTrains
from yatsim.train import Train

grid = GameGridWithTrains(5, 5)

cell_factory: SimpleTimedCellFactory = SimpleTimedCellFactory()

cells: List[CellElement] = []

cells.append(cell_factory.rotated_new(2, 2, 7, 0))

cells.append(cell_factory.rotated_new(2, 1, 2, 1))
cells.append(cell_factory.rotated_new(3, 1, 2, 2))
cells.append(cell_factory.rotated_new(3, 2, 2, 3))
cells.append(cell_factory.rotated_new(2, 3, 2, 3))
cells.append(cell_factory.rotated_new(1, 3, 2, 0))
cells.append(cell_factory.rotated_new(1, 2, 2, 1))

for cell in cells:
    grid.add_element(cell, cell.x, cell.y)

trains: List[Train] = []
trains.append(Train(0, 2, cells[1]))
trains.append(Train(1, 2, cells[4]))

for train in trains:
    grid.add_train(train)

start_visualizer(grid, 1)
