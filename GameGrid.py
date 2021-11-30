# This class contains the cell elements edited by the user.

class GamerGrid:
  
  # Creates a grid
  def __init__(height, width):
    pass

  # update cell element, overwrite with the given element
  def addElement(cellel, x, y):
    pass	

  # Replace element at the given coordinates with background element
  def removeElement(x, y):
    pass

  # Call when the model is changed so the views are informed
  def updateView():
    pass

  # Return a display representation of the current grid. In early phases it can be a textual representation, last phases will return a printable information
  def display():
    pass

  # Start the simulation of game
  def startSimulation():
    pass

  # pause/resume the simulation
  def setPauseResume():
    pass

  # Stop the simulation
  def stopSimulation():
    pass
