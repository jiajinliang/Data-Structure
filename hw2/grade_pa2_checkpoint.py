#!/usr/bin/env python
'''
Grading script for PA2 (BST)
Jonathan Margoliash
Based on grading script from  Dylan McNamara, Niema Moshiri
'''
from subprocess import Popen, check_output, PIPE, TimeoutExpired, CalledProcessError
import time
import sys
import os
import math

# global constants
SHORT_TEST_TIMEOUT = 5  # kill execution if it takes more than this number in seconds
LONG_TEST_TIMEOUT = 50
MEM_LEAK_NUM_REPS = 10
MEMLEAK_P = "Memory leak test succeeded."
MEMLEAK_F = "Memory leak test failed!"
MAX_RETRIES = 2

POSSIBLE_POINTS = 25 #Doesn't include extra credit

#runs a command
#returns a tuple (timeoutError, returnStatus, stdout, stderr)
#If the command fails before starting up, then this method throws the exception related to that failure
#If the command fails after starting up, then this method returns with returnStatus != 0 and stderr (hopefully) not empty, and timeoutError = None
#If this python script would fail after the command starts up (e.g. keyboard interrupt), then this script tries as hard
#    as possible to kill the subprocess before continuing to fail. Not guaranteed to work against a barrage of keyboard interrupts
#    I'm not sure this is even needed as this doesn't seem to be an issue when command doesn't contain timeout
#If the command times out, then this returns with (timeoutError, None, None, None)
#stdout and stderr are bytes and must be decoded
#Command should just be a string
#Command must NOT include the unix timeout command, as this will only kill the child process and not its descendants,
#And so in particular if you include timeout in the command, then this will kill timeout and not the process being timed
def runCommand(command, timeout):
	proc = None
	e = None
	try:
		proc = Popen(command.split(), stdout = PIPE, stderr = PIPE)
		stdout, stderr = proc.communicate(timeout = timeout)
		return (None, proc.returncode, stdout, stderr)
	#catch all exceptions, including keyboard interrupt
	except TimeoutExpired as timeoutError:
		return (timeoutError, None, None, None)
	except:
		#I'm not sure this is necessary, but here's an attempt to handle keyboard interrupts and still kill the subprocess
		#Need to catch all exceptions so that we can catch keyboard interrupts.
		#If we don't catch a keyboard interrupt, then not even the finally block seems to run before the program dies
		#Its possible that another keyboard interrupr is sent after we enter this block before the process is killed.
		#I can't figure out any sane way to handle that
		e = sys.exc_info()[1] #stroe the error for future use
	finally:
		if proc is not None:
			proc.kill()
		if e is not None:
			#e wasn't an error we're expecting, so we shouldn't really have caught it,
			#we just needed to kill the supbrocess. Now that that's done, reraise it
			raise e

#Python print() will only work with ascii characters 0-127 
#latin-1 uses characters 128-255, so need a work around
def printLatinText(text):
	textbytes = text.encode("cp1252")
	sys.stdout.buffer.write(textbytes)
	sys.stdout.flush()

#In addition to testing the compilation
#Intentionally has the side effect of leaving the code compiled
#so future tests can be run
def compileTestsWraper():
	success = compileTests()
	if success:
		return

	print('0/%i points awarded' % POSSIBLE_POINTS)
	exit()

def compileTests():
	print("Running compile test")
	
	#Confirm that 'make' works
	try:
		check_output("make")
		if not os.path.isfile("main"):
			print("'make' command did not create a 'main' executable.")
			return False
	except CalledProcessError:
		print("'make' command failed.")
		return False

	#Confirm that 'make clean' works
	try:
		check_output("make clean".split())
	except CalledProcessError:
		print("'make clean' command failed.")
		return False

	#Compile the code again. Hopefully 'make' still works.
	try:
		check_output("make")
		if not os.path.isfile("main"):
			print("'make' command did not create a 'main' executable.")
			return False
	except CalledProcessError:
		print("'make' command failed.")
		return False

	print("Compile test succeeded.")
	return True

'''
Looks for the files TestCases/<testName>Corpus.txt, GradingScriptFiles/<testName>Tests.txt, 
The corpus file will contain all the words to be parsed by the autocompleter
And the tests file will contain all the test cases
'''
def standardTestWraper(testName, testDescription, shortTest, totalPoints, outputLocation = None):
	testFile = ('GradingScriptFiles/{}Tests.txt'.format(testName))
	corpusFile = ('TestCases/{}Corpus.txt'.format(testName))
	print("-----{}-----".format(testDescription))
	pointsAwarded = standardTest(corpusFile, testFile, testDescription, 1, None, shortTest, totalPoints, outputLocation)
	sys.stdout.flush()
	return pointsAwarded

