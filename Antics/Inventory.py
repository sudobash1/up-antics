class Inventory:
	def init(self, playerId, antArray, food):
		self.player = playerId
		self.ants = antArray
		self.foodCount = food
	def getPlayer(self):
		return self.player
	def getAnt(self, antId):
		return self.ants[antId]
	def getFoodCount(self):
		return self.foodCount
	def updateFoodCount(self, change):
		self.foodCount = self.foodCount + change