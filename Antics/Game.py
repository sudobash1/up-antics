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
        self.mode = None
        self.ui = UserInterface((865,695))
        self.ui.initAssets()
        #UI Callback functions
        self.ui.buttons['move'][-1] = self.moveClickedCallback
        self.ui.buttons['build'][-1] = self.buildClickedCallback
        self.ui.buttons['end'][-1] = self.endClickedCallback
        self.ui.buttons['start'][-1] = self.startGame
        self.ui.buttons['tournament'][-1] = self.tournamentPath
        self.ui.buttons['human'][-1] = self.humanPath
        self.ui.buttons['ai'][-1] = self.aiPath
        self.ui.antButtons['worker'][-1] = self.buildWorkerCallback
        self.ui.antButtons['drone'][-1] = self.buildDroneCallback
        self.ui.antButtons['dsoldier'][-1] = self.buildDSoldierCallback
        self.ui.antButtons['isoldier'][-1] = self.buildISoldierCallback
        self.ui.antButtons['none'][-1] = self.buildNothingCallback
        self.ui.locationClicked = self.locationClickedCallback
          
    def runGame(self):
        # initialize board be ready for player input for game parameter
        while True:
            self.ui.drawBoard(self.state)
            #Determine current chosen game mode. Enter different execution paths based on the mode, which must be chosen by clicking a button.
            
            #player has clicked start game so enter game loop
            if self.state.phase != MENU_PHASE:
                self.ui.notify("Game Started!")
                
                #init game stuffs
                #build a list of things to place
                #things to place: 2 anthill/queen, 9 obstacles, 2 food sources (for opponent)
                constrsToPlace = []
                constrsToPlace += [Building(None, ANTHILL, i) for i in xrange(0,2)]
                constrsToPlace += [Construction(None, GRASS) for i in xrange(0,18)]
                constrsToPlace += [Construction(None, FOOD) for i in xrange(0,4)]
                
                gameOver = False
                winner = None
                
                while not gameOver:
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
                            target = self.state.coordLookup(target, self.state.whoseTurn)
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
                            #give the players the initial food
                            self.state.inventories[PLAYER_ONE].foodCount = 3
                            self.state.inventories[PLAYER_TWO].foodCount = 3
                            #change to play phase
                            self.state.phase = PLAY_PHASE
                        
                    elif self.state.phase == PLAY_PHASE: 
                        currentPlayer = self.players[self.state.whoseTurn]
                        
                        #if the player is player two, flip the board
                        theState = self.state.clone()
                        if theState.whoseTurn == PLAYER_TWO:
                            theState.flipBoard()
                        
                        #get the move from the current player
                        move = currentPlayer.getMove(theState)
                        
                        if not move == None and move.coordList != None:
                            for i in xrange(0,len(move.coordList)):
                                #translate coords of move to match player
                                move.coordList[i] = self.state.coordLookup(move.coordList[i], self.state.whoseTurn)
                        
                        #make sure it's a valid move
                        validMove = self.isValidMove(move)
                        
                        #complete the move if valid
                        if validMove:
                            #check move type
                            if move.moveType == MOVE:
                                startCoord = move.coordList[0]
                                endCoord = move.coordList[-1]
                                
                                #take ant from start coord
                                antToMove = self.state.board[startCoord[0]][startCoord[1]].ant
                                #change ant's coords and hasMoved status
                                antToMove.coords = (endCoord[0], endCoord[1])
                                antToMove.hasMoved = True
                                #remove ant from location
                                self.state.board[startCoord[0]][startCoord[1]].ant = None
                                #put ant at last loc in coordList
                                self.state.board[endCoord[0]][endCoord[1]].ant = antToMove
                                #clear all highlights after move happens
                                self.ui.coordList = []
                                
                                #check and take action for attack
                                self.resolveAttack(antToMove, currentPlayer)                                
                                #clear all highlights after attack happens
                                self.ui.coordList = []
                                self.ui.attackList = []
                                                                                          
                            elif move.moveType == BUILD:
                                coord = move.coordList[0]
                                currentPlayerInv = self.state.inventories[self.state.whoseTurn]
                                                         
                                #subtract the cost of the item from the player's food count
                                if move.buildType == TUNNEL:
                                    currentPlayerInv.foodCount -= CONSTR_STATS[move.buildType][BUILD_COST]
                                    
                                    tunnel = Building(coord, TUNNEL, self.state.whoseTurn)
                                    self.state.board[coord[0]][coord[1]].constr = tunnel
                                else:
                                    currentPlayerInv.foodCount -= UNIT_STATS[move.buildType][COST]
                                    
                                    ant = Ant(coord, move.buildType, self.state.whoseTurn)
                                    ant.hasMoved = True
                                    self.state.board[coord[0]][coord[1]].ant = ant
                                    self.state.inventories[self.state.whoseTurn].ants.append(ant)
                                
                                self.ui.coordList = []    
                                
                            elif move.moveType == END:
                                for ant in self.state.inventories[self.state.whoseTurn].ants:
                                    #reset hasMoved on all ants of player
                                    ant.hasMoved = False
                                    constrUnderAnt = self.state.board[ant.coords[0]][ant.coords[1]].constr
                                    if constrUnderAnt != None:
                                        if type(constrUnderAnt) is Building and not constrUnderAnt.player == self.state.whoseTurn:
                                            #affect capture health of buildings
                                            constrUnderAnt.captureHealth -= 1
                                            if constrUnderAnt.captureHealth == 0 and constrUnderAnt.type != ANTHILL:
                                                constrUnderAnt.player = self.state.whoseTurn
                                                constrUnderAnt.captureHealth = CONSTR_STATS[constrUnderAnt.type][CAP_HEALTH]
                                        elif constrUnderAnt.type == FOOD and ant.type == WORKER:
                                            #have all worker ants on food sources gather food
                                            ant.carrying = True
                                        elif (constrUnderAnt.type == ANTHILL or constrUnderAnt.type == TUNNEL) and ant.carrying == True:
                                            #deposit carried food (only workers carry)
                                            self.state.inventories[self.state.whoseTurn].foodCount += 1
                                            ant.carrying = False
                                            
                                #clear any currently highlighted squares
                                self.ui.coordList = []
                                            
                                #switch whose turn it is
                                self.state.whoseTurn = (self.state.whoseTurn + 1) % 2
                            else:
                                #invalid move type, exit
                                pass
                        else:
                            #not a valid move, check if None
                            #human can give None move, AI can't
                            pass
                    else:
                        #wrong phase, exit
                        exit(0)

                    if self.hasWon(PLAYER_ONE):
                        gameOver = True
                        winner = PLAYER_ONE
                    elif self.hasWon(PLAYER_TWO):
                        gameOver = True
                        winner = PLAYER_TWO
                
    def startGame(self):
        if self.mode != None and self.state.phase == MENU_PHASE:
            self.state.phase = SETUP_PHASE
                
    def tournamentPath(self):
        #If already in tournament mode, do nothing. WILL BE CHANGED IN THE FUTURE
        if self.mode == TOURNAMENT_MODE:
            return
        #Attempt to load the AI files
        self.loadAIs(False)
        #Check right number of players, if successful set the mode.
        if len(self.players) >= 2:
            self.mode = TOURNAMENT_MODE
        self.mode = None # DELETE THIS LINE LATER!!
        
    def humanPath(self):
        #If already in human mode, do nothing.
        if self.mode == HUMAN_MODE:
            return
        #Attempt to load the AI files
        self.loadAIs(True) 
        #Add the human player to the player list
        self.players.insert(PLAYER_ONE, HumanPlayer.HumanPlayer(PLAYER_ONE))
        #Check right number of players, if successful set the mode.
        if len(self.players) == 2:
            self.mode = HUMAN_MODE
            self.ui.notify("Mode changed to human")
    
    def aiPath(self):
        #If already in ai mode, do nothing.
        if self.mode == AI_MODE:
            return
        #Attempt to load the AI files
        self.loadAIs(False)
        #Check right number of players, if successful set the mode.
        if len(self.players) == 2:
            self.mode = AI_MODE
        self.mode = None # DELETE THIS LINE LATER!!
    
    def loadAIs(self, humanMode):
        #If humanMode, then we're going to start AI ids at a higher number. Change modifier to reflect this
        modifier = 1 if humanMode else 0
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
                self.players.append(temp.AIPlayer(len(self.players) + modifier))
        #Remove current directory from python's import search order.
        sys.path.pop(0)
        #Revert working directory to parent.
        os.chdir('..')
    
    ##
    #isValidMove(Move)
    #Description: Checks to see if the move is valid for the current player.
    #  (maybe put in GameState to make available to students)
    #
    #Returns: None if no move is given
    ##
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
            
        #CHECK THAT THE MOVE IS WELL FORMED (typewise, tuples, ints, etc)
        
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
                    if constrAtLoc == None or antToMove.type == DRONE:
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
                        buildCost = UNIT_STATS[WORKER][COST]
                    elif move.buildType == DRONE:
                        buildCost = UNIT_STATS[DRONE][COST]
                    elif move.buildType == D_SOLDIER:
                        buildCost = UNIT_STATS[D_SOLDIER][COST]
                    elif move.buildType == I_SOLDIER:
                        buildCost = UNIT_STATS[I_SOLDIER][COST]
                    else:
                        return False
                    
                    #check the player has enough food
                    if self.state.inventories[self.state.whoseTurn].foodCount >= buildCost:
                        return True
                    else:   
                        return False
                else:
                #we know we're building a construction
                    buildCost = CONSTR_STATS[TUNNEL][BUILD_COST]
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
    
    ##
    #isValidAttack
    #Description: Determines whether the attack with the given parameters is valid
    #Attacking ant is assured to exist and belong to the player whose turn it is
    ##  
    def isValidAttack(self, attackingAnt, attackCoords):
        if attackCoords == None:
            return None
    
        attackLoc = self.state.board[attackCoords[0]][attackCoords[1]]
        
        if attackLoc.ant == None or attackLoc.ant.player == attackingAnt.player:
            return False
        
        #we know we have an enemy ant
        range = UNIT_STATS[attackingAnt.type][RANGE]
        diffX = abs(attackingAnt.coords[0] - attackCoords[0])
        diffY = abs(attackingAnt.coords[1] - attackCoords[1])
        
        #pythagoras would be proud
        if range ** 2 >= diffX ** 2 + diffY ** 2:
            #return True if within range
            return True
        else:
            return False
            
    ##
    #hasWon(int)
    #Description: Determines whether the game has ended in victory for the given player.
    #   
    # Returns: True if the player with playerId has won the game.
    ##
    def hasWon(self, playerId):
        opponentId = (playerId + 1) % 2
        
        if ((self.state.phase == PLAY_PHASE) and 
        ((self.state.inventories[opponentId].getQueen() == None) or
        (self.state.inventories[opponentId].getAnthill().captureHealth <= 0) or
        (self.state.inventories[playerId].foodCount >= 11))):
            return True
        else:
            return False

    ##
    #resolveAttack 
    #Description: Checks a player wants to attack and takes appropriate action.
    #
    ##   
    def resolveAttack(self, attackingAnt, currentPlayer):
        #check if player wants to attack
        validAttackCoords = []
        opponentId = (self.state.whoseTurn + 1) % 2
        range = UNIT_STATS[attackingAnt.type][RANGE]
        for ant in self.state.inventories[opponentId].ants:
            if self.isValidAttack(attackingAnt, ant.coords):
                validAttackCoords.append(ant.coords)
        
        if validAttackCoords != []:
            #players must attack if possible and we know at least one is valid
            attackCoords = None
            validAttack = False
            
            #if a human player, let it know an attack is expected (to affect location clicked context)
            if type(currentPlayer) == HumanPlayer.HumanPlayer:
                #give the valid attack coords to the ui to highlight                                
                self.ui.attackList = validAttackCoords
                #set expecting attack for location clicked context
                currentPlayer.expectingAttack = True
            
            #keep requesting coords until valid attack is given
            while attackCoords == None or not validAttack:               
                #Draw the board again (to recognize user input inside loop)
                self.ui.drawBoard(self.state)
                
                #get the attack from the player
                attackCoords = currentPlayer.getAttack(validAttackCoords)
                validAttack = self.isValidAttack(attackingAnt, attackCoords)
                
                if not validAttack:
                    if type(currentPlayer) != HumanPlayer.HumanPlayer:
                        #if an ai submitted an invalid attack, exit
                        exit(0)
                    else:
                        #if a human submitted an invalid attack, reset coordList
                        currentPlayer.coordList = []
                    
             
            #if we reached this point though loop, we must have a valid attack
            #if a human player, let it know an attack is expected (to affect location clicked context)
            if type(currentPlayer) == HumanPlayer.HumanPlayer:
                currentPlayer.expectingAttack = False
            
            #decrement ants health
            attackedAnt = self.state.board[attackCoords[0]][attackCoords[1]].ant
            attackedAnt.health -= UNIT_STATS[attackingAnt.type][ATTACK]
            
            #check for dead ant
            if attackedAnt.health <= 0:
                #remove dead ant from board
                self.state.board[attackCoords[0]][attackCoords[1]].ant = None
                #remove dead ant from inventory
                self.state.inventories[opponentId].ants.remove(attackedAnt)
    
    ##
    #checkMoveStart 
    #Description: Checks if the location is valid to move from.
    #  (bounds and ant ownership)
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
    #checkMovePath
    #Description: Checks if the location is valid to move to.
    #  (clear path, adjacent locations) 
    #
    #fromCoord must always have been checked by the time it's passed
    #  (either in checkMoveStart or previous checkMovePath call)
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

    ##
    #checkBuildStart 
    #Description: Checks if the location is valid to build from.
    #  (bounds and building ownership)
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
    #locationClickedCallback
    #Description: Responds to a user clicking on a board location
    #
    ##
    def locationClickedCallback(self, coord):
        #Check if its human player's turn during play phase
        if self.state.phase == PLAY_PHASE and type(self.players[self.state.whoseTurn]) is HumanPlayer.HumanPlayer:
            whoseTurn = self.state.whoseTurn
            currentPlayer = self.players[whoseTurn]
            
            #add location to human player's movelist if appropriatocity is valid
            if len(currentPlayer.coordList) != 0 and coord == currentPlayer.coordList[-1]:
                currentPlayer.coordList.pop()
            elif len(currentPlayer.coordList) == 0:
                #Need to check this here or it may try to get the last element of the list when it is empty
                if self.checkMoveStart(coord) or self.checkBuildStart(coord) or currentPlayer.expectingAttack:
                    currentPlayer.coordList.append(coord)
            else:
                onList = False
                for checkCoord in currentPlayer.coordList:
                    if checkCoord == coord:
                        onList = True
                        
                if not onList and self.checkMovePath(currentPlayer.coordList[-1], coord): 
                    #add the coord to the move list so we can check if it makes a valid move
                    currentPlayer.coordList.append(coord)
                    
                    #enact the theoretical move
                    startCoord = currentPlayer.coordList[0]
                    antToMove = self.state.board[startCoord[0]][startCoord[1]].ant
                    move = Move(MOVE, currentPlayer.coordList, antToMove.type)
                    
                    #if the move wasn't valid, remove added coord from move list              
                    if not self.isValidMove(move):
                        currentPlayer.coordList.pop()
            
            #give coordList to UI so it can hightlight the player's path
            if not currentPlayer.expectingAttack:
                self.ui.coordList = currentPlayer.coordList
            
        #Check if its human player's turn during set up phase
        if self.state.phase == SETUP_PHASE and type(self.players[self.state.whoseTurn]) is HumanPlayer.HumanPlayer:
            self.players[self.state.whoseTurn].coordList.append(coord)

    ##
    #moveClickedCallback
    #Description: Responds to a user clicking on the move button
    #
    ##
    def moveClickedCallback(self):
        #Check if its human player's turn during play phase
        if (self.state.phase == PLAY_PHASE and type(self.players[self.state.whoseTurn]) is 
                HumanPlayer.HumanPlayer and not len(self.players[self.state.whoseTurn].coordList) == 0):
            self.players[self.state.whoseTurn].moveType = MOVE
    
    ##
    #buildClickedCallback
    #Description: Responds to a user clicking on the build button
    #
    ##
    def buildClickedCallback(self):
        #Check if its human player's turn during play phase
        if (self.state.phase == PLAY_PHASE and type(self.players[self.state.whoseTurn]) is 
                HumanPlayer.HumanPlayer and len(self.players[self.state.whoseTurn].coordList) == 1):
            whoseTurn = self.state.whoseTurn
            currentPlayer = self.players[whoseTurn]
            
            loc = self.state.board[currentPlayer.coordList[0][0]][currentPlayer.coordList[0][1]]
            #we know loc has to have an ant or constr at this point, so make sure it doesnt have both
            if loc.constr == None or loc.ant == None:
                if loc.constr == None:
                    #a tunnel is to be built
                    currentPlayer.buildType = TUNNEL
                elif loc.ant == None:
                    self.ui.buildAntMenu = True                    
                
                currentPlayer.moveType = BUILD

    ##
    #endClickedCallback
    #Description: Responds to a user clicking on the end button
    #
    ##
    def endClickedCallback(self):     
        #Check if its human player's turn during play phase
        if self.state.phase == PLAY_PHASE and type(self.players[self.state.whoseTurn]) is HumanPlayer.HumanPlayer:
            self.players[self.state.whoseTurn].moveType = END
    
    def buildWorkerCallback(self):
        whoseTurn = self.state.whoseTurn
        currentPlayer = self.players[whoseTurn]
        
        self.ui.buildAntMenu = False
        currentPlayer.buildType = WORKER
        
    def buildDroneCallback(self):
        whoseTurn = self.state.whoseTurn
        currentPlayer = self.players[whoseTurn]
        
        self.ui.buildAntMenu = False
        currentPlayer.buildType = DRONE
        
    def buildDSoldierCallback(self):
        whoseTurn = self.state.whoseTurn
        currentPlayer = self.players[whoseTurn]
        
        self.ui.buildAntMenu = False
        currentPlayer.buildType = D_SOLDIER
    
    def buildISoldierCallback(self):
        whoseTurn = self.state.whoseTurn
        currentPlayer = self.players[whoseTurn]
        
        self.ui.buildAntMenu = False
        currentPlayer.buildType = I_SOLDIER  
    
    def buildNothingCallback(self):
        whoseTurn = self.state.whoseTurn
        currentPlayer = self.players[whoseTurn]
        
        self.ui.buildAntMenu = False
        currentPlayer.moveType = None
        
    
    
a = Game()
a.runGame()
