def runTest(Ant):
    testAnt = Ant.Ant((2,3), Ant.QUEEN,1)
    if testAnt.alive != True: 
        raise Exception("Ant was created dead")
    if testAnt.carrying != False: 
        raise Exception("Ant was created carrying food")
    testAnt.die()
    if testAnt.alive == True:
        raise Exception("Die function does not work properly")
    testAnt.carrying = True
    if testAnt.carrying != True: 
        raise Exception("Giving ant a load to carry gave it no load to carry")