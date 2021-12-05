"""Type 3 and 4 (Y intersection) Test"""

from typing import List

from visualizer import start_visualizer
from yatsim.cell import cell_factory
from yatsim.cell.cell_element import CellElement, Direction
from yatsim.cell.cell_factory import SimpleTimedCellFactory
from yatsim.game_grid import GameGridWithTrains
from yatsim.train import Train

grid = GameGridWithTrains(5, 5)

cell_factory: SimpleTimedCellFactory = SimpleTimedCellFactory()

cells: List[CellElement] = []
cells.append(cell_factory.rotated_new(2, 0, 1, 0))
cells.append(cell_factory.rotated_new(2, 1, 3, 0))
cells.append(cell_factory.rotated_new(2, 2, 8, 0))
cells.append(cell_factory.rotated_new(2, 3, 4, 2))
cells.append(cell_factory.rotated_new(2, 4, 1, 0))

cells.append(cell_factory.rotated_new(3, 1, 1, 1))
cells.append(cell_factory.rotated_new(4, 1, 1, 1))

cells.append(cell_factory.rotated_new(3, 3, 1, 1))
cells.append(cell_factory.rotated_new(4, 3, 1, 1))

cells[1].switch_state()
cells[3].switch_state()

for cell in cells:
    grid.add_element(cell, cell.x, cell.y)

trains: List[Train] = []
trains.append(Train(1, 2, cells[-1]))
trains.append(Train(0, 2, cells[0]))

for train in trains:
    grid.add_train(train)

start_visualizer(grid, 1)
