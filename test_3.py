"""Cross Junction X (Type 5) Test

  2 trains in a loop which follow each other.
"""

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

cells.append(cell_factory.rotated_new(2, 0, 1, 0))
cells.append(cell_factory.rotated_new(2, 1, 1, 0))
cells.append(cell_factory.rotated_new(2, 2, 5, 0))
cells.append(cell_factory.rotated_new(2, 3, 1, 0))
cells.append(cell_factory.rotated_new(2, 4, 1, 0))

cells.append(cell_factory.rotated_new(0, 2, 1, 1))
cells.append(cell_factory.rotated_new(1, 2, 1, 1))

cells.append(cell_factory.rotated_new(3, 2, 1, 1))
cells.append(cell_factory.rotated_new(4, 2, 1, 1))


# The train goes directly to North in the default case
# The train will go to West when you switch the state once
# The train will go to East when you switch the state twice

cells[2].switch_state()
cells[2].switch_state()

for cell in cells:
    grid.add_element(cell, cell.x, cell.y)

trains: List[Train] = []
trains.append(Train(0, 2, cells[0]))
# trains.append(Train(1, 2, cells[7]))

for train in trains:
    grid.add_train(train)

start_visualizer(grid, 1)
