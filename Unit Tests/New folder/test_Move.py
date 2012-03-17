def runTest(Move):
    testMove = Move.Move(0, [(1,2), (1,3)], None)
    testMove.moveType = 2 
    if testMove.moveType != 2:
        raise Exception ("Move type was changed and change is not exhibited")
    testMove.coordList = [(1,3), (1,4)]
    if testMove.coordList != [(1,3), (1,4)]:
        raise Exception("Coordinate path was changed and change is not exhibited")
    