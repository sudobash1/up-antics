##
#UserInterface
#Description: This class renders the game board through pygame library method calls
#
##
import pygame
from pygame.locals import *

WHITE = (255, 255, 255)
CELL_SIZE = (10,10)

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
        for key in buttons:
            drawButton(buttons[key][:2], buttons[2])
        pygame.display.flip()
    
    def drawConstruction(self, item, position):
        Xpixel = 10 * (position[1] + 1) + CELL_SIZE[0] * position[1]
        Ypixel = 10 * (position[0] + 1) + CELL_SIZE[1] * position[0]
        screen.blit(constructions[item.type], (Xpixel, Ypixel))
    
    def drawAnt(self, ant, position):
        Xpixel = 10 * (position[1] + 1) + CELL_SIZE[0] * position[1]
        Ypixel = 10 * (position[0] + 1) + CELL_SIZE[1] * position[0]
        screen.blit(ants[ant.type], (Xpixel, Ypixel))
    
    def initAssets(self):
        #Load textures as Surfaces.
        self.grass = pygame.image.load("grass.bmp")
        self.ant = pygame.image.load("ant.bmp")
        #Make CELL_SIZE equal to the size of an ant image.
        CELL_SIZE = (ant.get_width(), ant.get_height())
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
        
