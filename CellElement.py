# This class determines how each cell in the game grid behaves.

class CellElement:
  
  # Put element in the position x, y
  def setPosition(self, x, y):
    self.x = x
    self.y = y

  # The elements can have one of 4 orientation, based on how many times they are rotated clockwise	
  def setOrientation(self, a):
    self.orientation = a % 4

	# As elements get clicked they switch to next state. This is useful in railroad switches to set which way train shall go
  def switchState(self):
    pass

	# It returns the expected delay of the train engine while passing this cell. It is the the time interval between train engine enters the cell and leaves the cell. The train is assumed to be moving in this period (unless it stops).
  def getDuration(self, entdir):
    pass

	# It returns the expected stop duration of the train engine on this cell, typically a train station. Engine stops for this while (in the middle of Duration) and continues afterwards.
  def getStop(self, entdir):
    pass

	# Based on the incoming direction of a train entering this cell, it returns the next cell for train to follow. It returns the new direction. For static cells it is fixed, for switches it depends on the current state.
  def nextCell(self, entdir):
    pass

	# return the URI storing how cell is displayed. In early phases, it is textual, later it will be an image
  def getView(self):
    pass

# The following are some cell types: [image]

# Three of them are examples of railroad switches, if a train enters from SOUTH it can continue in alternative directions. 
# The others have fixed next position. The cell elements can be placed in one of 4 different orientations. For example element making a right turn can be rotated 3 times to make it left turn, or rotate twice to make a west to north turn. You can choose to implement train park element type that generates trains during the simulation.

class BackgroundCellElement(CellElement):
  def getView(self):
      return '#'
