##
#UserInterface
#Description: This class renders the game board through pygame library method calls
#
##
import pygame, os, sys
from pygame.locals import *

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CELL_SIZE = Rect(0,0,10,10)
CELL_SPACING = 10
#Board size is in cells, not pixels.
BOARD_SIZE = Rect(0,0,10,10)

def add(tuple1, tuple2):
    if len(tuple1) != len(tuple2):
        return None
    else:
        return tuple([tuple1[i] + tuple2[i] for i in range(0, len(tuple1))])

def subtract(tuple1, tuple2):
    if len(tuple1) != len(tuple2):
        return None
    else:
        return tuple([tuple1[i] - tuple2[i] for i in range(0, len(tuple1))])

class UserInterface:
    def __init__(self, inputSize):
        self.screen = pygame.display.set_mode(inputSize)
    
    def submitMove(self):
        print "Clicked SUBMIT MOVE"
    
    def submitWait(self):
        print "Clicked SUBMIT WAIT"
    
    def submitEndTurn(self):
        print "Clicked SUBMIT END TURN"
    
    def gameModeTournament(self):
        print "Clicked GAME MODE TOURNAMENT"
    
    def gameModeHumanAI(self):
        print "Clicked GAME MODE HUMAN AI"
    
    def gameModeAIAI(self):
        print "Clicked GAME MODE AI AI"
    
    def loadAI(self):
        print "Clicked LOAD AI"
    
    def startGame(self):
        print "Clicked START GAME"
    
    def drawConstruction(self, item, position):
        Xpixel = CELL_SPACING * (position[1] + 1) + CELL_SIZE.width * position[1]
        Ypixel = CELL_SPACING * (position[0] + 1) + CELL_SIZE.height * position[0]
        self.screen.blit(self.constructions[item.type], (Xpixel, Ypixel))
    
    def drawAnt(self, ant, position):
        Xpixel = CELL_SPACING * (position[1] + 1) + CELL_SIZE.width * position[1]
        Ypixel = CELL_SPACING * (position[0] + 1) + CELL_SIZE.height * position[0]
        self.screen.blit(self.ants[ant.type], (Xpixel, Ypixel))
    
    def drawButton(self, key):
        label = self.gameFont.render(key, True, BLACK)
        offset = subtract(self.buttonRect.center, label.get_rect().center)
        self.screen.blit(self.buttonTextures[self.buttons[key][2]], self.buttons[key][:2])
        self.screen.blit(label, add(self.buttons[key][:2], offset))
    
    def drawScoreBoard(self, player1Score, player2Score):
        label1 = self.gameFont.render("Player 1: " + str(player1Score) + " Food", True, BLACK)
        label2 = self.gameFont.render("Player 2: " + str(player2Score) + " Food", True, BLACK)
        scoreLocation = (700, 160)
        self.screen.blit(label1, scoreLocation)
        self.screen.blit(label2, add(scoreLocation, (0, label2.get_rect().height)))
        

    def handleButton(self, key, released):
        if self.buttons[key][2] != released and released == 1:
            self.buttons[key][3]()
        
        self.buttons[key][2] = released
    
    def handleEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for key in self.buttons:
                    if self.buttonRect.move(self.buttons[key][:2]).collidepoint(event.pos):
                        self.handleButton(key, 0)
            elif event.type == pygame.MOUSEBUTTONUP:
                for key in self.buttons:
                    if self.buttonRect.move(self.buttons[key][:2]).collidepoint(event.pos):
                        self.handleButton(key, 1)
            elif event.type == pygame.MOUSEMOTION and event.buttons[0]:
                for key in self.buttons:
                    if self.buttonRect.move(self.buttons[key][:2]).collidepoint(add(event.pos, event.rel)):
                        self.handleButton(key, 0)
                    else:
                        self.handleButton(key, 1)
        
    def drawBoard(self, currentState):
        self.handleEvents()
        self.screen.fill(WHITE)
        for row in xrange(0, len(currentState.board)):
            for col in xrange(0, len(currentState.board[row])):
                currentLoc = currentState.board[row][col]
                if currentLoc.constr != None:
                    self.drawConstruction(currentLoc.constr, (row, col))
                if currentLoc.ant != None:
                    self.drawAnt(currentLoc.ant, (row, col))
        for key in self.buttons:
            self.drawButton(key)
        #I can't put this draw method outside of drawBoard, but it shouldn't work this way.
        self.drawScoreBoard(1,2)
        pygame.display.flip()
    
    def initAssets(self):
        global CELL_SIZE
        #Declare the name of the folder that all textures are in.
        texFolder = "Textures"
        #Load textures as Surfaces. Should convert these surfaces later for optimal speed.
        self.grass = pygame.image.load(os.path.join(texFolder, "grass.bmp"))
        self.ants = []
        self.ants.append(pygame.image.load(os.path.join(texFolder, "ant.bmp")))
        #Button textures
        self.buttonTextures = []
        self.buttonTextures.append(pygame.image.load(os.path.join(texFolder, "buttonDown.bmp")))
        self.buttonTextures.append(pygame.image.load(os.path.join(texFolder, "buttonUp.bmp")))
        #Button rectangle
        self.buttonRect = self.buttonTextures[0].get_rect()
        #Make CELL_SIZE equal to the size of an ant image.
        CELL_SIZE = self.grass.get_rect()
        #Make White transparent (alpha 0) for all textures (well, buttons don't actually need it).
        self.grass.set_colorkey(WHITE)
        for ant in self.ants:
            ant.set_colorkey(WHITE)
        #Set up fonts.
        pygame.font.init()
        self.gameFont = pygame.font.Font(None, 25)
        #Button statistics in order: x, y, buttonState(pressed/released)
        self.buttons = {
        'move':[700,10, 1, self.submitMove],
        'wait':[700,60, 1, self.submitWait],
        'end':[700,110, 1, self.submitEndTurn],
        'tournament':[700,450, 1, self.gameModeTournament],
        'human':[700,500, 1, self.gameModeHumanAI],
        'ai':[700,550, 1, self.gameModeAIAI],
        'load':[700,600, 1, self.loadAI],
        'start':[700,650, 1, self.startGame]
        }
      
#Stuff that shouldn't exist in the final product.
#I'm using all this to check my drawboard method.
import GameState, Location, Inventory, Ant
a=UserInterface((860,700))
a.initAssets()
b = [[ Location.Location(True, 1, (row, col)) for col in xrange(0, BOARD_SIZE.width)] for row in xrange(0, BOARD_SIZE.height)]
b[0][0].ant = Ant.Ant(0, (0,0), 0, 0)
b[1][0].ant = Ant.Ant(0, (1,0), 0, 0)
c = GameState.GameState(b, "inventories", "phase")

while(True):
    a.drawBoard(c)