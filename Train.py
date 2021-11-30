# Trains are generated only during the simulation. They disappear (destructed) when they go out of the grid. Also you can implement a blocking cell type that reverses trains direction. Each car and engine of the train has 1/2 cell length. 2 cars fit in a single cell where the others follow from behind. You can limit train length to be 4 or 6.

# There are two options to introduce trains in the simulation: Adding trains in the Grid with appropriate methods, or adding train parks that dynamically add trains during simulation. You are expected to implement simulation part in second and later phases.

class Train:

  # Creates a train at given cell with given number of cars behind. The total size of train is ncars+1 including the engine.
  def __init__(self, type, ncars, cell):
    self.type = type
    self.ncars = ncars
    self.cell = cell

  # Get the train engine the given cell
  def enterCell(self, cell):
    pass

  # The train status can be moving/moving reverse/stopped.
  def getStatus(self):
    pass

  # Gets the geometry of the train path, engine and cars. Implemented in later phases where full train needs to be displayed on a curve during simulation
  def getGeometry(self):
    pass


# Multiple grids
# In first phase only one grid is sufficient but in following phases you need to have multiple grids that can be attached by multiple users so they collaborate.

