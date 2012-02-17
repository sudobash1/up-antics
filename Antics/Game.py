##
#Game
#Description: Keeps track of game logic and manages the play loop.
##
class Game:
	def __init__(self
		self.players
		self.state
		self.mode
		self.ui
		self.scores
		
	def runGame(self
		# initialize board, draw start menu, be ready for player input for game parameters
		
		# *player clicks start game* enter game loop
		
		# once end game has been reached, display screen "player x wins!" OK/Play Again button
		
		
	def isGameOver(self, inputPlayer):
		if (self.state.inventories[inputPlayer].queen.isAlive == False) or 
			(self.state.inventories[(inputPlayer + 1) % 2].antHill.captureHealth == 0) or
			(self.state.inventories[inputPlayer].foodCount == 11):
			return True
		else:
			return False
			
	def isValidMove(self, inputMove, inputPlayer):
		if (inputMove.fromLoc.coords[0] < 10) and 
			(inputMove.fromLoc.coords[0] >= 0) and 
			(inputMove.fromLoc.coords[1] < 10) and 
			(inputMove.fromLoc.coords[1] >= 0) and 
			(inputMove.toLoc.coords[0] < 10) and 
			(inputMove.toLoc.coords[0] >= 0) and 
			(inputMove.toLoc.coords[1] < 10) and 
			(inputMove.toLoc.coords[1] >= 0) and 
			(inputMove.fromLoc.ant.player == inputPlayer) and
			(inputMove.toLoc.ant == None) 
			
		
	
	def isValidAttack(self
	
			
		
		
		
	