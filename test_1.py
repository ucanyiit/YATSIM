from visualizer import start_visualizer
from yatsim.cell_element import StatefulCell
from yatsim.game_grid import GameGridWithTrains
from yatsim.train import Train

grid = GameGridWithTrains(5, 5)

grid.add_element(StatefulCell(1, 1), 1, 1)
grid.add_element(StatefulCell(1, 2), 1, 2)
grid.add_element(StatefulCell(1, 3), 1, 3)
grid.add_element(StatefulCell(1, 4), 1, 4)
grid.add_element(StatefulCell(3, 1), 3, 1)
grid.add_element(StatefulCell(3, 2), 3, 2)
grid.add_element(StatefulCell(3, 3), 3, 3)
grid.add_element(StatefulCell(3, 4), 3, 4)

train_1: Train = Train(0, 2, StatefulCell(1, 4))
train_2: Train = Train(1, 2, StatefulCell(3, 4))

grid.add_train(train_1)
grid.add_train(train_2)

start_visualizer(grid)
