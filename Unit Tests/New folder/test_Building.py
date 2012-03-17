def runTest(Building):
    testBuilding = Building.Building((2,3), Building.ANTHILL,1)
    testBuilding.player =2
    if testBuilding.player !=2:
        raise Exception("Player was not changed successfully")
    testBuilding.inputCoords = (4,5)

