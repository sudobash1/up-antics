class Building(Construction):
	def __init__(self,inputId,inputCoords, inputType, inputPlayer, inputHealth):
                super(Building,self).__init__(inputId,inputCoords)
		self.type = inputType
		self.player = inputPlayer
		self.captureHealth = inputHealth		
	
	
	