def standardTest(corpusFile, testFile, testDescription, retryNum, prefixFile, shortTest, totalPoints, outputLocation):
	if shortTest:
		timeout = SHORT_TEST_TIMEOUT
	else:
		timeout = LONG_TEST_TIMEOUT

	with open(testFile, encoding='latin-1') as testCases:
		lines = testCases.readlines()
	
	prefixes = []
	expectedOutputs = []
	for line in lines:
		tokens = line.split()
		prefixes.append(tokens[0])
		expectedOutputs.append(tokens[1:])

	allPrefixes = " ".join(prefixes)
	if prefixFile is None:
		command = "./main {} {}".format(corpusFile, allPrefixes)
	else:
		command = "./main {} -p {}".format(corpusFile, prefixFile)
	print("Command: %s" % command)

	
	start = time.time()
	timeoutError, status, stdout, stderr = runCommand(command, timeout)
	if timeoutError:
		if retryNum < MAX_RETRIES:
			print("Your code timed out. Reattempting")
			return standardTest(corpusFile, testFile, testDescription, retryNum + 1, prefixFile, shortTest, totalPoints, outputLocation)
		else:
			print("Test failed. In each of the %i tries, your program took longer than the %i seconds allocated for this test." % (MAX_RETRIES, timeout))
			print("0/%i points awarded for this test" % totalPoints)
			return 0
	
	end = time.time()
	print("Elapsed time %.10f" % (end - start))
	stdout = stdout.decode('latin-1')
	stderr = stderr.decode('latin-1')
	
	if status != 0:
		print("Your program crashed. 0/%i points awarded for this test" % totalPoints)
		print("Program return value (negative values correspond to unix signals):", status)
		print("Stdout from your program command:", stdout)
		print("Stderr from your program command:", stderr)
		return 0

	outputLines = stdout.splitlines()

	testNum = -1
	numTests = len(outputLines)
	successfulTests = 0
	textOutput = []
	for expectedOutput in expectedOutputs:
		testNum += 1
		outputLine = outputLines[testNum].strip()
		if outputLine.split() == expectedOutput:
			#Python print() will only work with ascii characters 0-127 
			#latin-1 uses characters 128-255, so need a work around
			text = "Successfully completed prefix \"{}\" as \"{}\"\n".format(prefixes[testNum], outputLine)
			textOutput.append(text)
			
			successfulTests += 1
		else:
			text = "Incorrectly completed prefix \"{}\". Expected answer is \"{}\". Actual output was '{}'\n".format(prefixes[testNum], " ".join(expectedOutput), outputLine)
			textOutput.append(text)

	if outputLocation is not None:	
		with open(outputLocation, 'w', encoding='latin-1') as output:
			output.writelines(textOutput)
		print("Test output written to %s" % outputLocation)
	else:
		for line in textOutput:
			printLatinText(line)

	thisTestPointsAwarded = math.floor(successfulTests/numTests *totalPoints)
	print("%i/%i points awarded for this test" % (thisTestPointsAwarded, totalPoints))
	return thisTestPointsAwarded

#Don't check for correct outputs, just check for memory leak
#Due to point scoring system, memLeakTest must be last
def memLeakTest(testName, retryNum):
	timeout = LONG_TEST_TIMEOUT

	print("-----Running memory leak test-----")
	with open('GradingScriptFiles/{}Tests.txt'.format(testName), encoding='latin-1') as testCases:
		lines = testCases.readlines()
	
	prefixes = []
	for line in lines:
		tokens = line.split()
		prefixes.append(tokens[0])

	allPrefixes = " ".join(prefixes)
	start = time.time()
	command = "valgrind --log-fd=1 --leak-check=yes ./main TestCases/{}Corpus.txt -o {} {}".format(testName, MEM_LEAK_NUM_REPS, allPrefixes)
	print("Command: %s" % command)
	
	timeoutError, status, stdout, stderr = runCommand(command, timeout)
	end = time.time()

	if timeoutError:
		if retryNum < MAX_RETRIES:
			print("Your code timed out. Reattempting")
			return memLeakTest(testName, retryNum + 1)
		else:
			print("Test failed. In each of the %i tries, your program took longer than the %i seconds allocated for this test." % (MAX_RETRIES, timeout))
			return False
	
	print("Elapsed time %.10f" % (end - start))
	stdout = stdout.decode('latin-1')
	stderr = stderr.decode('latin-1')
	
	if status != 0:
		print("Your program crashed.")
		print("Program return value (negative values correspond to unix signals):", status)
		print("Stdout from your program command:", stdout)
		print("Stderr from your program command:", stderr)
		return False

	output = check_output(command.split()).decode('latin-1')
	if "no leaks are possible" in stdout or ("definitely lost: 0 bytes" in stdout and 
						"indirectly lost: 0 bytes" in stdout):
		print("No memory leaks detected. Memory leak test succeeded.")
		return True
	else:
		print("Memory leaks found. Memory leak test failed.")
		return False

def grade():
	currentScore = 0
	compileTestsWraper()
	sys.stdout.flush()

	currentScore += standardTestWraper("Empty", "Running empty corups test", True, 1)
	currentScore += standardTestWraper("Single", "Running single word corups test", True, 3)
	currentScore += standardTestWraper("Moderate", "Running moderate sized corups test", True, 6) 
	currentScore += standardTestWraper("Large", "Running large sized corpus test", False, 7)

	print("-----Running long test on large corpus-----")
	currentScore += standardTest("TestCases/LargeCorpus.txt", "GradingScriptFiles/LongTest.txt", "Running long test on large corpus", 1, "GradingScriptFiles/LongTestPrefixes.txt", False, 5, "longTestOutput.txt")
	sys.stdout.flush()

	if memLeakTest("Moderate", 1):
		print("3/3 points awarded for the memory leak test")
		currentScore += 3
	else:
		print("0/3 points awarded for the memory leak test")

	print("-----Total points awarded: %i/%i-----" % (currentScore, POSSIBLE_POINTS))
	sys.stdout.flush()

if __name__ == "__main__":
    grade()
