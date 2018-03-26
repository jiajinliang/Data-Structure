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
import re

# global constants
TEST_TIMEOUT = 10
MEM_LEAK_NUM_REPS = 10
MEMLEAK_P = "Memory leak test succeeded."
MEMLEAK_F = "Memory leak test failed!"
MAX_RETRIES = 2

POSSIBLE_POINTS = 20 #Doesn't include extra credit

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

#Runs a test command, handling timeouts, retries, informative printing, decoding, and errors in the code under test
#Returns a string of the output produced by the code
#Returns None if the code under test timed out or threw an error
def runCommandForTest(command, timeout, possiblePoints, retryNum = 1):
	print("Command: %s" % command)
	
	start = time.time()
	timeoutError, status, stdout, stderr = runCommand(command, timeout)
	if timeoutError:
		if retryNum < MAX_RETRIES:
			print("Your code timed out. Reattempting")
			return runCommandForTest(command, timeout, possiblePoints, retryNum+1)
		else:
			print("Test failed. In each of the %i tries, your program took longer than the %i seconds allocated for this test." % (MAX_RETRIES, timeout))
			print("0/%i points awarded for this test\n" % possiblePoints)
			return None
	
	end = time.time()
	print("Elapsed time %.10f" % (end - start))
	stdout = stdout.decode('latin-1')
	stderr = stderr.decode('latin-1')
	
	if status != 0:
		print("Your program crashed. 0/%i points awarded for this test" % possiblePoints)
		print("Program return value (negative values correspond to unix signals):", status)
		print("Stdout from your program command:", stdout)
		print("Stderr from your program command:", stderr)
		print("")
		return None

	return stdout

#Python print() will only work with ascii characters 0-127 
#latin-1 uses characters 128-255, so need a work around
def printLatinText(text):
	textbytes = text.encode("cp1252")
	sys.stdout.buffer.write(textbytes)

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
		check_output("make part2".split())
		if not os.path.isfile("main2"):
			print("'make part2' command did not create a 'main2' executable.")
			return False
	except CalledProcessError:
		print("'make part2' command failed.")
		return False

	#Confirm that 'make clean' works
	try:
		check_output("make clean".split())
	except CalledProcessError:
		print("'make clean' command failed.")
		return False

	#Compile the code again. Hopefully 'make' still works.
	try:
		check_output("make part2".split())
		if not os.path.isfile("main2"):
			print("'make part2' command did not create a 'main2' executable.")
			return False
	except CalledProcessError:
		print("'make part2' command failed.")
		return False

	print("Compile test succeeded.")
	return True

def helper(directory):
	wtw = {}
	for filename in os.listdir(directory):
		with open("%s/%s" % (directory, filename), encoding="latin-1") as inputDoc:
			lines = inputDoc.readlines()
			prevW = "."
			for line in lines:
				#insert spaces before punctuation so that later tokenization will remove the punctuation
				line = re.sub("(,|\.|\?|!)", r" \1 ", line)
				line = re.sub('[;:"~()[\]{}\\/^_<>*=&%@$+|`]', "", line)
				ws = line.split()
				for w in ws:
					if not prevW in wtw:
						wtw[prevW] = {}
					if not w in wtw[prevW]:
						wtw[prevW][w] = 0
					wtw[prevW][w] += 1
					prevW = w
				if not w in wtw:
					wtw[prevW] = {}

	return wtw

def withinAcceptibleRange(actual, expected):
	allowedDeviation = 0.2
	return (actual > expected * (1- allowedDeviation) and actual < expected * (1 + allowedDeviation))

def testSingleWordGen(testWord, expectedVals, points, description):
	retVal = testSingleWordGenHelper(testWord, expectedVals, points, description)
	sys.stdout.flush()
	return retVal

'''
Confirm that single word generation generates 
the correct words,
and the words with roughly the correct probabilities
'''
def testSingleWordGenHelper(testWord, expectedVals, points, description):
	print("%s\nTest word: '%s' Expected outputs distribution: '%s'" % (description, testWord, expectedVals))

	directory = "PresidentialSpeeches/Trump" 

	numWordsToGen = 10000

	command = "./main2 singleword %s %s %i" % (directory, testWord, numWordsToGen)
	output = runCommandForTest(command, TEST_TIMEOUT, points)
	if output is None:
		return 0

	outputVals = {}
	for key in expectedVals:
		outputVals[key] = 0

	for word in output.split():
		if not word in outputVals:
			print("Found an unexpected word '%s' in the output. Missed %i points.\n" % (word, points))
			return 0
		outputVals[word] += 1

	for word, val in outputVals.items():
		if not withinAcceptibleRange(val, expectedVals[word]*numWordsToGen/sum(expectedVals.values())):
			print("The word '%s' did not show up in roughly the expected proportion. Missed %i points.\n" % (word, points))
			return 0

	print("%i/%i points awarded for this test\n" % (points, points))
	return points 


