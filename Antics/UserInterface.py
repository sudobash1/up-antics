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
RED = (150, 0, 0)
CELL_SIZE = Rect(0,0,10,10)
BOARD_SIZE = Rect(0,0,10,10)
CELL_SPACING = 10

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
    
    def locationClicked(self, coords):
        print "Clicked LOCATION " + str(coords)
    
    def notify(self, message):
        self.lastNotification = message
    
    def drawNotification(self):
        messageSurface = self.notifyFont.render(self.lastNotification, True, RED)
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
    def drawButton(self, key):
        label = self.gameFont.render(key, True, BLACK)
        offset = subtractCoords(self.buttonRect.center, label.get_rect().center)
        self.screen.blit(self.buttonTextures[self.buttons[key][2]], self.buttons[key][:2])
        self.screen.blit(label, addCoords(self.buttons[key][:2], offset))
    
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
    def handleButton(self, key, released):
        if self.buttons[key][2] != released and released == 1:
            self.buttons[key][3]()
        
        self.buttons[key][2] = released
    
    ##
    #handleEvents
    #Description: Handles the more generic mouse movements. Finds out what has been
    #   clicked, and either calls handleButton on the activated button, or returns
    #   the board coordinates of the cell that was clicked.
    ##
    def handleEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for key in self.buttons:
                    if self.buttonRect.move(self.buttons[key][:2]).collidepoint(event.pos):
                        self.handleButton(key, 0)
                #Additionally, check if a cell on the board has been clicked.
                if event.pos[0] % (CELL_SPACING + CELL_SIZE.width) > CELL_SPACING and event.pos[1] % (CELL_SPACING + CELL_SIZE.height) > CELL_SPACING:
                    x = event.pos[0] / (CELL_SPACING + CELL_SIZE.width)
                    y = event.pos[1] / (CELL_SPACING + CELL_SIZE.height)
                    if x < BOARD_SIZE.width and y < BOARD_SIZE.height:
                        self.locationClicked((x, y))
            elif event.type == pygame.MOUSEBUTTONUP:
                for key in self.buttons:
                    if self.buttonRect.move(self.buttons[key][:2]).collidepoint(event.pos):
                        self.handleButton(key, 1)
            elif event.type == pygame.MOUSEMOTION and event.buttons[0]:
                for key in self.buttons:
                    if self.buttonRect.move(self.buttons[key][:2]).collidepoint(addCoords(event.pos, event.rel)):
                        self.buttons[key][2] = 0
                    else:
                        self.buttons[key][2] = 1
    
    ##
    #drawBoard
    #Description: This is the bread and butter of the UserInterface class. Everything
    #   starts drawing from here.
    #
    #Parameters:
    #   currentState - 
    def drawBoard(self, currentState):
        self.handleEvents()
        self.screen.fill(WHITE)
        for col in xrange(0, len(currentState.board)):
            for row in xrange(0, len(currentState.board[col])):
                currentLoc = currentState.board[col][row]
                if currentLoc.constr != None:
                    self.drawConstruction(currentLoc.constr, (col, row))
                if currentLoc.ant != None:
                    self.drawAnt(currentLoc.ant, (col, row))
        for key in self.buttons:
            self.drawButton(key)
        #I can't put this draw method outside of drawBoard, but it shouldn't work this way.
        self.drawScoreBoard(currentState.inventories[0].foodCount, currentState.inventories[1].foodCount)
        #Draw notifications just above menu buttons.
        self.drawNotification()
        pygame.display.flip()
    
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
        self.scoreLocation = (800, 160)
        #Where should notifications be drawn?
        self.messageLocation = (800, 400)
        #Button statistics in order: x, y, buttonState(pressed/released)
        self.buttons = {
        'move':[800,10, 1, self.submitMove],
        'build':[800,60, 1, self.submitBuild],
        'end':[800,110, 1, self.submitEndTurn],
        'tournament':[800,450, 1, self.gameModeTournament],
        'human':[800,500, 1, self.gameModeHumanAI],
        'ai':[800,550, 1, self.gameModeAIAI],
        'start':[800,650, 1, self.startGame]
        }
        #Initial vaue for callback function that will be used to get cell clicks in game
        self.locationCallback = self.locationClicked
        #Intial user notification is empty, since we assume the user hasn't made a mistake in opening the program. Not that the program could detect that anyway.
        self.lastNotification = None