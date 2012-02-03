class Ant:
    def __init__(self, inputId, inputCoords, inputType):
        self.id = inputId
        self.coords = inputCoords
        self.type = inputType
        self.alive = True
        self.carrying = False

    def die(self):
        self.alive = False