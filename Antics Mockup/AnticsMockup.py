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
grass.set_colorkey(WHITE)
ant = pygame.image.load("ant.bmp")
ant.set_colorkey(WHITE)
anthill = pygame.image.load("anthill.bmp")
anthill.set_colorkey(WHITE)
pressed = pygame.image.load("buttonDown.bmp")
pressed.set_colorkey(WHITE)
released = pygame.image.load("buttonUp.bmp")
released.set_colorkey(WHITE)
checked = pygame.image.load("checked.bmp")
checked.set_colorkey(WHITE)
unchecked = pygame.image.load("unchecked.bmp")
unchecked.set_colorkey(WHITE)
#Set up variables
pygame.font.init()
gameFont = pygame.font.Font(None, 25)
typeToDraw = 1
buttonLocations = {
'move':(700,10),
'wait':(700,60),
'end':(700,110),
'tournament':(700,510),
'human':(700,540),
'ai':(700,570),
'load':(700,600),
'start':(700,650)
}
coloredSquares = []
#text that's beeen entered into the text box
textEntry = '9702'
boxSelected = False
boxRect = Rect(700, 240, 150, 30)
cursorRect = Rect(0, 0, 2, 20)
#Initialize board
board = [[None for y in xrange(bHeight)] for x in xrange(bWidth)]
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
    global typeToDraw, coloredSquares, boxSelected, textEntry
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == MOUSEBUTTONDOWN or event.type == MOUSEBUTTONUP:
            if boxRect.collidepoint(pygame.mouse.get_pos()):
                boxSelected = True
            else:
                boxSelected = False
        if boxSelected and event.type == KEYDOWN:
            if str(event.unicode) in [str(i) for i in xrange(0, 10)]:
                textEntry += str(event.unicode)
            elif event.key == 8 and textEntry != '':
                textEntry = textEntry[:-1]
            print "DOWN unicode: " + str(event.unicode) + ", key: " + str(event.key) + " and mod: " + str(event.mod)
        if boxSelected and event.type == KEYUP:
            print "UP key: " + str(event.key) + " and mod: " + str(event.mod)
        if event.type == MOUSEBUTTONDOWN:
            if released.get_rect().move(buttonLocations['start']).collidepoint(pygame.mouse.get_pos()):
                typeToDraw = 2
            spotClicked = clickedSquare()
            if spotClicked != None:
                if spotClicked in coloredSquares:
                    coloredSquares.remove(spotClicked)
                else:
                    coloredSquares.append(spotClicked)
        elif event.type == MOUSEBUTTONUP:
            typeToDraw = 1

def clickedSquare():
    pos = pygame.mouse.get_pos()
    if pos[0] > 10 and pos[1] > 10 and pos[0] < (74 + 68*bWidth) and pos[1] < (74 + 68*bHeight):
        if (pos[0]-10)%68 < 64 and (pos[1]-10)%68 < 64:
            return ((pos[0]-10)/68, (pos[1]-10)/68)

def drawTextBox():
    textBoxPosition = (710, 250)
    pygame.draw.rect(screen, WHITE, boxRect)
    label = gameFont.render(textEntry + ('|' if boxSelected else ''), True, BLACK)
    screen.blit(label, textBoxPosition)
    # if boxSelected:
        # pygame.draw.rect(screen, BLACK, cursorRect.move(textBoxPosition).move(label.get_width() + 10, 0))

def drawCheckBox(screen, text, boxSurface, location):
    #Create the surface containing the text.
    textSurface = gameFont.render(text, True, RED)
    #Find the y center of the check box, and the left side.
    tempRect = boxSurface.get_rect()
    boxCenter = (tempRect.width, tempRect.height/2)
    #Find the y center of the text.
    tempRect = textSurface.get_rect()
    textCenterY = tempRect.height/2
    #Use the above info to find the amount the text must be offset to appear to the right of the check box.
    offset = (boxCenter[0], boxCenter[1]-textCenterY)
    #Render the button
    screen.blit(boxSurface, location)
    #render the text atop the button
    screen.blit(textSurface, (location[0]+offset[0],location[1]+offset[1]))

def drawButton(screen, text, buttonSurface, location):
    #Create the surface containing the text.
    textSurface = gameFont.render(text, True, BLACK)
    #Find the center of the button.
    tempRect = buttonSurface.get_rect()
    buttonCenter = (tempRect.width/2, tempRect.height/2)
    #Find the center of the text.
    tempRect = textSurface.get_rect()
    textCenter = (tempRect.width/2, tempRect.height/2)
    #Use the above info to find the amount the text must be offset to appear in the button.
    offset = (buttonCenter[0]-textCenter[0], buttonCenter[1]-textCenter[1])
    #Render the button
    screen.blit(buttonSurface, location)
    #render the text atop the button
    screen.blit(textSurface, (location[0]+offset[0],location[1]+offset[1]))

#All that other stuff
screen = pygame.display.set_mode(size)
while 1:
    handleEvents()
    screen.fill(BLACK)
    drawTextBox()
    if typeToDraw == 1:
        drawButton(screen, "Start Game", released, buttonLocations['start'])
    else:
        drawButton(screen, "Start Game", pressed,  buttonLocations['start'])
    drawButton(screen, "Load AI", released,  buttonLocations['load'])
    drawButton(screen, "Move", released,  buttonLocations['move'])
    drawButton(screen, "Wait", released,  buttonLocations['wait'])
    drawButton(screen, "End Turn", released,  buttonLocations['end'])
    drawCheckBox(screen, "Tournament", checked,  buttonLocations['tournament'])
    drawCheckBox(screen, "AI vs. AI", unchecked,  buttonLocations['human'])
    drawCheckBox(screen, "Human vs. AI", unchecked,  buttonLocations['ai'])
    pygame.draw.rect(screen, WHITE, Rect(700, 160, 150, 55))
    screen.blit(gameFont.render("Food: 14", True, BLACK), (720, 180))
    for y in xrange(0, bHeight):
        for x in xrange(0, bWidth):
            rectangle = Rect(10+68*x, 10+68*y, 64, 64)
            if board[x][y] == None:
                pygame.draw.rect(screen, GREEN if (x,y) in coloredSquares else WHITE, rectangle)
            else:
                pygame.draw.rect(screen, GREEN if (x,y) in coloredSquares else WHITE, rectangle)
                screen.blit(board[x][y], rectangle)
    pygame.display.flip()