from Constants import *
from Inventory import Inventory
from Building import Building
##
#GameState
#Description: The current state of the game.
#
#Variables:
#   board - The game Board being used.
#   inventories - A tuple containing the Inventory for each player.
#   phase - The current phase of the game.
#    whoseTurn - The ID of the Player who's turn it currently is.
##
class GameState(object):

    ##
    #__init__
    #Description: Creates a new GameState
    #
    #Parameters:
    #   inputBoard - The Board to be used by the GameState (Board)
    #   inputInventories - A tuple containing the Inventory for each player ((Inventory, Inventory))
    #   inputPhase - The phase of the game (int)
    #   inputTurn - The ID of the Player who's turn it is (int)
    ##
    def __init__(self, inputBoard, inputInventories, inputPhase, inputTurn):
        self.board = inputBoard
        self.inventories = inputInventories
        self.phase = inputPhase
        self.whoseTurn = inputTurn

    ##
    #applyMove
    #Description: Makes the required changes to the GameState based off of the given move
    #
    #Parameters:
    #   inputMove - The move to make (Move)
    ##
    def applyMove(self, inputMove):
        fromX = fromLoc.getCoords()[0]
        fromY = fromLoc.getCoords()[1]

        toX = toLoc.getCoords()[0]
        toY = toLoc.getCoords()[1]
        
        tempAnt = self.board[fromX][fromY].getAnt()

        tempAnt.coords = ToLoc.getCoords()
        self.board[fromX][fromY].ant = None
        self.board[toX][toY].ant = tempAnt

    ##
    #coordLookup
    #Description: Returns the appropriate coordinates for the given
    #   player to allow both players to play from top of the board.
    #
    #Return: Correct coordinate location for player
    ##
    def coordLookup(self, coords, player):
        if player == PLAYER_ONE:
            return coords
        else:
            return (BOARD_LENGTH - 1 - coords[0], BOARD_LENGTH - 1 - coords[1])
    
    ##
    #flipBoard
    #Description: Flips the board (so Player Two sees self on top side)
    #
    ##
    def flipBoard(self):
        for col in self.board:
            col.reverse()
            
        self.board.reverse()
        
        for col in self.board:
            for loc in col:
                if loc.ant != None:
                    loc.ant.coords = self.coordLookup(loc.ant.coords, PLAYER_TWO)
                if loc.constr != None:
                    loc.constr.coords = self.coordLookup(loc.constr.coords, PLAYER_TWO)
    ##
    #clone
    #Description: Returns a deep copy of itself
    #
    #Return: The GameState identical to the original
    ##
    def clone(self):
        newBoard = []
        ants1 = []
        ants2 = []
        cons1 = []
        cons2 = []
        food1 = self.inventories[PLAYER_ONE].foodCount
        food2 = self.inventories[PLAYER_TWO].foodCount
        for col in xrange(0,len(self.board)):
            newBoard.append([])
            for row in xrange(0,len(self.board)):
                newLoc = self.board[col][row].clone()
                newBoard[col].append(newLoc)
                #Organize constructions into inventories
                if newLoc.constr != None and type(newLoc.constr) is Building and newLoc.constr.player == PLAYER_ONE:
                    cons1.append(newLoc.constr)
                elif newLoc.constr != None and type(newLoc.constr) is Building and newLoc.constr.player == PLAYER_TWO:
                    cons2.append(newLoc.constr)
                #Organize ants into inventories
                if newLoc.ant != None and newLoc.ant.player == PLAYER_ONE:
                    ants1.append(newLoc.ant)
                elif newLoc.ant != None and newLoc.ant.player == PLAYER_TWO:
                    ants2.append(newLoc.ant)
        #newBoard = [[self.board[row][col].clone() for col in xrange(0,len(self.board))] for row in xrange(0,len(self.board))]
        newInventories = [Inventory(PLAYER_ONE, ants1, cons1, food1), Inventory(PLAYER_TWO, ants2, cons2, food2)]
        return GameState(newBoard, newInventories, self.phase, self.whoseTurn)