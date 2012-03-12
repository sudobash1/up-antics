import os

directoryContents = os.listdir(os.getcwd())
unitTestFiles = filter(lamda x: x.endswith('.py') and x != 'run_tests.py', directoryContents)
unitTestModules = [__import__(file.rstrip('.py'), globals(), locals(), [], -1) for file in unitTestFiles]

failures = False

for i in xrange(0, len(unitTestModules)):
    try:
        unitTestModules[i].runTest()
    except Exception as e:
        failures = True
        file = open(unitTestFiles[i].rstrip('.py') + '.log', 'w')
        file.write(e + '\n\n')
        file.write('message: ' + (e.message if e.message != '' else 'No Message'))
        file.close()
        print unitTestFiles[i] + " failed. Check associated logfile in this directory for details."
    
if not failures:
    print 'All tests were successful!'