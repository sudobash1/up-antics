##
#Game
#Description: Keeps track of game logic and manages the play loop.
##
PLAYER_ONE = 0;
PLAYER_TWO = 1;

class Game:
	def __init__(self
		self.players
		self.state
		self.mode
		self.ui
		self.scores
		
	def runGame(self
		# initialize board, draw start menu, be ready for player input for game parameters
		
		#assign first player
		
		# *player clicks start game* enter game loop
		while !isGameOver(PLAYER_ONE) and !isGameOver(PLAYER_TWO):
			#check what type first player is
				#get move(list of locs) from first player until end turn is submitted
				#If computer player, check validMove 
				#check if player wants to attack
				#check isGameOver. If so, break
			#check what type second player is 
				#get move(list of locs) from second until end turn is submitted 
				#If computer player, check ValidMove
				#check if player wants to attack 
				#check isGameOver If so, break 
			
			
				
			
		
		# once end game has been reached, display screen "player x wins!" OK/Play Again button
		
		
	def isGameOver(self, playerId):
		opponentId = (playerId + 1) % 2
		
		if (self.state.inventories[playerId].queen.isAlive == False) or 
			(self.state.inventories[opponentId].antHill.captureHealth <= 0) or
			(self.state.inventories[playerId].foodCount >= 11):
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
	
			
		
		
		
	