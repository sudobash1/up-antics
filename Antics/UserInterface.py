f##
#UserInterface
#Description: This class renders the game board through pygame library method calls
#
##
import pygame
from pygame.locals import *

WHITE = (255, 255, 255)

class UserInterface:
    def __init__(self, inputSize):
        self.screen = pygame.display.set_mode(inputSize)
    
    def drawBoard(self, currentState):
        for row in len(currentState.board):
            for col in len(currentState.board[row]):
                currentLoc = currentState.board[row][col]
                if currentLoc.constr != None:
                    drawConstruction(currentLoc.constr, (row, col))
                if currentLoc.ant != None:
                    drawAnt(currentLoc.ant, (row, col))
        pygame.display.flip()
    
    def drawConstruction(self, item, position):
    
    def drawAnt(self, ant, position):
        Xpixel = 
        screen.blit(ants[ant.type], )
    
    def initAssets(self):
        #Load textures as Surfaces.
        self.grass = pygame.image.load("grass.bmp")
        self.ant = pygame.image.load("ant.bmp")
        #Make White transparent (alpha 0) for all textures.
        grass.set_colorkey(WHITE)
        ant.set_colorkey(WHITE)
        #Set up fonts.
        pygame.font.init()
        self.gameFont = pygame.font.Font(None, 25)
        #Button statistics in order: x, y, buttonState(pressed/released)
        buttons = {
        'move':(700,10, 1),
        'wait':(700,60, 1),
        'end':(700,110, 1),
        'tournament':(700,510, 1),
        'human':(700,540, 1),
        'ai':(700,570, 1),
        'load':(700,600, 1),
        'start':(700,650, 1)
        }
        
