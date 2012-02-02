class Ant:
    def __init__(self, inputId, inputCoords, inputType):
        self.id = inputId
        self.coords = inputCoords
        self.type = inputType
        self.alive = True
        self.carrying = False

    def getId(self):
        return self.id

    def getCoords(self):
        return self.coords

    def getType(self):
        return self.type

    def die(self):
        self.alive = False

    def isAlive(self):
        return self.alive

    def isCarrying(self):
        return self.carrying
