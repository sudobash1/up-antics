class Location:
	def __init__(self, passable, moveCost, coordinates):
		self.isPassable = passable
		self.movementCost = moveCost
		self.ant = None
		self.constr = None
		self.coords = coordinates
	def getAnt(self):
		return self.ant
	def getCoords(self):
		return self.coords
	def getConstr(self):
		return self.constr
	def getMovementCost(self):
		return self.movementCost
	def setAnt(self, addAnt):
		self.ant = addAnt
	def setConstr(self, addConstr):
		self.constr = addConstr  

