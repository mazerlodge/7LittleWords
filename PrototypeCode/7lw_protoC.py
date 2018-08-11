#!/usr/bin/python

# Version: 20160614-1542

# Reads word segments from file.
# Tests two segment combos against a specified length.  If length met AND combo in dictionary, combo is output.

# Example usage:
# ./7lw_protoC.py -os win -infile filename.txt -targetlen 7
#   Output segment combinations that match the target length specified.

import sys
from ArgTools import ArgParser

# Hard coded constants
INPUT_FILE_PATH__MAC = "/Users/mazerlodge/Documents/XProjects/Python/7LittleWords/data/"
INPUT_FILE_PATH__WIN = "C:\\pmsoren\\_PT\\pyproj\\7LittleWords\\data\\"
DICTIONARY_FILE_NAME = "DictionaryPatterns.csv" 

# Setup variables
bDictionaryMatchRequired = False 
osType = "NOT_SET"
inputFilename = "NOT_SET"
targetLength = -1
segmentList = []
dictionaryWords = []

def showUsage():
    print("Usage: python 7lw_protoB.py -os {mac | win} -infile {filename} -targetlen {a number} [-dictionarymatch] ");
    sys.exit()

def parseArgs():

	# Parse the arguments looking for required parameters.
	# Return false if any tests fail.
	
	global bDictionaryMatchRequired, osType, inputFilename, targetLength
	
	subtestResults = []
	rval = True
	
	# Instantiate the ArgParser
	ap = ArgParser(sys.argv)

	# check the OS type
	rv = False
	if (ap.isArgWithValue("-os", "mac") or ap.isArgWithValue("-os", "win")):
		osType = ap.getArgValue("-os")
		rv = True
	subtestResults.append(rv)

	# check for input filename
	inputFilename = "NOT_SET"
	rv = False
	if (ap.isInArgs("-infile", True)):
		# input filename value must appear after target
		inputFilename = ap.getArgValue("-infile")
		rv = True
	subtestResults.append(rv)

	# check for target length
	targetLength = -1
	rv = False
	if (ap.isInArgs("-targetlen", True)):
		# input filename value must appear after target
		targetLength = int(ap.getArgValue("-targetlen"))
		rv = True
	subtestResults.append(rv)

	# check for the optional dictionary match flag
	bDictionaryMatchRequired = ap.isInArgs("-dictionarymatch", False)

	# Determine if all subtests passed
	for idx in range(len(subtestResults)):
		rval = rval and subtestResults[idx]
			
	return(rval)
	
def getDictionaryWords():

	# set dictionary path based on OS
	if (osType == "mac"):
		dictionaryPath = INPUT_FILE_PATH__MAC + DICTIONARY_FILE_NAME
	else:
		dictionaryPath = INPUT_FILE_PATH__WIN + DICTIONARY_FILE_NAME

	# Read the dictionary
	file = open(dictionaryPath, "r")
	lines = file.readlines()
	file.close()
	
	# extract words from lines
	dwords = []
	for line in lines:
		if line[0] == '#':
			continue 
			
		lp = line.split(',') 
		dwords.append(lp[0]) 
	
	return(dwords)
	
def isInDictionary(targetWord):

	global dictionaryWords

	brval = False
	
	for dw in dictionaryWords:
		if (dw == targetWord):
			brval = True
			break
	
	return(brval) 

def getInputFileLines():

	# set path based on OS
	if (osType == "mac"):
		pathAndFilename = INPUT_FILE_PATH__MAC + inputFilename
	else:
		pathAndFilename = INPUT_FILE_PATH__WIN + inputFilename

	# Read the file
	file = open(pathAndFilename, "r")
	lines = file.readlines()
	file.close()
	
	return(lines)

	
def getSegmentList():
	# parse input lines into segments, return array of segments 
	rval = []
	inLines = getInputFileLines() 
	for rawLine in inLines:
		if rawLine[0] == '#':
			# this line is a comment, skip it
			continue 
		
		segs = rawLine.split(',') 
		for seg in segs:
			# add segments to the return value array
			rval.append(seg.strip()) 
	
	return rval

def getCandidateWords():
	# test segment combos against target length and return a list of candidate words 
	
	global segmentList, dictionaryWords
	
	rval = []
	
	dc = 0
	for x in range(0,len(segmentList)):
		for y in range(0, len(segmentList)): 
			# cannot combine with self, skip this combo
			if (x == y):
				continue 
			
			wx = segmentList[x]
			wy = segmentList[y] 
			if (len(wx) + len(wy) == targetLength):
				# if the dictionary match is required, check it before adding this entry
				if (bDictionaryMatchRequired):
					if(isInDictionary(wx+wy)):
						rval.append(wx + wy)
				else:
					rval.append(wx+wy)
	
	return rval

	
#### EXECUTION Starts Here ####

# Validate startup parameters
if (not parseArgs()):
	showUsage()
	
# If the dictionary is needed, load it.
if (bDictionaryMatchRequired):
	dictionaryWords = getDictionaryWords()
	
segmentList = getSegmentList() 

print len(segmentList) 

candidateWords = getCandidateWords()
print "candidate Word count ", len(candidateWords) 
for cw in candidateWords:
	print(cw)
	

