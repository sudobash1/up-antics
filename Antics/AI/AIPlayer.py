import random
from Player import *
import Constants as const
from Construction import CONSTR_STATS
from Ant import UNIT_STATS
from Move import Move
from UserInterface import addCoords
##
#AIPlayer
#Description: The responsbility of this class is to interact with the game by
#deciding a valid move based on a given game state. This class has methods that
#will be implemented by students in Dr. Nuxoll's AI course.
#
#Variables:
#   playerId - The id of the player.
##
class AIPlayer(Player):

    #__init__
    #Description: Creates a new Player
    #
    #Parameters:
    #   inputPlayerId - The id to give the new player (int)
    ##
    def __init__(self, inputPlayerId):
        super(AIPlayer,self).__init__(inputPlayerId)
        self.author = "Mooooonk! I need a monk!"
    
    ##
    #getPlacement
    #Description: called during setup phase for each Construction that must be placed by the player.
    #   These items are: 1 Anthill on the player's side; 9 grass on the player's side; and 2 food on the enemy's side.
    #
    #Parameters:
    #   construction - the Construction to be placed.
    #   currentState - the state of the game at this point in time.
    #
    #Return: The coordinates of where the construction is to be placed
    ##
    def getPlacement(self, construction, currentState):
        #implemented by students to return their next move
        if construction.type == const.ANTHILL or construction.type == const.GRASS:
            move = None
            while move == None:
                #Choose any x location
                x = random.randint(0, 9)
                #Choose any y location on your side of the board
                y = random.randint(0, 3)
                #Set the move if this space is empty
                if currentState.board[x][y].constr == None:
                    move = (x, y)
            return move
        elif construction.type == const.FOOD:
            move = None
            while move == None:
                #Choose any x location
                x = random.randint(0, 9)
                #Choose any y location on enemy side of the board
                y = random.randint(6, 9)
                #Set the move if this space is empty
                if currentState.board[x][y].constr == None:
                    move = (x, y)
            return move
        else:
            return (0, 0)
    
    ##
    #getMove
    #Description: Gets the next move from the Player.
    #
    #Parameters:
    #   currentState - The state of the current game waiting for the player's move (GameState)
    #
    #Return: The Move to be made
    ##
    def getMove(self, currentState):
        #Get my inventory
        myInv = None
        for inv in currentState.inventories:
            if inv.player == self.playerId:
                myInv = inv
                break
        #If my inventory is still none, then I don't have one.
        if myInv == None:
            return None
        #If you have the food for an ant tunnel, try to purchase something random.
        if myInv.foodCount >= CONSTR_STATS[TUNNEL][COST]:
            #First detect whether you have an ant with nothing under it
            placeableAnts = []
            for ant in myInv.ants:
                if currentState.board[ant.coords[0]][ant.coords[1]].constr == None:
                    placeableAnts.append(ant)
            #Then detect whether you have an anthill with nothing on top of it
            placeableHill = False
            hill = myInv.getAnthill()
            if currentState.board[hill.coords[0]][hill.coords[1]].ant == None:
                placeableHill = True
            #Choose randomly between building ants or tunnels
            if len(placeableAnts) != 0 and placeableHill:
                #randint returns up to the max, so no need to add or subtract for placeableHill's sake
                toPlace = random.randint(0, 5)
                if toPlace == 5:
                    #build a tunnel
                    location = random.randint(0, len(placeableAnts) - 1)
                    return Move(BUILD, location, TUNNEL)
                else:
                    #build an ant
                    return Move(BUILD, hill.coords, random.randint(QUEEN, I_SOLDIER))
            elif len(placeableAnts) != 0:
                #build a tunnel
                location = random.randint(0, len(placeableAnts) - 1)
                return Move(BUILD, location, TUNNEL)
            elif placeableHill:
                #build an ant
                return Move(BUILD, hill.coords, random.randint(QUEEN, I_SOLDIER))
            else:
                #I have resources to build, but no place to build things
                pass
        #See if you can move any ants
        antsToMove = []
        for ant in myInv:
            if not ant.hasMoved:
                antsToMove.append(ant)
        #Move first of these ants
        if antsToMove != []:
            chosen = antsToPlace[0]
            coordList = [chosen.coords]
            totalCost = 0
            lastStep = None
            while totalCost < UNIT_STATS[chosen.type][MOVEMENT]:
                #pick a random direction that won't move me back.
                possibleDirections = [(0, 1), (0, -1), (1, 0), (-1, 0)]
                validDirections = []
                for direction in possibleDirections:
                    nextLoc = addCoords(coordList[-1], direction)
                    costOfStep = currentState.board[nextLoc.coords[0]][nextLoc.coords[1]].getMoveCost()
                    if UNIT_STATS[chosen.type][MOVEMENT] >= totalCost + costOfStep:
                        validDirections.append(direction)
                #If no directions are valid, break out of the loop.
                if validDirections == []:
                    break
                else:
                    #Choose a random direction
                    randDir = random.randint(0, len(validDirections) - 1)
                    #Apply it
                    nextLoc = addCoords(chosen.coords, validDirections[randDir])
                    coordList.append(nextLoc)
                    #Add its cost to the total move cost
                    totalCost += currentState.board[nextLoc.coords[0]][nextLoc.coords[1]].getMoveCost()
            #Return the chosen move
            return Move(MOVE, coordList, None)
        #If I can't to anything, end turn
        return Move(END, None, None)
    
    ##
    #getAttack
    #Description: Gets the attack to be made from the Player
    #
    #Parameters:
    #   enemyLocation - The Locations of the Enemies that can be attacked (Location[])
    ##
    def getAttack(self, enemyLocations):
        #Attack a random enemy.
        return random.randint(0, len(enemyLocations) - 1)