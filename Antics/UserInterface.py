##
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
        
        pygame.display.flip()
    
    def initAssets(self):
        self.grass = pygame.image.load("grass.bmp")
        grass.set_colorkey(WHITE)
        self.ant = pygame.image.load("ant.bmp")
        ant.set_colorkey(WHITE)
        pygame.font.init()
        self.gameFont = pygame.font.Font(None, 25)
        #buttons in order: x, y, buttonState
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
