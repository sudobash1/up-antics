class Location:
	def __init__(self, inputPassable, inputMoveCost, inputCoordinates):
		self.isPassable = inputPassable
		self.movementCost = inputMoveCost
		self.ant = None
		self.constr = None
		self.coords = inputCoordinates
