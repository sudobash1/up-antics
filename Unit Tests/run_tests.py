import os, sys

directoryContents = os.listdir(os.getcwd())
unitTestFiles = filter(lambda x: x.startswith('test_') and x.endswith('.py') and x != 'run_tests.py', directoryContents)
unitTestModules = [__import__(file.rstrip('.py'), globals(), locals(), [], -1) for file in unitTestFiles]

failures = False

#change current directory to location of Antics files so that they can be imported in their test files
testDirectory = os.getcwd()
os.chdir(os.path.join("..", "Antics"))
anticsDirectory = os.getcwd()
sys.path.insert(0, anticsDirectory)
#Run tests
for i in xrange(0, len(unitTestModules)):
    try:
        anticsModule = __import__(unitTestFiles[i].rstrip('.py').lstrip("test_"), globals(), locals(), [], -1)
        unitTestModules[i].runTest(anticsModule)
    except Exception as e:
        failures = True
        file = open(unitTestFiles[i].rstrip('.py') + '.log', 'w')
        file.write(str(e) + '\n\n')
        file.write('message: ' + (e.message if e.message != '' else 'No Message'))
        file.close()
        print unitTestFiles[i] + " failed. Check associated logfile in this directory for details."
#change direectory back to initial value
os.chdir(testDirectory)
sys.path.remove(anticsDirectory)
if not failures:
    print 'All tests were successful!'