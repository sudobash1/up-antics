import os, re, sys, math, HumanPlayer
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
        #all the players loaded in the game
        self.players = []
        #the current two players playing the game
        self.currentPlayers = []
        self.mode = None
        self.ui = UserInterface((865,695))
        self.ui.initAssets()
        self.errorNotify = False
        #Human vs AI mode
        self.expectingAttack = False
        #AI vs AI mode: used for stepping through moves
        self.nextClicked = False
        self.continueClicked = False
        #Tournament mode
        self.playerScores = [] # [[author,wins,losses], ...]
        self.gamesToPlay = [] #((p1.id, p2.id), numGames)
        self.numGames = None
        #UI Callback functions
        self.ui.buttons['Start'][-1] = self.startGame
        self.ui.buttons['Tournament'][-1] = self.tournamentPath
        self.ui.buttons['Human vs AI'][-1] = self.humanPath
        self.ui.buttons['AI vs AI'][-1] = self.aiPath      
        self.ui.humanButtons['Move'][-1] = self.moveClickedCallback
        self.ui.humanButtons['Build'][-1] = self.buildClickedCallback
        self.ui.humanButtons['End'][-1] = self.endClickedCallback
        self.ui.aiButtons['Next'][-1] = self.nextClickedCallback
        self.ui.aiButtons['Continue'][-1] = self.continueClickedCallback
        self.ui.antButtons['Worker'][-1] = self.buildWorkerCallback
        self.ui.antButtons['Drone'][-1] = self.buildDroneCallback
        self.ui.antButtons['D_Soldier'][-1] = self.buildDSoldierCallback
        self.ui.antButtons['I_Soldier'][-1] = self.buildISoldierCallback
        self.ui.antButtons['None'][-1] = self.buildNothingCallback
        self.ui.locationClicked = self.locationClickedCallback
        self.ui.checkBoxClicked = self.checkBoxClickedCallback
        #Finally, let the ui look at players
        self.ui.allAIs = self.players
          
    def runGame(self):
        # initialize board be ready for player input for game parameter
        while True:
            self.ui.drawBoard(self.state, self.mode)
            #Determine current chosen game mode. Enter different execution paths based on the mode, which must be chosen by clicking a button.
            
            #player has clicked start game so enter game loop
            if self.state.phase != MENU_PHASE:
                self.ui.notify("Game started!")
                
                #init game stuffs
                #build a list of things to place for player 1 in setup phase 1
                #1 anthill/queen, 9 obstacles
                constrsToPlace = []
                constrsToPlace += [Building(None, ANTHILL, PLAYER_ONE)]
                constrsToPlace += [Construction(None, GRASS) for i in xrange(0,9)]
                
                gameOver = False
                winner = None
                loser = None
                
                while not gameOver:
                    #draw the board (to recognize user input in game loop)
                    self.ui.drawBoard(self.state, self.mode)
                    
                    if self.state.phase != MENU_PHASE:
                        #if the player is player two, flip the board
                        theState = self.state.clone()
                        if theState.whoseTurn == PLAYER_TWO:
                            theState.flipBoard()
                    
                    if self.state.phase == SETUP_PHASE_1 or self.state.phase == SETUP_PHASE_2:
                        currentPlayer = self.currentPlayers[self.state.whoseTurn]
                        if type(currentPlayer) is HumanPlayer.HumanPlayer:
                            if constrsToPlace[0].type == ANTHILL:
                                self.ui.notify("Place anthill on your side") 
                            elif constrsToPlace[0].type == GRASS:
                                self.ui.notify("Place grass on your side")
                            elif constrsToPlace[0].type == FOOD:
                                self.ui.notify("Place food on enemy's side")
                        #clear targets list as anything on list been processed on last loop
                        targets = []
                        
                        #hide the 1st player's set anthill and grass placement from the 2nd player
                        if theState.whoseTurn == PLAYER_TWO and self.state.phase == SETUP_PHASE_1:
                            theState.clearConstrs()
                            
                        #get the placement from the player
                        targets += currentPlayer.getPlacement(theState)
                        #only want to place as many targets as constructions to place
                        if len(targets) > len(constrsToPlace):
                            targets = targets[:len(constrsToPlace)]
     
                        validPlace = self.isValidPlacement(constrsToPlace, targets)
                        if validPlace:
                            for target in targets:
                                #translate coords to match player
                                target = self.state.coordLookup(target, self.state.whoseTurn)
                                #get construction to place
                                constr = constrsToPlace.pop(0)
                                #give constr its coords
                                constr.coords = target
                                #put constr on board
                                self.state.board[target[0]][target[1]].constr = constr
                                if (constr.type == ANTHILL):
                                    #update the inventory
                                    self.state.inventories[self.state.whoseTurn].constructions.append(constr)
                            
                            #if AI mode, pause to observe move until next or continue is clicked
                            self.pauseForAIMode()
                            
                            if not constrsToPlace:
                                constrsToPlace = []
                                if self.state.phase == SETUP_PHASE_1:
                                    if self.state.whoseTurn == PLAYER_ONE:
                                        constrsToPlace += [Building(None, ANTHILL, PLAYER_TWO)]
                                        constrsToPlace += [Construction(None, GRASS) for i in xrange(0,9)]
                                    elif self.state.whoseTurn == PLAYER_TWO:
                                        constrsToPlace += [Construction(None, FOOD) for i in xrange(0,2)]
                                        self.state.phase = SETUP_PHASE_2
                                elif self.state.phase == SETUP_PHASE_2:
                                    if self.state.whoseTurn == PLAYER_ONE:
                                        constrsToPlace += [Construction(None, FOOD) for i in xrange(0,2)]
                                    elif self.state.whoseTurn == PLAYER_TWO:
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
                                        self.ui.notify("")
                                        self.state.phase = PLAY_PHASE
                                        
                                #change player turn in state
                                self.state.whoseTurn = (self.state.whoseTurn + 1) % 2
                                    
                        else:
                            if not type(currentPlayer) is HumanPlayer.HumanPlayer:
                                #exit gracefully
                                exit(0)
                            elif validPlace != None:
                                self.ui.notify("Invalid placement")
                                self.errorNotify = True
                        
                    elif self.state.phase == PLAY_PHASE: 
                        currentPlayer = self.currentPlayers[self.state.whoseTurn]
                        
                        #display instructions for human player
                        if type(currentPlayer) is HumanPlayer.HumanPlayer:
                            #An error message is showing
                            if not self.errorNotify:
                                #nothing selected yet
                                if not currentPlayer.coordList:
                                    self.ui.notify("Select an ant or building")
                                #ant selected
                                elif not self.state.board[currentPlayer.coordList[0][0]][currentPlayer.coordList[0][1]].ant == None:
                                    self.ui.notify("Select move for ant")
                                #Anthill selected
                                elif not self.state.board[currentPlayer.coordList[0][0]][currentPlayer.coordList[0][1]].constr == None:
                                    self.ui.notify("Select an ant type to build")
                                else:
                                    self.ui.notify("")
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
                                
                                #if AI mode, pause to observe move until next or continue is clicked                               
                                self.pauseForAIMode()   
                                
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
                                
                                #if AI mode, pause to observe move until next or continue is clicked
                                self.pauseForAIMode()
                                
                                #clear all highlights after build
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
                                
                                #if AI mode, pause to observe move until next or continue is clicked
                                self.pauseForAIMode()
                                
                                #switch whose turn it is
                                self.state.whoseTurn = (self.state.whoseTurn + 1) % 2
                            else:
                                #invalid move type, exit
                                exit(0)
                        else:     
                            #human can give None move, AI can't
                            if not type(currentPlayer) is HumanPlayer.HumanPlayer:
                                exit(0)
                            elif validMove != None:
                                #if validMove is False and not None, clear move
                                currentPlayer.coordList = []
                                self.ui.coordList = []
                            
                    else:
                        #wrong phase, 
                        exit(0)

                    #determine if if someone is a winner.
                    if self.hasWon(PLAYER_ONE):
                        gameOver = True
                        winner = self.currentPlayers[PLAYER_ONE].playerId
                        loser = self.currentPlayers[PLAYER_TWO].playerId
                        
                        #tell the players if they won or lost
                        self.currentPlayers[PLAYER_ONE].registerWin(True)
                        self.currentPlayers[PLAYER_TWO].registerWin(False)
                        
                    elif self.hasWon(PLAYER_TWO):
                        gameOver = True
                        loser = self.currentPlayers[PLAYER_ONE].playerId
                        winner = self.currentPlayers[PLAYER_TWO].playerId
                        
                        #tell the players if they won or lost
                        self.currentPlayers[PLAYER_ONE].registerWin(False)
                        self.currentPlayers[PLAYER_TWO].registerWin(True)
                #end game loop
    
                #check mode for appropriate response to game over
                if self.mode == HUMAN_MODE or self.mode == AI_MODE:
                    #reset the game
                    self.resetGame()
                    self.resetUI()
                    
                    #notify the user of the winner
                    if winner == PLAYER_ONE:
                        self.ui.notify("Player 1 has won the game!")
                    else:
                        self.ui.notify("Player 2 has won the game!")
                elif self.mode == TOURNAMENT_MODE: 
                    #adjust the count of games to play for the current pair
                    currentPairing = (self.currentPlayers[PLAYER_ONE].playerId, self.currentPlayers[PLAYER_TWO].playerId)
                
                    #reset the game
                    self.resetGame()
                
                    #give the new scores to the UI
                    self.ui.tournamentScores = self.playerScores
                
                    #adjust the wins and losses of players
                    self.playerScores[winner][1] += 1
                    self.playerScores[loser][2] += 1
                   
                    for i in range(0, len(self.gamesToPlay)):
                        #if we found the current pairing
                        if self.gamesToPlay[i][0] == currentPairing:
                            #mark off another game for the pairing
                            self.gamesToPlay[i][1] -= 1
                            
                            #if the pairing has no more games, then remove it
                            if self.gamesToPlay[i][1] == 0:
                                self.gamesToPlay.remove(self.gamesToPlay[i])
                            break
                            
                    if len(self.gamesToPlay) == 0:
                        #if no more games to play, reset tournament stuff
                        self.numGames = 0                               
                        self.playerScores = []
                        self.mode = TOURNAMENT_MODE
                    else:
                        #setup game to run again
                        self.mode = TOURNAMENT_MODE
                        self.state.phase = SETUP_PHASE_1
                    
                        #get players from next pairing
                        playerOneId = self.gamesToPlay[0][0][0]
                        playerTwoId = self.gamesToPlay[0][0][1]
                    
                        #set up new current players
                        self.currentPlayers.append(self.players[playerOneId][0])
                        self.currentPlayers.append(self.players[playerTwoId][0])
                    
                    
                else:
                    #wrong or no mode, exit
                    exit(0)
    
    ##
    #resetGame
    #Description: resets the game's instance variables to their starting state
    #
    ##
    def resetGame(self):
        board = [[Location((col, row)) for row in xrange(0,BOARD_LENGTH)] for col in xrange(0,BOARD_LENGTH)]
        p1Inventory = Inventory(PLAYER_ONE, [], [], 0)
        p2Inventory = Inventory(PLAYER_TWO, [], [], 0)
        self.state = GameState(board, [p1Inventory, p2Inventory], MENU_PHASE, PLAYER_ONE)
        self.currentPlayers = []
        self.mode = None
        #Human vs AI mode
        self.expectingAttack = False
        #AI vs AI mode: used for stepping through moves
        self.nextClicked = False
        self.continueClicked = False
        #Don't reset Tournament Mode's variables, might need to run more games
        
    ##
    #resetUI
    #Description: resets the game's instance variables to their starting state
    #
    ##
    def resetUI(self):
        self.ui.initAssets()
        #UI Callback functions
        self.ui.buttons['Start'][-1] = self.startGame
        self.ui.buttons['Tournament'][-1] = self.tournamentPath
        self.ui.buttons['Human vs AI'][-1] = self.humanPath
        self.ui.buttons['AI vs AI'][-1] = self.aiPath      
        self.ui.humanButtons['Move'][-1] = self.moveClickedCallback
        self.ui.humanButtons['Build'][-1] = self.buildClickedCallback
        self.ui.humanButtons['End'][-1] = self.endClickedCallback
        self.ui.aiButtons['Next'][-1] = self.nextClickedCallback
        self.ui.aiButtons['Continue'][-1] = self.continueClickedCallback
        self.ui.antButtons['Worker'][-1] = self.buildWorkerCallback
        self.ui.antButtons['Drone'][-1] = self.buildDroneCallback
        self.ui.antButtons['D_Soldier'][-1] = self.buildDSoldierCallback
        self.ui.antButtons['I_Soldier'][-1] = self.buildISoldierCallback
        self.ui.antButtons['None'][-1] = self.buildNothingCallback
        self.ui.locationClicked = self.locationClickedCallback
        
    def loadAIs(self, humanMode):
        #If humanMode, then we're going to start AI ids at a higher number. Change modifier to reflect this
        modifier = 1 if humanMode else 0
        #Reset the player list in case some have been loaded already
        self.players = []
        self.ui.allAIs = self.players
        #Attempt to load AIs. Exit gracefully if user trying to load weird stuff.
        filesInAIFolder = os.listdir("AI")
        #Change directory to AI subfolder so modules can be loaded (they won't load as filenames).
        os.chdir('AI')
      
        #Add current directory in python's import search order.
        sys.path.insert(0, os.getcwd())
        #Make player instances from all AIs in folder.
        for file in filesInAIFolder:
            if re.match(".*\.py$", file):
                moduleName = file[:-3]
                #Check to see if the file is already loaded.
                temp = __import__(moduleName, globals(), locals(), [], -1)
                #If the module has already been imported into this python instance, reload it.
                if temp == None:
                    temp = reload(globals()[moduleName])
                #Create an instance of Player from temp
                self.players.append([temp.AIPlayer(len(self.players) + modifier), INACTIVE])
            else:
                #No proper AIs were found in the subdirectory, notify
                self.ui.notify("AIs could not be loaded.")
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
                    if not self.checkMovePath(previousCoord, coord, antToMove):
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
            if len(move.coordList) != 1:
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
                        self.ui.notify("")
                        return True
                    else:
                        self.ui.notify("Requires " + str(buildCost) + " food")
                        self.errorNotify = True
                        return False
                else:
                #we know we're building a construction
                    adjacentCoords = []
                    adjacentCoords.append(addCoords(buildCoord, (0, -1)))
                    adjacentCoords.append(addCoords(buildCoord, (0, 1)))
                    adjacentCoords.append(addCoords(buildCoord, (-1, 0)))
                    adjacentCoords.append(addCoords(buildCoord, (1, 0)))
                
                    #check that there's no food in adjacent locations
                    for aCoord in adjacentCoords:
                        if aCoord[0] >= 0 and aCoord[0] < 10 and aCoord[1] >= 0 and aCoord[1] < 10:
                            if (self.state.board[aCoord[0]][aCoord[1]].constr != None and
                                    self.state.board[aCoord[0]][aCoord[1]].constr.type == FOOD):
                                self.ui.notify("Cannot build next to food")
                                self.errorNotify = True
                                return False
                 
                    buildCost = CONSTR_STATS[TUNNEL][BUILD_COST]
                    if self.state.inventories[self.state.whoseTurn].foodCount >= buildCost:
                        self.ui.notify("")
                        return True
                    else:
                        self.ui.notify("Requires "+str(buildCost) + " food")
                        self.errorNotify = True
                        return False
                
            
        else:
            #what the heck kind of move is this?
            pass
        
    ##
    #isValidPlacement
    #Description: Length of targets cannot be longer than length of items
    #
    #Returns None if no target is given
    ##
    def isValidPlacement(self, items, targets):
        #If no target, return None (human vs ai caught by caller)
        if len(targets) == 0:
            return None

        for i in range(0, len(targets)):
            #check targets[i] is within proper boundaries x-wise
            if not (targets[i][0] >= 0 and targets[i][0] < BOARD_LENGTH):
                #Nobody can place in the center two rows of the board or on their opponents side
                return False
            
            #check item type
            if items[i].type == ANTHILL or items[i].type == GRASS:
                #check targets[i] is within proper boundaries y-wise
                if not (targets[i][1] >= 0 and targets[i][1] < BOARD_LENGTH / 2 - 1):
                    return False
            #check item type
            elif items[i].type == FOOD:
                #check targets[i] is within proper boundaries y-wise
                if not (targets[i][1] < BOARD_LENGTH and targets[i][1] >= BOARD_LENGTH / 2 + 1):
                    return False
            else:
                #I don't know what this type is.
                return False
            
            #change target to access appropriate players locations
            aTarget = self.state.coordLookup(targets[i], self.state.whoseTurn)
            #make sure nothing is there yet
            if not self.state.board[aTarget[0]][aTarget[1]].constr == None:
                return False
                    
        return True
    
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
                #keep track of valid attack coords (flipped for player two)
                validAttackCoords.append(self.state.coordLookup(ant.coords, currentPlayer.playerId))
        if validAttackCoords != []:
            #give instruction to human player
            if type(currentPlayer) is HumanPlayer.HumanPlayer:
                self.ui.notify("Select ant to attack")
            
            #players must attack if possible and we know at least one is valid
            attackCoords = None
            validAttack = False
            
            #if a human player, let it know an attack is expected (to affect location clicked context)
            if type(currentPlayer) is HumanPlayer.HumanPlayer:
                #give the valid attack coords to the ui to highlight                                
                self.ui.attackList = validAttackCoords
                #set expecting attack for location clicked context
                self.expectingAttack = True
            
            #keep requesting coords until valid attack is given
            while attackCoords == None or not validAttack:               
                #Draw the board again (to recognize user input inside loop)
                self.ui.drawBoard(self.state, self.mode)
                
                #Create a clone of the state to give to the player
                theState = self.state.clone()
                if theState.whoseTurn == PLAYER_TWO:
                    theState.flipBoard()
                        
                #get the attack from the player (flipped for player two)
                attackCoords = self.state.coordLookup(currentPlayer.getAttack(theState, validAttackCoords), currentPlayer.playerId)
                
                #check for the move's validity
                validAttack = self.isValidAttack(attackingAnt, attackCoords)
                if not validAttack:
                    if not type(currentPlayer) is HumanPlayer.HumanPlayer:
                        #if an ai submitted an invalid attack, exit
                        exit(0)
                    else:
                        #if a human submitted an invalid attack, reset coordList
                        currentPlayer.coordList = []

            #if we reached this point though loop, we must have a valid attack
            #if a human player, let it know an attack is expected (to affect location clicked context)
            if type(currentPlayer) is HumanPlayer.HumanPlayer:
                self.expectingAttack = False
            
            #decrement ants health
            attackedAnt = self.state.board[attackCoords[0]][attackCoords[1]].ant
            attackedAnt.health -= UNIT_STATS[attackingAnt.type][ATTACK]
            
            #check for dead ant
            if attackedAnt.health <= 0:
                #remove dead ant from board
                self.state.board[attackCoords[0]][attackCoords[1]].ant = None
                #remove dead ant from inventory
                self.state.inventories[opponentId].ants.remove(attackedAnt)
                
            #if AI mode, pause to observe attack until next or continue is clicked
            self.pauseForAIMode()
              
    ##
    #pauseForAIMode
    #Description: will pause the game if set to AI mode until user clicks next or continue
    #
    ##    
    def pauseForAIMode(self):
        if self.mode == AI_MODE:
            while not self.nextClicked and not self.continueClicked:
                self.ui.drawBoard(self.state, self.mode)
            #reset nextClicked to catch next move
            self.nextClicked = False
    
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
            if antToMove != None:
                #check that it's the player's ant and that it hasn't moved
                if antToMove.player == self.state.whoseTurn and not antToMove.hasMoved:
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
    def checkMovePath(self, fromCoord, toCoord, antToMove):
        #check that we're actaully moving an ant
        if antToMove == None:
            return False
        #check location is on board
        if (toCoord[0] >= 0 and toCoord[0] < BOARD_LENGTH and
                toCoord[1] >= 0 and toCoord[1] < BOARD_LENGTH):
            #check that squares are adjacent (difference on only one axis is 1)
            if ((abs(fromCoord[0] - toCoord[0]) == 1 and abs(fromCoord[1] - toCoord[1]) == 0) or
                    (abs(fromCoord[0] - toCoord[0]) == 0 and abs(fromCoord[1] - toCoord[1]) == 1)):
                antAtLoc = self.state.board[toCoord[0]][toCoord[1]].ant
                #check that an ant exists at the loc
                if antAtLoc ==  None or antAtLoc == antToMove:
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
            if loc.constr != None and loc.constr.type == ANTHILL and loc.ant == None:
                #check that it's the player's anthill
                if loc.constr.player == self.state.whoseTurn:
                    return True
            #check that an ant exists at an empty location
            elif loc.ant != None and loc.ant.type == WORKER and loc.constr == None:       
                #check that it's the player's ant and it hasn't moved
                if loc.ant.player == self.state.whoseTurn and not loc.ant.hasMoved:
                    return True
                    
        return False

    ##
    #startGame
    #Description: Starts a new game
    #
    ##
    def startGame(self):
        if self.mode == None:
            self.ui.notify("Please select a mode.")
            return
        
        #Make a temporary list to append to so that we may check how many AIs we have available.
        tempCurrent = [player for player in self.currentPlayers]
        #Load the first two active players (idx 0 is human player)
        for index in range(0, len(self.players)):
            if self.players[index][1] == ACTIVE:
                tempCurrent.append(self.players[index][0])
                for playerEntry in self.players[index + 1:]:
                    if playerEntry[1] == ACTIVE:
                        tempCurrent.append(playerEntry[0])
                        break
                break
        if len(tempCurrent) != 2:
            self.ui.notify("Please select AIs to play game.")
            return
        elif self.ui.choosingAIs:
            self.ui.choosingAIs = False
            return

        self.currentPlayers = tempCurrent

        if self.state.phase == MENU_PHASE:     
            #set up stuff for tournament mode
            if self.mode == TOURNAMENT_MODE:
                if self.ui.textBoxContent != '':
                    self.numGames = int(self.ui.textBoxContent)
                else:
                    self.ui.textBoxContent = '0'
                    self.numGames = 0
            
                #if numGames is non-positive, dont set up game
                if self.numGames <= 0:
                    return
                
                self.ui.tournamentScores = []
                
                for i in range(0, len(self.players)):
                    if self.players[i][1] == ACTIVE:
                        #initialize the player's win/loss scores
                        tempAuth = self.players[i][0].author
                        #If the length of the author's name is longer than 24 characters, truncate it to 24 characters
                        if len(tempAuth) > 20:
                            tempAuth = tempAuth[0:21] + "..."
                        
                        self.playerScores.append([tempAuth, 0, 0])
                        self.ui.tournamentScores.append([tempAuth, 0, 0])
                        
                        for j in range(i, len(self.players)):
                            if self.players[i][0] != self.players[j][0] and self.players[j][1] == ACTIVE:
                                self.gamesToPlay.append([(i, j), None])
                            
                numPairings = len(self.gamesToPlay)
                for i in range(0, numPairings):
                    #assign equal number of games to each pairing (rounds down)
                    self.gamesToPlay[i][1] = self.numGames
            
            #change the phase to setup
            self.state.phase = SETUP_PHASE_1
       
    ##
    #tournamentPath
    #Description: Responds to a user clicking on the Tournament button
    #
    ##
    def tournamentPath(self):
        #If already in tournament mode, do nothing. WILL BE CHANGED IN THE FUTURE
        if self.mode == TOURNAMENT_MODE or self.state.phase != MENU_PHASE:
            return
        #Attempt to load the AI files
        self.loadAIs(False)
        #Check right number of players, if successful set the mode.
        if len(self.players) >= 2:
            self.ui.choosingAIs = True
            self.mode = TOURNAMENT_MODE
            self.ui.notify("Mode set to Tournament Mode.")
    
    ##
    #humanPath
    #Description: Responds to a user clicking on the Human vs. AI button
    #
    ##
    def humanPath(self):
        #If already in human mode, do nothing.
        if self.mode == HUMAN_MODE or self.state.phase != MENU_PHASE:
            return
        #Attempt to load the AI files
        self.loadAIs(True) 
        #Add the human player to the player list
        self.players.insert(PLAYER_ONE, (HumanPlayer.HumanPlayer(PLAYER_ONE), ACTIVE))
        #Check right number of players, if successful set the mode.
        if len(self.players) >= 2:
            self.ui.choosingAIs = True
            self.mode = HUMAN_MODE
            self.ui.notify("Mode set to Human vs. AI.")
    
    ##
    #aiPath
    #Description: Responds to a user clicking on the AI vs. AI button
    #
    ##
    def aiPath(self):
        #If already in ai mode, do nothing.
        if self.mode == AI_MODE or self.state.phase != MENU_PHASE:
            return
        #Attempt to load the AI files
        self.loadAIs(False)
        #Check right number of players, if successful set the mode.
        if len(self.players) >= 2:
            self.ui.choosingAIs = True
            self.mode = AI_MODE
            self.ui.notify("Mode set to AI vs. AI.")    
        
    ##
    #locationClickedCallback
    #Description: Responds to a user clicking on a board location
    #
    ##
    def locationClickedCallback(self, coord):
        #Check if its human player's turn during play phase
        if self.state.phase == PLAY_PHASE and type(self.currentPlayers[self.state.whoseTurn]) is HumanPlayer.HumanPlayer:
            whoseTurn = self.state.whoseTurn
            currentPlayer = self.currentPlayers[whoseTurn]
            
            #add location to human player's movelist if appropriatocity is valid
            
            if len(currentPlayer.coordList) == 0:
                #Clicked when nothing selected yet (select ant or building)
                if self.checkMoveStart(coord) or self.checkBuildStart(coord) or self.expectingAttack:
                    currentPlayer.coordList.append(coord)
                self.errorNotify = False
                    
            elif len(currentPlayer.coordList) != 0 and coord == currentPlayer.coordList[-1]:
                #Clicked most recently added location (unselect building or submit ant move)
                if not self.ui.buildAntMenu:
                    moveStartLoc = self.state.board[currentPlayer.coordList[0][0]][currentPlayer.coordList[0][1]]
                    if moveStartLoc.ant == None:
                        currentPlayer.coordList.pop()
                    else:
                        currentPlayer.moveType = MOVE
                    self.errorNotify = False
                
            else:
                onList = False
                index = None
                for checkCoord in currentPlayer.coordList:
                    if checkCoord == coord:
                        onList = True
                        index = currentPlayer.coordList.index(coord)
                
                startCoord = currentPlayer.coordList[0]
                antToMove = self.state.board[startCoord[0]][startCoord[1]].ant
                if not onList:
                    if self.checkMovePath(currentPlayer.coordList[-1], coord, antToMove): 
                        #add the coord to the move list so we can check if it makes a valid move
                        currentPlayer.coordList.append(coord)
                        
                        #enact the theoretical move
                        move = Move(MOVE, currentPlayer.coordList, antToMove.type)
                        
                        #if the move wasn't valid, remove added coord from move list              
                        if not self.isValidMove(move):
                            currentPlayer.coordList.pop()
                        else:
                            self.errorNotify = False
                    else:
                        currentPlayer.coordList = []
                else:
                    #if the user clicked a previous location, change move to it
                    numToRemove = len(currentPlayer.coordList) - (index + 1)
                    for i in range(0, numToRemove):
                        currentPlayer.coordList.pop()
                
                        
            #give coordList to UI so it can hightlight the player's path
            if not self.expectingAttack:
                self.ui.coordList = currentPlayer.coordList
            
        #Check if its human player's turn during set up phase
        elif ((self.state.phase == SETUP_PHASE_1 or self.state.phase == SETUP_PHASE_2) 
                and type(self.currentPlayers[self.state.whoseTurn]) is HumanPlayer.HumanPlayer):
            self.currentPlayers[self.state.whoseTurn].coordList.append(coord)

    ##
    #moveClickedCallback
    #Description: Responds to a user clicking on the move button
    #
    ##
    def moveClickedCallback(self):
        #Check if its human player's turn during play phase
        if (self.state.phase == PLAY_PHASE and type(self.currentPlayers[self.state.whoseTurn]) is 
                HumanPlayer.HumanPlayer and not len(self.currentPlayers[self.state.whoseTurn].coordList) == 0):
            self.currentPlayers[self.state.whoseTurn].moveType = MOVE
    
    ##
    #buildClickedCallback
    #Description: Responds to a user clicking on the build button
    #
    ##
    def buildClickedCallback(self):
        #Check if its human player's turn during play phase
        if (self.state.phase == PLAY_PHASE and type(self.currentPlayers[self.state.whoseTurn]) is 
                HumanPlayer.HumanPlayer and len(self.currentPlayers[self.state.whoseTurn].coordList) == 1):
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
        if (self.state.phase == PLAY_PHASE and self.expectingAttack == False 
                and type(self.currentPlayers[self.state.whoseTurn]) is HumanPlayer.HumanPlayer):
            self.currentPlayers[self.state.whoseTurn].moveType = END
    
    ##
    #buildWorkerClickedCallback
    #Description: Responds to a user clicking on the Build Worker button
    #
    ##
    def buildWorkerCallback(self):
        whoseTurn = self.state.whoseTurn
        currentPlayer = self.currentPlayers[whoseTurn]
        
        self.ui.buildAntMenu = False
        currentPlayer.buildType = WORKER
    
    ##
    #buildDrondClickedCallback
    #Description: Responds to a user clicking on the Build Drone button
    #
    ##    
    def buildDroneCallback(self):
        whoseTurn = self.state.whoseTurn
        currentPlayer = self.currentPlayers[whoseTurn]
        
        self.ui.buildAntMenu = False
        currentPlayer.buildType = DRONE
    
    ##
    #buildSoldierClickedCallback
    #Description: Responds to a user clicking on the Build D_Soldier button
    #
    ##
    def buildDSoldierCallback(self):
        whoseTurn = self.state.whoseTurn
        currentPlayer = self.currentPlayers[whoseTurn]
        
        self.ui.buildAntMenu = False
        currentPlayer.buildType = D_SOLDIER
    
    ##
    #buildISoldierClickedCallback
    #Description: Responds to a user clicking on the Build I_Soldier button
    #
    ##
    def buildISoldierCallback(self):
        whoseTurn = self.state.whoseTurn
        currentPlayer = self.currentPlayers[whoseTurn]
        
        self.ui.buildAntMenu = False
        currentPlayer.buildType = I_SOLDIER  
    
    ##
    #buildNothinClickedCallback
    #Description: Responds to a user clicking on the Build None button
    #
    ##
    def buildNothingCallback(self):
        whoseTurn = self.state.whoseTurn
        currentPlayer = self.currentPlayers[whoseTurn]
        
        self.ui.buildAntMenu = False
        currentPlayer.moveType = None
        
        self.ui.coordList = []
        currentPlayer.coordList = []
    
    ##
    #nextClickedCallback
    #Description: Responds to a user clicking on the next button in AI vs AI mode
    #
    ##
    def nextClickedCallback(self):
        if self.state.phase != MENU_PHASE:
            self.nextClicked = True
    
    ##
    #continueClickedCallback
    #Description: Responds to a user clicking on the continue button in AI vs AI mode
    #
    ##
    def continueClickedCallback(self):
        if self.state.phase != MENU_PHASE:
            self.continueClicked = True
    
    ##
    #checkBoxClickedCallback
    #Description: Responds to a user clicking on a checkbox to select AIs
    #
    ##
    def checkBoxClickedCallback(self, index):
        self.players[index][1] = ACTIVE if self.players[index][1] == INACTIVE else INACTIVE

a = Game()
a.runGame()
