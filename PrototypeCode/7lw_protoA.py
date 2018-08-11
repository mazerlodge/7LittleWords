#!/usr/bin/python

# Version: 20160613-1445

# Reads word segments from file.
# Outputs line if found or "not found"

# Example usage:
# ./7lw_protoA.py -os win -infile filename.txt
#   Output lines in file if found or the phrase '{file} not found'.

import sys
from ArgTools import ArgParser

# Hard coded constants
INPUT_FILE_PATH__MAC = "/Users/mazerlodge/Documents/XProjects/Python/7LittleWords/data/"
INPUT_FILE_PATH__WIN = "C:\\pmsoren\\_PT\\pyproj\\7LittleWords\\data\\"

# Setup variables
osType = "NOT_SET"
inputFilename = "NOT_SET"

def showUsage():
    print("Usage: python 7lw_protoB.py -os {mac | win} -infile {filename} ");
    sys.exit()

def parseArgs():

	# Parse the arguments looking for required parameters.
	# Return false if any tests fail.
	
	global osType, inputFilename
	
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

	# Determine if all subtests passed
	for idx in range(len(subtestResults)):
		rval = rval and subtestResults[idx]
			
	return(rval)
	
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

def parseInputLines():
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

	
#### EXECUTION Starts Here ####

# Validate startup parameters
if (not parseArgs()):
	showUsage()
	
segList = parseInputLines() 

print len(segList) 

