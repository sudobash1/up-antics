##
#Location
#Description: This class represents all valid locations on the board
#
#Variables 
#   isPassable - A boolean to indicate whether an Ant can move through this location
#   movementCost - The cost of moving through this location 
#   ant - The ant found at this location
#   constr - The construction found at this location 
#   coords - The coordinates of this location
##
class Location:
	def __init__(self, inputPassable, inputMoveCost, inputCoordinates):
		self.isPassable = inputPassable
		self.movementCost = inputMoveCost
		self.ant = None
		self.constr = None
		self.coords = inputCoordinates
