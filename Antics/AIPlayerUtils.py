import random
from Constants import *

#
# AIPlayerUtils.py
#
# a set of methods that are likely to be handy for all kinds of AI
# players

##
# legalCoord
#
# determines whether a given coordinate is legal or not
#
#Parameters:
#   coord        - an x,y coordinate
#
# Return: true (legal) or false (illegal)
def legalCoord(coord):

    #make sure we have a tuple or list with two elements in it
    try:
        if (len(coord) != 2):
            return false;
    except TypeError:
        print "ERROR:  parameter to legalCoord was not a tuple or list"
        raise

    x = coord[0]
    y = coord[1]
    return ( (x >= 0) and (x <= 9) and (y >= 0) and (y <= 9))



##
# listAdjacent
#
# Parameters:
#     coord    - a tuple containing a valid x,y coordinate
#     reqEmpty - if 'true' listAdjacent will skip cells that are occupied
#
# Return: a list of all legal coords that are adjacent to the given space
#
def listAdjacent(coord):
    #catch invalid inputs
    if (not legalCoord(coord)):
        return result;

    #this set of coord deltas represent movement in each cardinal direction
    deltas = [ (-1, 0), (1, 0), (0, -1), (0, 1) ]
    x = coord[0]
    y = coord[1]
    result = []

    #calculate the cost after making each move
    for delta in deltas:
        newX = delta[0] + coord[0]
        newY = delta[1] + coord[1]

        #skip illegal moves
        if (not legalCoord((newX, newY))):
            continue

        result.append((newX, newY))

    return result



##
# listReachableAdjacent
#
# calculates all the adjacent cells that can be reached from a given coord.
#
# Parameters:
#    currentState - current game state
#    coords       - where the ant is
#    movement     - movement points ant has
#
# Return:  a list of coords (tuples)   
def listReachableAdjacent(currentState, coords, movement):
    #build a list of all adjacent cells
    oneStep = listAdjacent(coords)

    #winnow the list based upon cell contents and cost to reach
    candMoves = []
    for cell in oneStep:
        loc = currentState.board[cell[0]][cell[1]]
        if (loc.ant == None) and (loc.getMoveCost() <= movement):
            candMoves.append(cell)

    return candMoves



##
# listAllMovementPaths              <!-- RECURSIVE -->
#
# calculates all the legal paths for a single ant to move from a
# given position on the board.  The ant doesn't actually have to
# be there for this method to return a valid answer.
#
# Parameters:
#    currentState - current game state
#    coords       - where the ant is
#    movement     - movement points ant has remaining
#
# Return: a list of lists of coords (tuples). Each sub-list of tuples is an
# acceptable set of coords for a Move object
def listAllMovementPaths(currentState, coords, movement):
    #base case: ant can't move any further
    if (movement <= 0): return []

    #construct a list of all valid one-step moves
    adjCells = listReachableAdjacent(currentState, coords, movement)
    oneStepMoves = []
    for cell in adjCells:
        oneStepMoves.append([coords, cell])

    #add those as valid moves
    validMoves = list(oneStepMoves)

    #recurse for each adj cell to see if we can take additional steps
    for move in oneStepMoves:
        #get a list of all moves that will extend this one
        moveCoords = move[-1]
        cost = currentState.board[moveCoords[0]][moveCoords[1]].getMoveCost()
        extensions = listAllMovementPaths(currentState, moveCoords, movement - cost)

        #create new moves by adding each extension to the base move
        for ext in extensions:
            newMove = list(move)      #create a clone
            for cell in ext[1:]:      #start at index '1' to skip overlap
                newMove.append(cell)
            validMoves.append(newMove)

    return validMoves


##
# stepsToReach
#
# estimates the shortest distance between two cells taking
# movement costs into account.
#
#Parameters:
#   currentState   - The state of the game (GameState)
#   src            - starting position (an x,y coord)
#   dst            - destination position (an x,y coord)
#
# Return: the costs in steps (an integer) or -1 on invalid input
def stepsToReach(currentState, src, dst):
    #check for invalid input
    if (not legalCoord(src)): return -1
    if (not legalCoord(dst)): return -1

    #a dictionary of already visted cells and the corresponding cost to reach
    visited = { src : 0 }
    #a list of to be processed cells
    queue = [ src ]

    #this loops processes cells in the queue until it is empty
    while(len(queue) > 0):
        cell = queue.pop(0)

        #if this cell is our destination we are done
        if (cell == dst):
            return visited[cell]

        #calc distance to all cells adj to this one assuming we reach them
        #from this one
        nextSteps = listAdjacent(cell)
        for newCell in nextSteps:
            dist = visited[cell] + currentState.board[newCell[0]][newCell[1]].getMoveCost()

            #if the new distance is best so far, update the visited dict
            if (visited.has_key(newCell)):
                if (dist < visited[newCell]):
                    visited[newCell] = dist
            #if we've never seen this cell before also update dict and
            #enqueue this new cell to be processed at a future loop iteration
            else:
                visited[newCell] = dist
                queue.append(newCell)

    #we should never reach this point
    return -1

##
# returns a reference the inventory of the player whose turn it is in
# the given state
def getCurrPlayerInventory(currentState):
    #Get my inventory
    resultInv = None
    for inv in currentState.inventories:
        if inv.player == currentState.whoseTurn:
            resultInv = inv
            break
        
    return resultInv
    
##
# getCurrPlayerQueen
#
# Return: a reference to the player's queen
def getCurrPlayerQueen(currentState):
    #find the queen
    queen = None
    for inv in currentState.inventories:
        if inv.player == currentState.whoseTurn:
            queen = inv.getQueen()
            break
    return queen
    
##
# getAntList()
#
# builds a list of all ants on the board that meet a given specification
#
# Parameters:
#     currentState - curr game state
#     pid   - all ants must belong to this player id.  Pass None to
#             indicate any player
#     types - a tuple of all the ant types wanted (see Constants.py)
#
def getAntList(currentState,
               pid = -3,
               types = (QUEEN, WORKER, DRONE, SOLDIER, R_SOLDIER) ):

    #start with a list of all ants that belong to the indicated player(s)
    allAnts = []
    for inv in currentState.inventories:
        if (pid == None) or (pid == inv.player):
            allAnts += inv.ants

    #fill the result with ants that are of the right type
    result = []
    for ant in allAnts:
        if ant.type in types:
            result.append(ant)

    return result
        
