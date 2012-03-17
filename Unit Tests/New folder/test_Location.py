def runTest(Location):
    import Ant
    import Construction
    ant1 = Ant.Ant((2,3), Ant.QUEEN, 1)
    ant2 = Ant.Ant((5,6), Ant.WORKER, 1)
    construction1 = Construction.Construction((3,4), Construction.TUNNEL)
    testLocation = Location.Location((2,3))
    testLocation2 = Location.Location((4,5))
    testLocation.ant = ant1
    testLocation.constr = construction1
    if(testLocation.ant == None):
        raise Exception ("Ant is not found at a location where there should be an Ant")
    if(testLocation.constr == None):
        raise Exception("Construction is not found at a location where they should be a Construction")
    if(testLocation2.ant != None):
        raise Exception ("Ant is found at a location where there is no Ant")
    if(testLocation2.constr != None):
        raise Exception ("Construction is found at a location where there is not Construction")
    locationClone = testLocation.clone()
    if locationClone == testLocation:
        raise Exception("The cloned location is equal to the original")
    if locationClone.ant != testLocation.ant:
        raise Exception("The cloned location does not have the same ant object as the original location")
    if locationClone.constr != testLocation.constr:
        raise Exception("The cloned location does not have the same construction as the original location")
    locationClone.ant = ant2
    if locationClone.ant == testLocation.ant:
        raise Exception("The ant on the cloned location has been changed but is not recognized as different from the original location")