'''
Confirm that the doc generation only generates allowed sequences of words and that it generates enough unique words
Do not test probabilities
'''
def testDocumentGeneration(presName):
	retVal = testDocumentGenerationHelper(presName)
	print("")
	sys.stdout.flush()
	return retVal

def testDocumentGenerationHelper(presName):
	print("------Testing full document generation for president %s speeches------" % presName)
	thisTestPointsAwarded = 0
	totalPoints = 5

	directory = "PresidentialSpeeches/%s" % presName
	wtw = helper(directory)

	#compare to output of code being tested
	numWordsToGen = 100000
	command = "./main2 document %s %i" % (directory, numWordsToGen)
	output = runCommandForTest(command, TEST_TIMEOUT, totalPoints)
	if output is None:
		return 0
	
	#insert spaces before punctuation so that later tokenization will remove the punctuation
	output = re.sub("(,|\.|\?|!)", r" \1", output)
	words = output.split()

	if len(words) != numWordsToGen:
		print("Didn't generate the requested number of words")
		print("0/%i points awarded for this test\n" % totalPoints)
		return 0

	uniqueWords = set(words)

	incorrectWords = uniqueWords.difference(wtw.keys())
	if len(uniqueWords) < 20:
		print("Generated a document with less than 20 unique words. 0/5 points awarded for this test.")
		return 0	

	if len(incorrectWords) != 0:
		print("Found the following words in your generated document. None of these words appeared in the source documents. Missed 3 points:", end = "")
		sys.stdout.flush()
		for word in incorrectWords:
			printLatinText(" %s" % word)
		print("")
	elif len(uniqueWords) > 1000:
		thisTestPointsAwarded += 3
		print("Generated a document that has only correct words and sufficiently many unique words. +3 points")
	else:
		print("Generated a document with only correct words, but insufficiently many unique words. Missed 3 points.")

	prevWord = "."
	wrongPairs = set()
	for word in words:
		if not prevWord in wtw or not word in wtw[prevWord]:
			wrongPairs.add((prevWord, word))
		prevWord = word
	if len(wrongPairs) != 0:
		print("Found the following wrong pairs in your generated document. None of these pairs appeared in the source documents. Missed 2 points:")
		sys.stdout.flush()
		for pair in wrongPairs:
			printLatinText(str(pair))
		print("")
	else:
		thisTestPointsAwarded += 2
		print("Only pairs that appeared in the source documents appeared in your generated document. +2 points")

	print("%i/%i points awarded for this test" % (thisTestPointsAwarded, totalPoints))
	return thisTestPointsAwarded

#Don't check for correct outputs, just check for memory leak
#Due to point scoring system, memLeakTest must be last
def memLeakTest():
	print("-----Running memory leak test-----")
	
	start = time.time()

	command = "valgrind --log-fd=1 --leak-check=yes ./main2 -r 5 document ./PresidentialSpeeches/Trump 10000 3"
	#timeout * 15 for reps, * 2 for valgrind slowdown
	output = runCommandForTest(command, TEST_TIMEOUT * 5 * 3 * 2, 2)
	if output is None:
		return False
	
	if "no leaks are possible" in output or ("definitely lost: 0 bytes" in output and 
						"indirectly lost: 0 bytes" in output):
		print("No memory leaks detected. Memory leak test succeeded.")
		print("2/2 points awarded for the memory leak test\n")
		return True
	else:
		print("Memory leaks found. Memory leak test failed.")
		print("0/2 points awarded for the memory leak test\n")
		return False

def grade():
	currentScore = 0
	compileTestsWraper()
	sys.stdout.flush()

	print("\n------Testing single word generation (using Trump speeches)------")
	currentScore += testSingleWordGen('crack', {'down' : 1}, 2, 'Test generation with only one possibility')
	currentScore += testSingleWordGen('labor', {'unions' : 1, 'force' : 2}, 3, 'Test generation with two possibilities')
	currentScore += testSingleWordGen('raise', {'wages' : 2, 'your' : 1, 'them' : 1, 'it' : 1}, 3, 'Test generation with many possibilities')

	sys.stdout.flush()

	currentScore += testDocumentGeneration("Trump")
	currentScore += testDocumentGeneration("Obama")

	if memLeakTest():
		currentScore += 2

	print("-----Total points awarded: %i/%i-----" % (currentScore, POSSIBLE_POINTS))
	sys.stdout.flush()

if __name__ == "__main__":
	grade()
