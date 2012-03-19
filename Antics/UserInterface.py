##
#UserInterface
#Description: This class renders the game board through pygame library method calls,
#   and handles user input events.
#
##
import pygame, os, sys
from pygame.locals import *

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
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
        self.screen.blit(self.constructions[item.type], (Xpixel, Ypixel))
    
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
        self.screen.blit(self.ants[ant.type], (Xpixel, Ypixel))
    
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
        label1 = self.gameFont.render("Player 1: " + str(player1Score) + " Food", True, BLACK)
        label2 = self.gameFont.render("Player 2: " + str(player2Score) + " Food", True, BLACK)
        self.screen.blit(label1, self.scoreLocation)
        self.screen.blit(label2, addCoords(self.scoreLocation, (0, label2.get_rect().height)))
        
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
    def handleEvents(self):
        for event in pygame.event.get():
            relButtons = self.antButtons if self.buildAntMenu else self.buttons
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for key in relButtons:
                    if self.buttonRect.move(relButtons[key][0]).collidepoint(event.pos):
                        self.handleButton(key, 0, relButtons)
                #Additionally, check if a cell on the board has been clicked.
                if event.pos[0] % (CELL_SPACING + CELL_SIZE.width) > CELL_SPACING and event.pos[1] % (CELL_SPACING + CELL_SIZE.height) > CELL_SPACING:
                    x = event.pos[0] / (CELL_SPACING + CELL_SIZE.width)
                    y = event.pos[1] / (CELL_SPACING + CELL_SIZE.height)
                    if x < BOARD_SIZE.width and y < BOARD_SIZE.height:
                        self.locationClicked((x, y))
            elif event.type == pygame.MOUSEBUTTONUP:
                for key in relButtons:
                    if self.buttonRect.move(relButtons[key][0]).collidepoint(event.pos):
                        self.handleButton(key, 1, relButtons)
            elif event.type == pygame.MOUSEMOTION and event.buttons[0]:
                for key in relButtons:
                    if self.buttonRect.move(relButtons[key][0]).collidepoint(addCoords(event.pos, event.rel)):
                        relButtons[key][1] = 0
                    else:
                        relButtons[key][1] = 1
    
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
    def drawBoard(self, currentState):
        self.handleEvents()
        self.screen.fill(BLACK)
        pygame.draw.rect(self.screen, WHITE, self.buttonArea)
        for col in xrange(0, len(currentState.board)):
            for row in xrange(0, len(currentState.board[col])):
                self.drawCell(currentState.board[col][row])
        #Make sure we draw the right buttons
        relButtons = self.antButtons if self.buildAntMenu else self.buttons
        for key in relButtons:
            self.drawButton(key, relButtons)
        #I can't put this draw method outside of drawBoard, but it shouldn't work this way.
        self.drawScoreBoard(currentState.inventories[0].foodCount, currentState.inventories[1].foodCount)
        #Draw notifications just above menu buttons.
        self.drawNotification()
        pygame.display.flip()
    
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
        self.constructions = []
        self.constructions.append(pygame.image.load(os.path.join(texFolder, "anthill.bmp")))
        self.constructions.append(pygame.image.load(os.path.join(texFolder, "antTunnel.bmp")))
        self.constructions.append(pygame.image.load(os.path.join(texFolder, "grass.bmp")))
        self.constructions.append(pygame.image.load(os.path.join(texFolder, "food.bmp")))
        self.ants = []
        self.ants.append(pygame.image.load(os.path.join(texFolder, "queen.bmp")))
        self.ants.append(pygame.image.load(os.path.join(texFolder, "worker.bmp")))
        self.ants.append(pygame.image.load(os.path.join(texFolder, "drone.bmp")))
        self.ants.append(pygame.image.load(os.path.join(texFolder, "direct.bmp")))
        self.ants.append(pygame.image.load(os.path.join(texFolder, "indirect.bmp")))
        #Button textures
        self.buttonTextures = []
        self.buttonTextures.append(pygame.image.load(os.path.join(texFolder, "buttonDown.bmp")))
        self.buttonTextures.append(pygame.image.load(os.path.join(texFolder, "buttonUp.bmp")))
        #Button rectangle
        self.buttonRect = self.buttonTextures[0].get_rect()
        #Make CELL_SIZE equal to the size of an ant image.
        CELL_SIZE = self.constructions[0].get_rect()
        #Make White transparent (alpha 0) for all textures (well, buttons don't actually need it).
        for construction in self.constructions:
            construction.set_colorkey(WHITE)
        for ant in self.ants:
            ant.set_colorkey(WHITE)
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
        #Button statistics in order: x, y, buttonState(pressed/released)
        self.buttons = {
        'move':[self.findButtonCoords(0, True), 1, self.submitMove],
        'build':[self.findButtonCoords(1, True), 1, self.submitBuild],
        'end':[self.findButtonCoords(2, True), 1, self.submitEndTurn],
        'tournament':[self.findButtonCoords(3, False), 1, self.gameModeTournament],
        'human':[self.findButtonCoords(2, False), 1, self.gameModeHumanAI],
        'ai':[self.findButtonCoords(1, False), 1, self.gameModeAIAI],
        'start':[self.findButtonCoords(0, False), 1, self.startGame]
        }
        #Initial vaue for callback function that will be used to get cell clicks in game
        self.locationCallback = self.locationClicked
        #Initial value for build ant menu
        self.antButtons = {
        'worker':[self.findButtonCoords(0, True), 1, self.submitWorker],
        'drone':[self.findButtonCoords(1, True), 1, self.submitDrone],
        'dsoldier':[self.findButtonCoords(2, True), 1, self.submitDSoldier],
        'isoldier':[self.findButtonCoords(3, True), 1, self.submitISoldier],
        'none':[self.findButtonCoords(4, True), 1, self.submitNoBuild]
        }
        #Draw the ant build menu?
        self.buildAntMenu = False
        #Initial user notification is empty, since we assume the user hasn't made a mistake in opening the program. Not that the program could detect that anyway.
        self.lastNotification = None
        #Initial coordList so I know what to shade
        self.coordList = []
        #Cells that should be highlighted for attacks
        self.attackList = []