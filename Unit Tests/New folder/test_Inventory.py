def runTest(Inventory):
  import Ant
  import Construction 
  ant1 = Ant.Ant((2,3), Ant.QUEEN, 1)
  ant2 = Ant.Ant((4,5), Ant.WORKER, 1)
  construction1 = Construction.Construction((3,4), Construction.TUNNEL)
  construction2 = Construction.Construction((1,2), Construction.ANTHILL)
  testInventory = Inventory.Inventory(1,[ant1, ant2], [construction1, construction2], 3)
  testQueen = testInventory.getQueen()
  if testQueen == None:
    raise Exception("getQueen method is not returning existing Queen Ant")
  testAntHill = testInventory.getAnthill()
  if testAntHill == None:
    raise Exception("getAnthill method is not returning existing Ant Hill")
  testInventoryClone = testInventory.clone()
  if testInventoryClone == testInventory:
    raise Exception("The cloned inventory is equal to the original")
  if testInventoryClone.player != testInventory.player:
    raise Exception("The cloned inventory does not have the same player as the original Inventory")
  if testInventoryClone.ants != testInventory.ants:
    raise Exception("The cloned inventory does not have the same set of ants as the original Inventory")
  if testInventoryClone.constructions != testInventory.constructions:
    raise Exception("The cloned inventory does not have the same set of constructions as the original Inventory")
  if testInventoryClone.foodCount != testInventory.foodCount:
    raise Exception("The cloned inventory does not have the same number of food pieces as the original Inventory")
  testInventoryClone.foodCount = 5
  if testInventoryClone.foodCount == testInventory.foodCount:
    raise Exception("The changed cloned inventory food count is the same as the original")
