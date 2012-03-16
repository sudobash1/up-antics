import os, re, sys, HumanPlayer
from UserInterface import *
from Construction import *
from Constants import *
from GameState import *
from Inventory import *
from Building import *
from Location import *
from Ant import *
from Move import *

##
#Game
#Description: Keeps track of game logic and manages the play loop.
##

class Game(object):
    def __init__(self):
        #BOARDS ARE SQUARE
        board = [[Location((col, row)) for row in xrange(0,BOARD_LENGTH)] for col in xrange(0,BOARD_LENGTH)]
        p1Inventory = Inventory(PLAYER_ONE, [], [], 0)
        p2Inventory = Inventory(PLAYER_TWO, [], [], 0)
        self.state = GameState(board, [p1Inventory, p2Inventory], MENU_PHASE, PLAYER_ONE)
        self.players = []
        self.scores = [0,0]
        self.mode = None
        self.ui = UserInterface((960,750))
        self.ui.initAssets()
        #UI Callback functions
        self.ui.buttons['start'][-1] = self.startGame
        self.ui.buttons['tournament'][-1] = self.tournamentPath
        self.ui.buttons['human'][-1] = self.humanPath
        self.ui.buttons['ai'][-1] = self.aiPath
        self.ui.locationClicked = self.locationClickedCallback
          
    def runGame(self):
        # initialize board be ready for player input for game parameter
        while True:
            self.ui.drawBoard(self.state)
            #Determine current chosen game mode. Enter different execution paths based on the mode, which must be chosen by clicking a button.
            
            #player has clicked start game so enter game loop
            if self.state.phase != MENU_PHASE:
                print "Game Started!"
                #init game stuffs
                #build a list of things to place
                #things to place: 2 anthill/queen, 9 obstacles, 2 food sources (for opponent)
                constrsToPlace = []
                constrsToPlace += [Building(None, ANTHILL, i) for i in xrange(0,2)]
                constrsToPlace += [Construction(None, GRASS) for i in xrange(0,18)]
                constrsToPlace += [Construction(None, FOOD) for i in xrange(0,4)]
                
                while not self.isGameOver(PLAYER_ONE) and not self.isGameOver(PLAYER_TWO):
                    #Draw the board again (to recognize user input in game loop)
                    self.ui.drawBoard(self.state)
                
                    if self.state.phase == SETUP_PHASE:
                        currentPlayer = self.players[self.state.whoseTurn]
                        
                        #if the player is player two, flip the board
                        theState = self.state.clone()
                        if theState.whoseTurn == PLAYER_TWO:
                            theState.flipBoard()
                            
                        #get the placement from the player
                        target = currentPlayer.getPlacement(constrsToPlace[0], theState)
                        validPlace = self.isValidPlacement(constrsToPlace[0], target)
                        if validPlace:
                            #translate coords to match player
                            target = self.state.coordLookup(target, theState.whoseTurn)
                            #get construction to place
                            constr = constrsToPlace.pop(0)
                            #give constr its coords
                            constr.coords = target
                            #put constr on board
                            self.state.board[target[0]][target[1]].constr = constr
                            #update the inventory
                            self.state.inventories[self.state.whoseTurn].constructions.append(constr)
                            #change player turn in actual state
                            self.state.whoseTurn = (self.state.whoseTurn + 1) % 2
                        else:
                            if not type(currentPlayer) is HumanPlayer.HumanPlayer:
                                #exit gracefully
                                exit(0)
                            elif validPlace != None:
                                self.ui.notify("Invalid placement: " + str(target[0]) + ", " + str(target[1]))
                        
                        if not constrsToPlace:
                            #if we're finished placing, add in queens and move to play phase
                            
                            #get anthill coords
                            p1AnthillCoords = self.state.inventories[PLAYER_ONE].getAnthill().coords
                            p2AnthillCoords = self.state.inventories[PLAYER_TWO].getAnthill().coords
                            #create queen ants
                            p1Queen = Ant(p1AnthillCoords, QUEEN, PLAYER_ONE)
                            p2Queen = Ant(p2AnthillCoords, QUEEN, PLAYER_TWO)
                            #put queens on board
                            self.state.board[p1Queen.coords[0]][p1Queen.coords[1]].ant = p1Queen
                            self.state.board[p2Queen.coords[0]][p2Queen.coords[1]].ant = p2Queen
                            #add the queens to the inventories
                            self.state.inventories[PLAYER_ONE].ants.append(p1Queen)
                            self.state.inventories[PLAYER_TWO].ants.append(p2Queen)                           
                            #change to play phase
                            self.state.phase = PLAY_PHASE
                        
                    elif self.state.phase == PLAY_PHASE: ####AT SOMEPOINT PASS VALID ATTACKS TO UI
                        currentPlayer = self.players[self.state.whoseTurn]
                        
                        #if the player is player two, flip the board
                        theState = self.state.clone()
                        if theState.whoseTurn == PLAYER_TWO:
                            theState.flipBoard()
                        
                        #get the move from the current player
                        move = currentPlayer.getMove(theState)
                        
                        if not move == None:
                            move.coordList[0] = self.state.coordLookup(move.coordList[0])
                        
                        #make sure it's a valid move
                        validMove = self.isValidMove(move)
                        
                        #complete the move if valid
                        if validMove:
                            #check move type
                            if move.moveType == MOVE:
                                startCoord = move.coordList[0]
                                endCoord = move.coordList[-1]
                                
                                #take ant from fromLoc
                                antToMove = self.state.board[startCoord[0]][startCoord[1]].ant
                                #change ant's coords and hasMoved status
                                antToMove.coords = (endCoord[0], endCoord[1])
                                antToMove.hasMoved = True
                                #remove ant from location
                                self.state.board[startCoord[0]][startCoord[1]].ant = None
                                #put ant at last loc in locList
                                self.state.board[endCoord[0]][endCoord[1]] = antToMove   
                            elif move.moveType == BUILD:
                                # TODO: finish!!
                                pass
                            elif move.moveType == END:
                                for ant in self.state.inventories[self.state.whoseTurn].ants:
                                    #reset hasMoved on all ants of player
                                    ant.hasMoved = False
                                    #affect capture health of buildings
                                    constrUnderAnt = self.state.board[ant.coords[0]][ant.coords[1]].constr
                                    if type(constrUnderAnt) is Building and not constrUnderAnt.player == self.state.whoseTurn:
                                        constrUnderAnt.captureHealth -= 1
                                        if constrUnderAnt.captureHealth == 0:
                                            constrUnderAnt.player = self.state.whoseTurn
                                            constrUnderAnt.captureHealth = CONSTR_STATS[constrUnderAnt.type][CAP_HEALTH]
                                            
                                #switch whose turn it is
                                self.state.whoseTurn = (self.state.whoseTurn + 1) % 2
                            else:
                                #exit, invalid move type
                                #human can give None move, AI can't
                                pass
                        else:
                            #if move type check if player wants to attack
                            pass
                    else:
                        #something went wrong, exit gracefully
                        pass             
                
    def startGame(self):
        if self.mode != None:
            self.state.phase = SETUP_PHASE
                
    def tournamentPath(self):
        #If already in tournament mode, do nothing. WILL BE CHANGED IN THE FUTURE
        if self.mode == TOURNAMENT_MODE:
            return
        #Attempt to load the AI files
        self.loadAIs()
        #Check right number of players, if successful set the mode.
        if len(self.players) >= 2:
            self.mode = TOURNAMENT_MODE
        self.mode = None # DELETE THIS LINE LATER!!
        
    def humanPath(self):
        #If already in human mode, do nothing.
        if self.mode == HUMAN_MODE:
            return
        #Attempt to load the AI files
        self.loadAIs() 
        #Add the human player to the player list
        self.players.insert(PLAYER_ONE, HumanPlayer.HumanPlayer(len(self.players)))                
        #Check right number of players, if successful set the mode.
        if len(self.players) == 2:
            self.mode = HUMAN_MODE
            self.ui.notify("Mode changed to human")
    
    def aiPath(self):
        #If already in ai mode, do nothing.
        if self.mode == AI_MODE:
            return
        #Attempt to load the AI files
        self.loadAIs()
        #Check right number of players, if successful set the mode.
        if len(self.players) == 2:
            self.mode = AI_MODE
        self.mode = None # DELETE THIS LINE LATER!!
    
    def loadAIs(self):
        #Reset the player list in case some have been loaded already
        self.players = []
        #Attempt to load AIs. Exit gracefully if user trying to load weird stuff.
        filesInAIFolder = os.listdir("AI")
        #Change directory to AI subfolder so modules can be loaded (they won't load as filenames).
        os.chdir('AI')
        #IF WE FOUND A BUG IN PYTHON!!!!
        #Details: changing directory, then importing in python terminal will first check subdirectories for modules.
        #   However, modules will not be foud if this function is used. Does it have to do with it being in a function?
        #Add current directory in python's import search order.
        sys.path.insert(0, os.getcwd())
        #Make player instances from all AIs in folder.
        for file in filesInAIFolder:
            if re.match(".*\.py$", file):
                moduleName = file.rstrip('.py')
                #Check to see if the file is already loaded.
                temp = __import__(moduleName, globals(), locals(), [], -1)
                #If the module has already been imported into this python instance, reload it.
                if temp == None:
                    temp = reload(globals()[moduleName])
                #Create an instance of Player from temp
                self.players.append(temp.AIPlayer(len(self.players)))
        #Remove current directory from python's import search order.
        sys.path.pop(0)
        #Revert working directory to parent.
        os.chdir('..')
    
    def locationClickedCallback(self, coord):
        whoseTurn = self.state.whoseTurn
        currentPlayer = self.players[whoseTurn]
        #Check if its human player's turn during play phase
        if self.state.phase == PLAY_PHASE and type(self.players[whoseTurn]) is HumanPlayer.HumanPlayer:
            #add location to human player's movelist if appropriatocity is valid
            if len(currentPlayer.moveList) != 0 and coord == currentPlayer.moveList[-1]:
                currentPlayer.moveList.pop()
            elif len(currentPlayer.moveList) == 0:
                #Need to check this here or it may try to get the last element of the list when it is empty
                if self.checkMoveStart(coord):
                    currentPlayer.moveList.append(coord)
            else:
                onList = False
                for checkCoord in currentPlayer.moveList:
                    if checkCoord == coord:
                        onList = True
                        
                if not onList and self.checkMovePath(currentPlayer.moveList[-1], coord): 
                    #add the coord to the move list so we can check if it makes a valid move
                    currentPlayer.moveList.append(coord)
                    
                    #enact the theoretical move
                    startCoord = currentPlayer.moveList[0]
                    antToMove = self.state.board[startCoord[0]][startCoord[1]].ant
                    move = Move(MOVE, currentPlayer.moveList, antToMove.type)
                    
                    #if the move wasn't valid, remove added coord from move list              
                    if not self.isValidMove(move):
                        currentPlayer.moveList.pop()
            
            #give moveList to UI so it can hightlight the player's path
            self.ui.moveList = currentPlayer.moveList
            
        #Check if its human player's turn during set up phase
        if self.state.phase == SETUP_PHASE and type(self.players[whoseTurn]) is HumanPlayer.HumanPlayer:
            currentPlayer.moveList.append(coord)
                
    # once end game has been reached, display screen "player x wins!" OK/Play Again button
    def isGameOver(self, playerId):
        opponentId = (playerId + 1) % 2
        
        #temp, remove later
        return False
        
        #if ((self.state.phase == PLAY_PHASE) and 
        #((self.state.inventories[playerId].queen.isAlive == False) or
        #(self.state.inventories[opponentId].antHill.captureHealth <= 0) or
        # (self.state.inventories[playerId].foodCount >= 11))):
           # return True
        # else:
          # return False
       
    #checks to see if the move is valid for the current player
    #maybe put in GameState to make available to students
    #Returns None if no move is given
    def isValidMove(self, move):
        #check for no move
        if move == None:
            return None
        
        #check for no move type
        if move.moveType == None:
            return False
            
        #for END type moves
        if move.moveType == END:
            return True
        
        #check for an empty coord list
        if move.coordList == None or len(move.coordList) == 0:
            return False
        
        #for MOVE and BUILD type moves
        if move.moveType == MOVE:
            firstCoord = move.coordList[0]
            #check valid start location (good coords and ant ownership)
            if self.checkMoveStart(firstCoord):
                #get ant to move
                antToMove = self.state.board[firstCoord[0]][firstCoord[1]].ant
                movePoints = UNIT_STATS[antToMove.type][MOVEMENT]             
                previousCoord = None
                
                for coord in move.coordList:
                    #if first runthough, need to set up previous coord
                    if previousCoord == None:
                        previousCoord = coord
                        continue  
                    #if any to-coords are invalid, return invalid move
                    if not self.checkMovePath(previousCoord, coord):
                        return False
                    #subtract cost of loc from movement points
                    constrAtLoc = self.state.board[coord[0]][coord[1]].constr
                    if constrAtLoc == None:
                        movePoints -= 1
                    else:
                        movePoints -= CONSTR_STATS[constrAtLoc.type][MOVE_COST]
                        
                    previousCoord = coord
                    
                #within movement range and hasn't moved yet?
                if movePoints >= 0 and antToMove.hasMoved == False:
                    return True
                else:
                    return False
                        
        elif move.moveType == BUILD:
            #coord list must contain one point for build
            if not len(move.coordList) == 1:
                return False
        
            buildCoord = move.coordList[0]
            #check valid start location
            if self.checkBuildStart(buildCoord):
                #we're building either an ant or constr for sure
               
                if self.state.board[buildCoord[0]][buildCoord[1]].ant == None:
                #we know we're building an ant
                    buildCost = None
                    #check buildType for valid ant
                    if move.buildType == WORKER:
                        buildCost = UNIT_STATS[WORKER][MOVEMENT]
                    elif move.buildType == DRONE:
                        buildCost = UNIT_STATS[DRONE][MOVEMENT]
                    elif move.buildType == D_SOLDIER:
                        buildCost = UNIT_STATS[D_SOLDIER][MOVEMENT]
                    elif move.buildType == I_SOLDIER:
                        buildCost = UNIT_STATS[I_SOLDIER][MOVEMENT]
                    else:
                        return False
                    
                    #check the player has enough food
                    if self.state.inventories[self.state.whoseTurn].foodCount >= buildCost:
                        return True
                    else:   
                        return False
                else:
                #we know we're building a construction
                    buildCost = CONSTR_STATS[TUNNEL][COST]
                    return self.state.inventories[self.state.whoseTurn].foodCount >= buildCost
                
            
        else:
            #what the heck kind of move is this?
            pass
        
    ##
    #isValidPlacement
    #
    #Returns None if no target is given
    ##
    def isValidPlacement(self, item, target):
        #If no target, return None (human vs ai caught by caller)
        if target == None:
            return None
                
        #check item type
        if item.type == ANTHILL or item.type == GRASS:
            #check target is on the board
            if target[0] >= 0 and target[0] < BOARD_LENGTH:
                #Nobody can place in the center two rows of the board or on their opponents side
                if target[1] >= 0 and target[1] < BOARD_LENGTH / 2 - 1:
                    #change target to access appropriate players locations
                    target = self.state.coordLookup(target, self.state.whoseTurn)
                    #make sure nothing is there yet
                    if self.state.board[target[0]][target[1]].constr == None:
                        #valid placement
                        return True
                    
        #check item type
        if item.type == FOOD:
            #check target is on the board
            if target[0] >= 0 and target[0] < BOARD_LENGTH:
                #Must place food on your opponents side
                if target[1] < BOARD_LENGTH and target[1] >= BOARD_LENGTH / 2 + 1:
                #change target to access appropriate players locations
                #
                    target = self.state.coordLookup(target, self.state.whoseTurn)
                    #make sure nothing is there yet
                    if self.state.board[target[0]][target[1]].constr == None:
                        #valid placement
                        return True
        #invalid move
        return False
    
    def isValidAttack(self):
        pass

    ##
    #checkMoveStart 
    #Description: Checks if the location is valid to move from.
    # (bounds and ant ownership)
    ##
    def checkMoveStart(self, coord):
        #check location is on board
        if (coord[0] >= 0 and coord[0] < BOARD_LENGTH and
                coord[1] >= 0 and coord[1] < BOARD_LENGTH):
            antToMove = self.state.board[coord[0]][coord[1]].ant
            #check that an ant exists at the loc
            if not antToMove ==  None:
                #check that it's the player's ant
                if antToMove.player == self.state.whoseTurn:
                    return True
                    
        return False
    
    ##
    #checkBuildStart 
    #Description: Checks if the location is valid to build from.
    # (bounds and building ownership)
    ##    
    def checkBuildStart(self, coord):
        #check location is on board
        if (coord[0] >= 0 and coord[0] < BOARD_LENGTH and
                coord[1] >= 0 and coord[1] < BOARD_LENGTH):
            loc = self.state.board[coord[0]][coord[1]]
            #check that an empty anthill exists at the loc
            if not loc.constr == None and loc.constr.type == ANTHILL and loc.ant == None:
                #check that it's the player's anthill
                if loc.constr.player == self.state.whoseTurn:
                    return True
            #check that an ant exists at an empty location
            elif not loc.ant == None and loc.ant.type == WORKER and loc.constr == None:
                #check that it's the player's ant
                if loc.ant.player == self.state.whoseTurn:
                    return True
                    
        return False

    ##
    #checkMovePath
    #Description: Checks if the location is valid to move to.
    # (clear path, adjacent locations) 
    #
    #fromCoord must always be checked by the time it's passed
    #(either in checkMoveStart or previous checkMovePath call)
    ##
    def checkMovePath(self, fromCoord, toCoord):
        #check location is on board
        if (toCoord[0] >= 0 and toCoord[0] < BOARD_LENGTH and
                toCoord[1] >= 0 and toCoord[1] < BOARD_LENGTH):
            #check that squares are adjacent (difference on only one axis is 1)
            if ((abs(fromCoord[0] - toCoord[0]) == 1 and abs(fromCoord[1] - toCoord[1]) == 0) or
                    (abs(fromCoord[0] - toCoord[0]) == 0 and abs(fromCoord[1] - toCoord[1]) == 1)):
                antAtLoc = self.state.board[toCoord[0]][toCoord[1]].ant
                #check that an ant exists at the loc
                if antAtLoc ==  None:
                    return True
                    
        return False

a = Game()
a.runGame()
