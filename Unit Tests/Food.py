##
#Food
#Description: The resource used to buy Ants and win through economic victory.
#
#Variables:
#   quantity - the number of Food items being represented.
##
class Food:

    ##
    #__init__
    #Description: Creates a new Food item
    #
    #Parameters:
    #   inputQuantity - The amount of Food to be represented by the Food item (int)
    ##
    def __init__(self, inputQuantity):
        self.quantity = inputQuantity