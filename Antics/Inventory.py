##
#Inventory
#Description: This class keeps track of the resources at a player's disposal
#
#Variables
#   player - The id of the player that this inventory belongs to
#   ants - The ants belonging to the player
#    queen - The Player's queen Ant
#    anthill - The player's anthill
#    constructions - An array of all the Player's Constructions
#   foodCount - The amount of food that the player has to use
##
class Inventory:

    ##
    #__init__
    #Description: Creates a new Inventory
    #Parameters:
    #   playerId - The id of the player that owns the Inventory (int)
    #   antArray - An array containing the Player's Ants (Ant[])
    #   inputFood - The amount of food in the Inventory (int)
    #   inputConstructions - An array containing all of the Player's Constructions (Construction[])
    ##
    def __init__(self, playerId, antArray, inputConstructions, inputFood):
        self.player = playerId
        self.foodCount = inputFood
        self.ants = antArray
        self.queen = self.findQueen(antArray)
        self.constructions = inputConstructions
        self.anthill = self.findAnthill(inputConstructions)
        
    def findQueen(self, antArr):
        if antArr == None:
            return None
        
        for checkAnt in antArr:
            if checkAnt.type == Ant.QUEEN: return checkAnt
            
        return None
        
    def findAnthill(self, constructionArr):
        if constructionArr == None:
            return None
        
        for checkConstruction in constructionArr:
            if checkConstruction.type == Building.ANTHILL: return checkConstruction
            
        return None
