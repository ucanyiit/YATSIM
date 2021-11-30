# This class contains the cell elements edited by the user.

from CellElement import BackgroundCellElement

class GameGrid:
  
  # Creates a grid
  def __init__(self, height, width):
    self.height = height
    self.width = width
    self.elements = [[BackgroundCellElement for _ in range(width)] for _ in range(height)]
    self.view = [[self.elements[i][j].getView() for j in range(width)] for i in range(height)]

  # update cell element, overwrite with the given element
  def addElement(self, cellel, x, y):
    self.elements[x][y] = cellel

  # Replace element at the given coordinates with background element
  def removeElement(self, x, y):
    self.elements[x][y] = BackgroundCellElement

  # Call when the model is changed so the views are informed
  def updateView(self):
    self.view = [[self.elements[i][j].getView() for j in range(self.width)] for i in range(self.height)]
    
  # Return a display representation of the current grid. In early phases it can be a textual representation, last phases will return a printable information
  def display(self):
    lines = [''.join(self.view[i]) for i in range(self.height)]
    return '\n'.join(lines)

  # Start the simulation of game
  def startSimulation(self):
    pass

  # pause/resume the simulation
  def setPauseResume(self):
    pass

  # Stop the simulation
  def stopSimulation(self):
    pass
