import pygame, sys, random
from pygame.locals import *
#Really? No buttons?
size = width, height = 900, 700
bSize = bWidth, bHeight = 10, 10
BLACK = 0, 0, 0
WHITE = 255, 255, 255
RED = 255, 0, 0
GREEN = 0, 255, 0
BLUE = 0, 0, 255
#Load images
grass = pygame.image.load("grass.bmp")
ant = pygame.image.load("ant.bmp")
anthill = pygame.image.load("anthill.bmp")
pressed = pygame.image.load("pressed.bmp")
released = pygame.image.load("released.bmp")
#Set up variables
typeToDraw = 1
buttonRect = pressed.get_rect().move(700,330)
#Initialize board
board = []
for x in xrange(0, bWidth):
    board.append([])
    for y in xrange(0, bHeight):
        board[x].append(None)
#Choose where to place grass.
grasses = []
while len(grasses) < bWidth*bHeight*0.2:
    x = int(random.random()*10)
    y = int(random.random()*10)
    if board[x][y] == None:
        grasses.append([x,y])
        board[x][y] = grass
#Choose where to place ants.
ants = []
while len(ants) < bWidth*bHeight*0.05:
    x = int(random.random()*10)
    y = int(random.random()*10)
    if board[x][y] == None:
        ants.append([x,y])
        board[x][y] = ant
#Choose where to place anthills.
anthills = []
while len(anthills) < 2:
    x = int(random.random()*10)
    y = int(random.random()*10)
    if board[x][y] == None:
        anthills.append([x,y])
        board[x][y] = anthill
#Remember to mess with locks. Do I need to lock the surface used in the pygame intro?
#Answer: No. Not without hardware acceleration (I think). Current Surfaces are software Surfaces.

#Event handler
def handleEvents():
    global typeToDraw
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == MOUSEBUTTONDOWN:
            if buttonRect.collidepoint(pygame.mouse.get_pos()):
                typeToDraw = 2
        elif event.type == MOUSEBUTTONUP:
            typeToDraw = 1

#All that other stuff
screen = pygame.display.set_mode(size)
while 1:
    handleEvents()
    screen.fill(BLACK)
    if typeToDraw == 1:
        screen.blit(released, buttonRect)
    else:
        screen.blit(pressed, buttonRect)
    for y in xrange(0, bHeight):
        for x in xrange(0, bWidth):
            rectangle = Rect(10+68*x, 10+68*y, 64, 64)
            if board[x][y] == None:
                pygame.draw.rect(screen, WHITE, rectangle)
            else:
                screen.blit(board[x][y], rectangle)
    pygame.display.flip()