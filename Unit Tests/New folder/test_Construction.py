def runTest(Construction):
    testConstruction = Construction.Construction((2,3), Construction.TUNNEL)
    testConstruction.type = Construction.ANTHILL
    if testConstruction.type != Construction.ANTHILL:
        raise Exception("Type of Construction was not changed properly")
