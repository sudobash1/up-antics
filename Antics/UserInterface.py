##
#UserInterface
#Description: This class renders the game board through pygame library method calls,
#   and handles user input events.
#
##
import pygame, os, sys
from pygame.locals import *
from Building import Building
from Constants import *

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (195, 195, 195)
DARK_RED = (150, 0, 0)
LIGHT_RED = (255, 0, 0)
DARK_GREEN = (0, 150, 0)
LIGHT_GREEN = (0, 255, 0)
CELL_SIZE = Rect(0,0,10,10)
BOARD_SIZE = Rect(0,0,10,10)
CELL_SPACING = 5

def addCoords(tuple1, tuple2):
    if len(tuple1) != len(tuple2):
        return None
    else:
        return tuple([tuple1[i] + tuple2[i] for i in range(0, len(tuple1))])

def subtractCoords(tuple1, tuple2):
    if len(tuple1) != len(tuple2):
        return None
    else:
        return tuple([tuple1[i] - tuple2[i] for i in range(0, len(tuple1))])

class UserInterface(object):
    ##
    #__init__
    #Description: Creates a new UserInterface
    #
    #Parameters:
    #   inputSize - the size of the window to be created, in pixels.
    ##
    def __init__(self, inputSize):
        self.screen = pygame.display.set_mode(inputSize)
        pygame.display.set_caption("aNTiCS")
        icon = pygame.image.load(os.path.join("Textures", "icon.bmp"))
        pygame.display.set_icon(icon)
    
    ##
    #submitMove
    #Description: Dummy method used as a placeholder for the event handling methods that will be passed in from Game.py.
    ##
    def submitMove(self):
        print "Clicked SUBMIT MOVE"
    
    ##
    #submitBuild
    #Description: Dummy method used as a placeholder for the event handling methods that will be passed in from Game.py.
    ##
    def submitBuild(self):
        print "Clicked SUBMIT BUILD"
    
    ##
    #submitEndTurn
    #Description: Dummy method used as a placeholder for the event handling methods that will be passed in from Game.py.
    ##
    def submitEndTurn(self):
        print "Clicked SUBMIT END TURN"
    
    ##
    #gameModeTournament
    #Description: Dummy method used as a placeholder for the event handling methods that will be passed in from Game.py.
    ##
    def gameModeTournament(self):
        print "Clicked GAME MODE TOURNAMENT"
    
    ##
    #gameModeHumanAI
    #Description: Dummy method used as a placeholder for the event handling methods that will be passed in from Game.py.
    ##
    def gameModeHumanAI(self):
        print "Clicked GAME MODE HUMAN AI"
    
    ##
    #gameModeAIAI
    #Description: Dummy method used as a placeholder for the event handling methods that will be passed in from Game.py.
    ##
    def gameModeAIAI(self):
        print "Clicked GAME MODE AI AI"
    
    ##
    #startGame
    #Description: Dummy method used as a placeholder for the event handling methods that will be passed in from Game.py.
    ##
    def startGame(self):
        print "Clicked START GAME"
    
    ##
    #submitNext
    #Description: Dummy method used as a placeholder for the event handling methods that will be passed in from Game.py.
    ##
    def submitNext(self):
        print "Clicked NEXT"
    
    ##
    #submitContinue
    #Description: Dummy method used as a placeholder for the event handling methods that will be passed in from Game.py.
    ##
    def submitContinue(self):
        print "Clicked CONTINUE"
    
    ##
    #submitWorker
    #Description: Dummy method used as a placeholder for the event handling methods that will be passed in from Game.py.
    ##
    def submitWorker(self):
        print "Clicked WORKER"
    
    ##
    #submitDrone
    #Description: Dummy method used as a placeholder for the event handling methods that will be passed in from Game.py.
    ##
    def submitDrone(self):
        print "Clicked DRONE"
    
    ##
    #submitDSoldier
    #Description: Dummy method used as a placeholder for the event handling methods that will be passed in from Game.py.
    ##
    def submitDSoldier(self):
        print "Clicked DIRECT SOLDIER"
    
    ##
    #submitISoldier
    #Description: Dummy method used as a placeholder for the event handling methods that will be passed in from Game.py.
    ##
    def submitISoldier(self):
        print "Clicked INDIRECT SOLDIER"
    
    ##
    #submitNoBuild
    #Description: Dummy method used as a placeholder for the event handling methods that will be passed in from Game.py.
    ##
    def submitNoBuild(self):
        print "Clicked BUILD NOTHING"
    
    ##
    #submitStartTournament
    #Description: Dummy method used as a placeholder for the event handling methods that will be passed in from Game.py.
    ##
    def submitStartTournament(self):
        print "Clicked START TOURNAMENT"
    
    ##
    #submitStopTournament
    #Description: Dummy method used as a placeholder for the event handling methods that will be passed in from Game.py.
    ##
    def submitStopTournament(self):
        print "Clicked STOP TOURNAMENT"
    
    def locationClicked(self, coords):
        print "Clicked LOCATION " + str(coords)
    
    def notify(self, message):
        self.lastNotification = message
    
    def drawNotification(self):
        messageSurface = self.notifyFont.render(self.lastNotification, True, DARK_RED)
        self.screen.blit(messageSurface, self.messageLocation)
    
    ##
    #drawConstruction
    #Description: Draws a non-moving structure of the specified type to the specified location on the game board.
    #
    #Parameters:
    #   item - an object subclassed from Construction.
    #   position - a tuple that indicates a cell on the board. This will be converted to a pixel location.
    ##
    def drawConstruction(self, item, position):
        Xpixel = CELL_SPACING * (position[0] + 1) + CELL_SIZE.width * position[0]
        Ypixel = CELL_SPACING * (position[1] + 1) + CELL_SIZE.height * position[1]
        self.screen.blit(self.constructionTexs[item.type], (Xpixel, Ypixel))
        if type(item) is Building:
            #Draw player marker in lower left
            playerNumber = self.notifyFont.render(str(item.player + 1), True, BLACK)
            self.screen.blit(playerNumber, (Xpixel, Ypixel + CELL_SIZE.height - playerNumber.get_height()))
    
    ##
    #drawAnt
    #Description: Draws an Ant of the specified type to the specified location on the game board.
    #
    #Parameters:
    #   ant - an Ant object.
    #   position - a tuple that indicates a cell on the board. This will be converted to a pixel location.
    ##
    def drawAnt(self, ant, position):
        Xpixel = CELL_SPACING * (position[0] + 1) + CELL_SIZE.width * position[0]
        Ypixel = CELL_SPACING * (position[1] + 1) + CELL_SIZE.height * position[1]
        self.screen.blit(self.antTexs[ant.type], (Xpixel, Ypixel))
        #Draw player marker in upper left
        playerNumber = self.notifyFont.render(str(ant.player + 1), True, BLACK)
        self.screen.blit(playerNumber, (Xpixel, Ypixel))
        #Draw current health in the upper right
        antHealth = self.notifyFont.render("Health: " + str(ant.health), True, BLACK)
        XoffsetHealth = CELL_SIZE.width - antHealth.get_width()
        self.screen.blit(antHealth, (Xpixel + XoffsetHealth, Ypixel))
        #Draw isCarrying marker in lower right
        if ant.carrying:
            XoffsetCarry = CELL_SIZE.width - self.isCarryingTex.get_width()
            YoffsetCarry = CELL_SIZE.height - self.isCarryingTex.get_height()
            self.screen.blit(self.isCarryingTex, (Xpixel + XoffsetCarry, Ypixel + YoffsetCarry))
        #Draw hasMoved marker as a shade across the image
        if ant.hasMoved:
            self.screen.blit(self.hasMovedTex, (Xpixel, Ypixel))
    
    ##
    #drawButton
    #Description: Draws a button to the board. All necessary information is contained in self.buttons under the given key.
    #
    #Parameters:
    #   key - a key in the self.buttons hash table, known in Python as a Dictionary.
    ##
    def drawButton(self, key, buttons):
        label = self.gameFont.render(key, True, BLACK)
        offset = subtractCoords(self.buttonRect.center, label.get_rect().center)
        self.screen.blit(self.buttonTextures[buttons[key][1]], buttons[key][0])
        self.screen.blit(label, addCoords(buttons[key][0], offset))
    
    ##
    #drawScoreBoard
    #Description: Draws the scores of both players as given.
    #
    #Parameters:
    #   player1Score - the integer value of player 1's food stock.
    #   player2Score - the integer value of player 2's food stock.
    ##
    def drawScoreBoard(self, player1Score, player2Score):
        label1 = self.gameFont.render("Player 1: " + str(player1Score) + " food", True, BLACK)
        label2 = self.gameFont.render("Player 2: " + str(player2Score) + " food", True, BLACK)
        self.screen.blit(label1, self.scoreLocation)
        self.screen.blit(label2, addCoords(self.scoreLocation, (0, label2.get_rect().height)))
    
    ##
    #
    ##
    def drawTextBox(self):
        pygame.draw.rect(self.screen, DARK_RED if self.textBoxContent == '' else LIGHT_GREEN, self.buttonRect.move(self.textPosition))
        label = self.gameFont.render(self.textBoxContent + ('|' if self.boxSelected else ''), True, BLACK)
        offset = subtractCoords(self.buttonRect.center, label.get_rect().center)
        self.screen.blit(label, addCoords(self.textPosition, offset))
    
    ##
    #Description: Draws the tournament score table from a list of (author string, wins int, losses int, ties int) tuples.
    ##
    def drawTable(self):
        XStartPixel = 50
        YStartPixel = self.screen.get_height() / 2 - len(self.tournamentScores) * 20 / 2
        if YStartPixel < 0:
            YStartPixel = 0
        #Prepend the column headers to the tournamentScores list, so that we can draw the entire table without special cases.
        scores = [('Author', 'Wins', 'Losses')] + self.tournamentScores
        #Find the longest string for each column
        lengths = [0 for i in range(0, len(scores[0]) + 1)]
        for score in scores:
            for index in range(0, len(score)):
                if len(str(score[index])) > lengths[index+1]:
                    lengths[index + 1] = len(str(score[index]))
        #Draw the table itself
        for index in range(0, len(scores)):
            for innerDex in range(0, len(scores[index])):
                Xoffset = 0 if innerDex == 0 else reduce(lambda x,y: x+y, lengths[:innerDex+1])
                tempX = XStartPixel + Xoffset * 8 + 10
                tempY = YStartPixel + index * 20
                label = self.notifyFont.render(str(scores[index][innerDex]), True, BLACK)
                self.screen.blit(label, (tempX, tempY))
    
    def drawAIChecklist(self):
        XStartPixel = 50
        YStartPixel = self.screen.get_height() / 2 - len(self.allAIs) * self.checkboxes[0].get_height() / 2
        if YStartPixel < 0:
            YStartPixel = 0
        #Draw it.
        for index in range(0, len(self.allAIs)):
            tempY = YStartPixel + index * self.checkBoxRect.height + 10
            self.screen.blit(self.checkBoxeTextures[self.chosenAIs[index]], (XStartPixel, tempY))
            label = self.notifyFont.render(str(self.allAIs[index].author), True, BLACK)
            self.screen.blit(label, (XStartPixel + self.checkBoxRect.width + 10, tempY))
    
    def drawCell(self, currentLoc):
        col = currentLoc.coords[0]
        row = currentLoc.coords[1]
        #Find the x y coordinates that this column and row map to.
        Xpixel = CELL_SPACING * (col + 1) + CELL_SIZE.width * col
        Ypixel = CELL_SPACING * (row + 1) + CELL_SIZE.height * row
        #Create a Rect that shows up if the square is selected.
        shadeWidth = 2 * CELL_SPACING + CELL_SIZE.width
        shadeHeight = 2 * CELL_SPACING + CELL_SIZE.height
        shadeRect = Rect(0, 0, shadeWidth, shadeHeight)
        #Find the X and Y coordinates to draw the shade at.
        shadeXpixel = Xpixel - CELL_SPACING
        shadeYpixel = Ypixel - CELL_SPACING
        if self.coordList != []:
            if currentLoc.coords in self.coordList[:-1]:
                #Draw the shadeRect if currentLoc is in coordList
                pygame.draw.rect(self.screen, DARK_GREEN, shadeRect.move(shadeXpixel, shadeYpixel))
            elif currentLoc.coords == self.coordList[-1]:
                #Draw brighter if the currentLoc is the last move selected
                pygame.draw.rect(self.screen, LIGHT_GREEN, shadeRect.move(shadeXpixel, shadeYpixel))
        #Draw the shade for a cell highlighted for attacks if currentLoc is in attackList
        if currentLoc.coords in self.attackList:
            pygame.draw.rect(self.screen, LIGHT_RED, shadeRect.move(shadeXpixel, shadeYpixel))
        #Draw the cell itself
        pygame.draw.rect(self.screen, WHITE, CELL_SIZE.move(Xpixel, Ypixel))
        #Draw what's in this cell
        if currentLoc.constr != None:
            self.drawConstruction(currentLoc.constr, (col, row))
        if currentLoc.ant != None:
            self.drawAnt(currentLoc.ant, (col, row))
    ##
    #drawBoard
    #Description: This is the bread and butter of the UserInterface class. Everything
    #   starts drawing from here.
    #
    #Parameters:
    #   currentState - 
    def drawBoard(self, currentState, mode):
        self.handleEvents(mode)
        if mode == TOURNAMENT_MODE:
            self.screen.fill(WHITE)
            #Draw the box into which the user can enter the number of games they want to play.
            self.drawTextBox()
            #Draw the table with columns author/win/loss/tie
            self.drawTable()
        else:
            self.screen.fill(BLACK)
            pygame.draw.rect(self.screen, WHITE, self.buttonArea)
            for col in xrange(0, len(currentState.board)):
                for row in xrange(0, len(currentState.board[col])):
                    self.drawCell(currentState.board[col][row])
            #Make sure we draw the right buttons
            relButtons = {} if mode == None else self.humanButtons if mode == HUMAN_MODE else self.aiButtons
            if self.buildAntMenu == True:
                relButtons = self.antButtons
            #Draw the context buttons
            for key in relButtons:
                self.drawButton(key, relButtons)
            #I can't put this draw method outside of drawBoard, but it shouldn't work this way.
            self.drawScoreBoard(currentState.inventories[0].foodCount, currentState.inventories[1].foodCount)
            #Draw notifications just above menu buttons.
            self.drawNotification()
        #Draw the basic buttons
        for key in self.buttons:
            self.drawButton(key, self.buttons)
        #Show everything I've drawn by posting self.screen to the monitor.
        pygame.display.flip()
    
    ##
    #handleButton
    #Description: Handles the finer details of what happens when a user is clicking on buttons.
    #   The button will only be counted as clicked if the user both presses and releases a mouse
    #   button while hovering over the game button. If clicked, a callback function will be used
    #   to notify Game.py.
    #
    #Parameters:
    #   key - a key in the self.buttons hash table, known in Python as a Dictionary.
    #   released - an integer/boolean that represents the state of the button: 1 if the button
    #   is released, or 0 if the button is depressed.
    ##
    def handleButton(self, key, released, buttons):
        if buttons[key][1] != released and released == 1:
            buttons[key][2]()
        
        buttons[key][1] = released
    
    ##
    #handleEvents
    #Description: Handles the more generic mouse movements. Finds out what has been
    #   clicked, and either calls handleButton on the activated button, or uses a
    #   callback to tell the HumanPlayer what the human clicked.
    ##
    def handleEvents(self, mode):
        #Make sure we check the right buttons
        relButtons = {} if self.choosingAIs else self.humanButtons if mode == HUMAN_MODE else self.aiButtons if mode == AI_MODE else {}
        #It should be impossible for self.buildAntMenu to be True unless mode is HUMAN_MODE and AIs have already been chosen.
        if mode == HUMAN_MODE and self.buildAntMenu:
            relButtons = self.antButtons
        #Check what to do for each event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                #Start by checking the basic buttons that always get drawn
                for key in self.buttons:
                    if self.buttonRect.move(self.buttons[key][0]).collidepoint(event.pos):
                        self.handleButton(key, 0, self.buttons)
                #Then check the buttons that congregate at the top of the screen, and change based on context
                for key in relButtons:
                    if self.buttonRect.move(relButtons[key][0]).collidepoint(event.pos):
                        self.handleButton(key, 0, relButtons)
                #Check to see if text box should be selected or deselected
                if mode == TOURNAMENT_MODE and self.buttonRect.move(self.textPosition).collidepoint(pygame.mouse.get_pos()):
                    self.boxSelected = True
                else:
                    self.boxSelected = False
                #Additionally, check if a cell on the board has been clicked.
                if mode != TOURNAMENT_MODE and not self.choosingAIs:
                    if event.pos[0] % (CELL_SPACING + CELL_SIZE.width) > CELL_SPACING and event.pos[1] % (CELL_SPACING + CELL_SIZE.height) > CELL_SPACING:
                        x = event.pos[0] / (CELL_SPACING + CELL_SIZE.width)
                        y = event.pos[1] / (CELL_SPACING + CELL_SIZE.height)
                        if x < BOARD_SIZE.width and y < BOARD_SIZE.height:
                            self.locationClicked((x, y))
                elif self.choosingAIs:
                    if event.pos[0] % 10:
                        pass
            elif event.type == pygame.MOUSEBUTTONUP:
                #Start by checking the basic buttons that always get drawn
                for key in self.buttons:
                    if self.buttonRect.move(self.buttons[key][0]).collidepoint(event.pos):
                        self.handleButton(key, 1, self.buttons)
                #Then check the buttons that congregate at the top of the screen, and change based on context
                for key in relButtons:
                    if self.buttonRect.move(relButtons[key][0]).collidepoint(event.pos):
                        self.handleButton(key, 1, relButtons)
                #Check to see if text box should be selected or deselected
                if mode == TOURNAMENT_MODE and self.buttonRect.move(self.textPosition).collidepoint(pygame.mouse.get_pos()):
                    boxSelected = True
                else:
                    boxSelected = False
            elif event.type == pygame.MOUSEMOTION and event.buttons[0]:
                #Start by checking the basic buttons that always get drawn
                for key in self.buttons:
                    if self.buttonRect.move(self.buttons[key][0]).collidepoint(addCoords(event.pos, event.rel)):
                        self.buttons[key][1] = 0
                    else:
                        self.buttons[key][1] = 1
                #Then check the buttons that congregate at the top of the screen, and change based on context
                for key in relButtons:
                    if self.buttonRect.move(relButtons[key][0]).collidepoint(addCoords(event.pos, event.rel)):
                        relButtons[key][1] = 0
                    else:
                        relButtons[key][1] = 1
            elif self.boxSelected and event.type == KEYDOWN:
                if str(event.unicode) in [str(i) for i in range(0, 10)]:
                    self.textBoxContent += str(event.unicode)
                elif event.key == 8 and self.textBoxContent != '':
                    self.textBoxContent = self.textBoxContent[:-1]
    
    def findButtonCoords(self, index, isTop):
        buttonSpacing = 2 * CELL_SPACING
        buttonX = self.screen.get_width() - self.buttonRect.width - buttonSpacing
        if isTop:
            buttonY = (index + 1) * buttonSpacing + index * self.buttonRect.height
            return buttonX, buttonY
        else:
            buttonY = self.screen.get_height() - (index + 1) * (buttonSpacing + self.buttonRect.height)
            return buttonX, buttonY
    
    def initAssets(self):
        global CELL_SIZE
        #Declare the name of the folder that all textures are in.
        texFolder = "Textures"
        #Load textures as Surfaces. Should convert these surfaces later for optimal speed.
        self.constructionTexs = []
        self.constructionTexs.append(pygame.image.load(os.path.join(texFolder, "anthill.bmp")))
        self.constructionTexs.append(pygame.image.load(os.path.join(texFolder, "antTunnel.bmp")))
        self.constructionTexs.append(pygame.image.load(os.path.join(texFolder, "grass.bmp")))
        self.constructionTexs.append(pygame.image.load(os.path.join(texFolder, "food.bmp")))
        self.antTexs = []
        self.antTexs.append(pygame.image.load(os.path.join(texFolder, "queen.bmp")))
        self.antTexs.append(pygame.image.load(os.path.join(texFolder, "worker.bmp")))
        self.antTexs.append(pygame.image.load(os.path.join(texFolder, "drone.bmp")))
        self.antTexs.append(pygame.image.load(os.path.join(texFolder, "direct.bmp")))
        self.antTexs.append(pygame.image.load(os.path.join(texFolder, "indirect.bmp")))
        #Load isCarrying and hasMoved textures, which will allow players to see the conditions of their ants.
        self.isCarryingTex = pygame.image.load(os.path.join(texFolder, "isCarrying.bmp"))
        self.hasMovedTex = pygame.image.load(os.path.join(texFolder, "hasMoved.bmp"))
        #CheckBox textures
        self.checkBoxTextures = []
        self.checkBoxTextures.append(pygame.image.load(os.path.join(texFolder, "unchecked.bmp")))
        self.checkBoxTextures.append(pygame.image.load(os.path.join(texFolder, "checked.bmp")))
        #CheckBox rectangle
        self.checkBoxRect = self.checkBoxTextures[0].get_rect()
        #Button textures
        self.buttonTextures = []
        self.buttonTextures.append(pygame.image.load(os.path.join(texFolder, "buttonDown.bmp")))
        self.buttonTextures.append(pygame.image.load(os.path.join(texFolder, "buttonUp.bmp")))
        #Button rectangle
        self.buttonRect = self.buttonTextures[0].get_rect()
        #Make CELL_SIZE equal to the size of an ant image.
        CELL_SIZE = self.constructionTexs[0].get_rect()
        #Make White transparent (alpha 0) for all textures (well, buttons don't actually need it).
        for construction in self.constructionTexs:
            construction.set_colorkey(WHITE)
        for ant in self.antTexs:
            ant.set_colorkey(WHITE)
        self.isCarryingTex.set_colorkey(WHITE)
        self.hasMovedTex.set_colorkey(GREY)
        self.hasMovedTex.set_alpha(50)
        #Set up fonts.
        pygame.font.init()
        self.gameFont = pygame.font.Font(None, 25)
        self.notifyFont = pygame.font.Font(None, 15)
        #Where should scores be drawn?
        self.scoreLocation = self.findButtonCoords(5, True)
        #Where should notifications be drawn?
        self.messageLocation = self.findButtonCoords(4, False)
        #Where should non-board stuff be placed (an area for buttons, notifications, and scores)?
        buttonAreaWidth = self.buttonRect.width + 4 * CELL_SPACING
        self.buttonArea = Rect(self.screen.get_width() - buttonAreaWidth, 0, buttonAreaWidth, self.screen.get_height())
        #Button statistics for basic buttons in order: x, y, buttonState(pressed/released)
        self.buttons = {
        'Start':[self.findButtonCoords(3.5, False), 1, self.startGame],
        'Tournament':[self.findButtonCoords(2, False), 1, self.gameModeTournament],
        'Human vs AI':[self.findButtonCoords(1, False), 1, self.gameModeHumanAI],
        'AI vs AI':[self.findButtonCoords(0, False), 1, self.gameModeAIAI]
        }
        #Initial values for buttons in human vs AI mode
        self.humanButtons = {
        'Move':[self.findButtonCoords(0, True), 1, self.submitMove],
        'Build':[self.findButtonCoords(1, True), 1, self.submitBuild],
        'End':[self.findButtonCoords(2, True), 1, self.submitEndTurn]
        }
        #Initial values for buttons in human vs AI mode
        self.aiButtons = {
        'Next':[self.findButtonCoords(0, True), 1, self.submitNext],
        'Continue':[self.findButtonCoords(1, True), 1, self.submitContinue]
        }
        #Initial values for build ant buttons
        self.antButtons = {
        'Worker':[self.findButtonCoords(0, True), 1, self.submitWorker],
        'Drone':[self.findButtonCoords(1, True), 1, self.submitDrone],
        'D_Soldier':[self.findButtonCoords(2, True), 1, self.submitDSoldier],
        'I_Soldier':[self.findButtonCoords(3, True), 1, self.submitISoldier],
        'None':[self.findButtonCoords(4, True), 1, self.submitNoBuild]
        }
        #Properties of our single text box
        self.textPosition = self.findButtonCoords(2, True)
        self.textBoxContent = ''
        self.boxSelected = False
        #Initial vaue for callback function that will be used to get cell clicks in game
        self.locationCallback = self.locationClicked
        #Draw the ant build menu?
        self.buildAntMenu = False
        #Initial user notification is empty, since we assume the user hasn't made a mistake in opening the program. Not that the program could detect that anyway.
        self.lastNotification = None
        #Initial coordList so I know what to shade
        self.coordList = []
        #Cells that should be highlighted for attacks
        self.attackList = []
        #Initializing tournament scores
        self.tournamentScores = []
        #Find out if user is choosing AIs
        self.choosingAIs = False