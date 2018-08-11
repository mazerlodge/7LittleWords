#!/usr/bin/python
# Version: 20180217-1845

import sys
from ArgTools import ArgParser
from Odometer import Odometer

class DictionaryEngine:

	# Hard coded constants
	DICTIONARY_FILE__MAC = "/Users/mazerlodge/Documents/XProjects/ObjectiveC/Skylar/Dictionaries/DictionaryPatterns.csv"
	DICTIONARY_FILE__WIN = "C:\\pmsoren\\_PT\\pyproj\\DictionaryTools\\Data\\DictionaryPatterns.csv"
	INPUT_FILE_PATH__MAC = "/Users/mazerlodge/Documents/XProjects/Python/7LittleWords/data/"
	INPUT_FILE_PATH__WIN = "C:\\pmsoren\\_PT\\pyproj\\7LittleWords\\data\\"

	# Setup variables
	bInitOK = False
	bInDebug = False
	osType = "NOT_SET"
	maintType = "NOT_SET"
	searchType = "NOT_SET"
	dictionaryPath = "NOT_SET"
	outDictionaryPath = "NOT_SET"
	targetPhrase = "NOT_SET" 
	inputFile = "NOT_SET"
	action = "NOT_SET"
	lines = []
	windowSize = -1

	def __init__(self,args):
		if (self.parseArgs(args)):
			self.bInitOK = True
		else:
			print("Init failed in argument parser.")
			
	def showUsage(self):
		print("Usage: python dict.py -os [mac | win] -action [search | genmask | jumblept2 | maint | 7lw ] {-debug}\n"
				+ "About searches: find a word, pattern (like ABBC), substitution "
				+ "encoded word (like GBRRCB),\n or jumbled word (like ISFH, returns fish).\n"
				+ "\tParams for -action search: -searchtype [word | pattern | encword | jumble] -target targetPhrase \n"
				+ "\tParams for -action jumblept2: -target letterList -windowsize n  \n"
				+ "\tParams for -action 7lw: -infile filename (a 7LW data file) -windowsize n (target word length)  \n"
				+ "\tParams for -action genmask: -target targetPhrase \n"
				+ "\tParams for -action maint: -mainttype [ gensortcolumn | addword ] -target word_to_add \n "
				+ "\tNote: search for word or encword returns first match, pattern returns all matches.\n")
		
	def debugMsg(self, msg):
		if (self.bInDebug):
			print msg
			
	def parseArgs(self,args):
		# Parse the arguments looking for required parameters.
		# Return false if any tests fail.
		subtestResults = []
		rval = True

		# Instantiate the ArgParser
		ap = ArgParser(args)
		
		# check for optional debug flag
		self.bInDebug = ap.isInArgs("-debug", False)

		# check the OS type
		rv = False
		if (ap.isArgWithValue("-os", "mac") or ap.isArgWithValue("-os", "win")):
			self.osType = ap.getArgValue("-os")
			rv = True
		subtestResults.append(rv)

		# check for action
		self.action = "NOT_SET"
		rv = False
		if (ap.isInArgs("-action", True)):
			# action value must appear after target
			self.action = ap.getArgValue("-action")
			rv = True
		subtestResults.append(rv)

		# check for searchtype, using a different arg parse approach than the OS check.
		if (self.action == "search"):
			rv = False
			if (ap.isInArgs("-searchtype", True)):
				# value must be either word or pattern
				st = ap.getArgValue("-searchtype")
				validSearchTypes = ["word", "pattern", "encword", "jumble"]
				for vst in validSearchTypes:
					if (st == vst):
						self.searchType = st
						rv = True
			subtestResults.append(rv)
			
			# search also requires a target
			rv = False
			if (ap.isInArgs("-target", True)):
				self.targetPhrase = ap.getArgValue("-target")
				rv = True
			subtestResults.append(rv)
			
		# check for JumblePt2 
		if (self.action == "jumblept2"):
			rv = False
			if (ap.isInArgs("-windowsize", True)):
				self.windowSize = int(ap.getArgValue("-windowsize"))
				rv = True
			subtestResults.append(rv)

			# JumblePt2 also requires a target
			rv = False
			if (ap.isInArgs("-target", True)):
				self.targetPhrase = ap.getArgValue("-target")
				rv = True
			subtestResults.append(rv)
			
		# check for 7lw (Seven Little Words) 
		if (self.action == "7lw"):
			rv = False
			if (ap.isInArgs("-windowsize", True)):
				self.windowSize = int(ap.getArgValue("-windowsize"))
				rv = True
			subtestResults.append(rv)

			# 7lw also requires an input file 
			rv = False
			if (ap.isInArgs("-infile", True)):
				self.inputFile = ap.getArgValue("-infile")
				rv = True
			subtestResults.append(rv)
						
		# check for genmask 
		if (self.action == "genmask"):
			# GenMask requires a target
			rv = False
			if (ap.isInArgs("-target", True)):
				self.targetPhrase = ap.getArgValue("-target")
				rv = True
			subtestResults.append(rv)			

		# check for maintenance 
		if (self.action == "maint"):
			rv = False
			if (ap.isInArgs("-mainttype", True)):
				self.maintType = ap.getArgValue("-mainttype")
				if (self.maintType == "addword"):
					if (ap.isInArgs("-target", True)):
						self.targetPhrase = ap.getArgValue("-target")
						rv = True

				# no additional checks for adding sort column
				if (self.maintType == "gensortcolumn"):
					rv = True
			subtestResults.append(rv)

		# Determine if all subtests passed
		for idx in range(len(subtestResults)):
			self.debugMsg("Arg subtest " + str(subtestResults[idx]))
			rval = rval and subtestResults[idx]
				
		return(rval)
	
	def getDictionaryLines(self):
		# Read the dictionary file from file location based on osType specified.
		# Return an array of lines (CSV strings from the dictionary).
		
		# set dictionary path based on OS
		if (self.osType == "mac"):
			self.dictionaryPath = self.DICTIONARY_FILE__MAC 
		else:
			self.dictionaryPath = self.DICTIONARY_FILE__WIN

		# Read the dictionary
		file = open(self.dictionaryPath, "r")
		lines = file.readlines()
		file.close()
	
		return(lines)
	
	def writeDictionaryLinesWithSortColumn(self):
		# Maintenance method, creates a dictionary file with sort column
		#   information.  Used to update dictionaries originally built without
		#   sorted patterns. 
		#  Dictionary file line before: aardvark,8
		#  Dictionary file line after:  aardvark,8,AABCDABE
		# Note: The output file has the word "NEW" appended. The original file is unchanged.

		outLineCount = 0
	
		lines = self.getDictionaryLines()

		# set dictionary path based on OS
		if (self.osType == "mac"):
			self.outDictionaryPath = self.DICTIONARY_FILE__MAC 
		else:
			self.outDictionaryPath = self.DICTIONARY_FILE__WIN

		# open the new file for writing.
		file = open(self.outDictionaryPath + "NEW", "w")
	
		for aline in lines:
			parts = aline.split(',')
			line2write = aline
			# if the line is commented out, don't add sort column
			if aline[0] != '#':	
				line2write = aline.strip() + "," + doSortGen(parts[0]) + "\n"
			file.write(line2write)
			outLineCount += 1

		file.close()
	
		print("Lines written to new dictionary file: " + str(outLineCount))
	
		return(outLineCount)
		
	def getInputFileLines(self, fileName):

		# set path based on OS
		if (self.osType == "mac"):
			pathAndFilename = self.INPUT_FILE_PATH__MAC + fileName
		else:
			pathAndFilename = self.INPUT_FILE_PATH__WIN + fileName

		# Read the file
		file = open(pathAndFilename, "r")
		lines = file.readlines()
		file.close()
	
		return(lines)

	
	def getSegmentList(self, fileName):
		# parse input lines into segments, return array of segments 
		rval = []
		inLines = self.getInputFileLines(fileName) 
		for rawLine in inLines:
			if rawLine[0] == '#':
				# this line is a comment, skip it
				continue 
		
			segs = rawLine.split(',') 
			for seg in segs:
				# add segments to the return value array
				rval.append(seg.strip()) 
	
		return rval
		
	
	def getPartFromCSV(self, CSVString, partIndex): 
		# Given a CSV String (e.g. "test,4,ABCA,estt") 
		#   return the zero based index requested (e.g. if 0, give back 'test')
		rval = "NOT_SET" 

		parts = CSVString.split(',')

		if (partIndex < len(parts)):
			rval = parts[partIndex] 
	
		return rval
		
		
	def addWordToDictionary(self, newWord):
		# add the specified word to the dictionary.
		# dictionary entries have the following format:
		# #word,len,pattern,sortedword
		# aardvark,8,AABCDABE,aaadkrrv
		
		# search the dictionary to see if the word already exists.
		searchResult = self.doSearch("word", newWord, True)
		
		if (len(searchResult) > 0):
			print "addWordToDictionary: The word is already in dictionary."
			return
			
		# generate line to add to the dictionary
		line2Add = ",".join([ newWord, 
								str(len(newWord)),
								self.doMaskGen(newWord),
								self.doSortGen(newWord)])
		line2Add = line2Add + "\n"
				
		print "Line to add: " + line2Add			

	
		# set dictionary path based on OS
		if (self.osType == "mac"):
			self.DictionaryPath = self.DICTIONARY_FILE__MAC 
		else:
			self.DictionaryPath = self.DICTIONARY_FILE__WIN

		# open the new file for writing.
		file = open(self.DictionaryPath, "a")
		file.write(line2Add)
		file.close()
	
		print("Lines written to dictionary: " + self.DictionaryPath)
		
	def do7lw_old(self, inputFile, windowSize):
		# Do a seven little word search where the phrase list is a CSV list of letter segments.
		# This is almost identical to jumblePt2 below.
		phraseList = []
		unsortedPhraseList = []
		
		# get segments from the input file and transform them into a CSV string
		segmentList = self.getSegmentList(inputFile)
		segmentString = ""
		for seg in segmentList:
			segmentString += seg + ","
		segmentString = segmentString[0:len(segmentString)-1]
		self.debugMsg("do7lw: got segmentString = " + segmentString)

		# generate an odometer instance with wheels that are a CSV Lists.
		odometer = Odometer(segmentString, windowSize, True, self.bInDebug) 
				
		# Generate Phrase List 
		print "Building distinct potential phrase list..."
		odoCycleCount = 0
					
		# Determine cycle limit based on number of wheels and size of those wheels 
		wheelSize = odometer.getOdometerWheelSize(0)
		numberOfWheels = odometer.getNumberOfWheels()
		cycleLimit = wheelSize
		for x in range(1,numberOfWheels):
			cycleLimit = cycleLimit * (wheelSize-x)
		print "Cycle Limit set to " + str(cycleLimit) 
			
		# set the frequency of update messages to 10% of the cycle limit.
		msgInterval = cycleLimit * .1
		ci = msgInterval		
		print "WindowSize=" + str(windowSize) + " wheelSize=" + str(wheelSize) + " numberOfWheels=" + str(numberOfWheels)  
		bDone = False
		while(not bDone): 
			odoCycleCount += 1		
			currentCombos = odometer.readOdometer()
			
			for phrase in currentCombos:
				# WARNING: This may introduce errors, combos may be returned jumbled. 
				# However the 7LW puzzles don't allow sorting within a segment.
				sortedPhrase = self.doSortGen(phrase)
			
				# if this phrase wasn't in the distict phrase list, add it.
				if(phraseList.count(sortedPhrase) == 0):
					phraseList.append(sortedPhrase) 
					
				# keep unsorted phrases, output when no matches are found.
				if(unsortedPhraseList.count(phrase) == 0):
					unsortedPhraseList.append(phrase) 
			
			# If at odometer is at max position mark as done, otherwise advance.
			if (odometer.isOdometerAtMax()):
				# remove last item, it is all maxes.
				if (len(phraseList) > 0):
					del phraseList[len(phraseList)-1]
				bDone = True
			else:
				odometer.advanceOdometer()
				
			# Check governor for runaway process
			if (odoCycleCount > cycleLimit):
				print "do7lw: Cycle limit governor hit."
				print "Odometer indexes at " + odometer.odometerIndexesToString()
				print "Is odometer at max = " + str(odometer.isOdometerAtMax())
				bDone = True
				
			# if it's time to output an update message, do it and set threshold for next message.
			if (odoCycleCount > ci):
				percentDone = round(odoCycleCount*100.0/cycleLimit,1) 
				print "Working, cycle limit percent consumed = {0}% at cc={1} oi={2}".format(percentDone, odoCycleCount, odometer.odometerIndexesToString()) 
				ci += msgInterval

		print "Cycles used = %s " % odoCycleCount
	
		# Process phrases through jumble evaluation 
		print("Processing, phrase combos count = " + str(len(phraseList)))
		
		# Walk the phrase list, finding word matches, adding them to 
		#   the distinct match list.
		matchList = []
		loopCount = 0
		phraseCount = len(phraseList)
		msgInterval = phraseCount * .1
		ci = msgInterval
		for phrase in phraseList:
			loopCount += 1
			currentMatches = self.doSearch("jumble", phrase, True)
			if (len(currentMatches) > 0):
				for m in currentMatches:
					if (matchList.count(m) == 0):
						matchList.append(m)
						print "\t match detected = " + self.getPartFromCSV(m,0)
						
			if (loopCount > ci):
				percentDone = round(loopCount*1.0/phraseCount,2)
				print "Searching dictionary, processed={0} matches={1}".format(percentDone, len(matchList))
				ci += msgInterval
				
		# end for phrase...
		
		if (len(matchList) == 0):
			print "No matches found"
		else:
			print "Matches detected"
			for aMatch in matchList:
				print "\t" + self.getPartFromCSV(aMatch,0)
			print "Match count = " + str(len(matchList))

		if (((len(matchList)==0) & (len(unsortedPhraseList) > 0)) | (self.bInDebug)): 
			print "Raw phrases considered were:"
			for p in unsortedPhraseList:
				print "\t " + p

	def do7lw(self, inputFile, windowSize):
		# Do a seven little word search where the phrase list is a CSV list of letter segments.
		phraseList = []
		
		# get segments from the input file and transform them into a CSV string
		segmentList = self.getSegmentList(inputFile)
		segmentString = ""
		for seg in segmentList:
			segmentString += seg + ","
		segmentString = segmentString[0:len(segmentString)-1]
		self.debugMsg("do7lw: got segmentString = " + segmentString)

		# generate an odometer instance with wheels that are a CSV Lists.
		odometer = Odometer(segmentString, windowSize, True, self.bInDebug) 
				
		# Generate Phrase List 
		print "Building distinct potential phrase list..."
		odoCycleCount = 0
					
		# Determine cycle limit based on number of wheels and size of those wheels 
		wheelSize = odometer.getOdometerWheelSize(0)
		numberOfWheels = odometer.getNumberOfWheels()
		cycleLimit = wheelSize
		for x in range(1,numberOfWheels):
			cycleLimit = cycleLimit * (wheelSize-x)
		cycleLimit *= 1.2
		cycleLimit = (wheelSize**numberOfWheels) * 1.3
		print "Cycle Limit set to " + str(cycleLimit) 
			
		# set the frequency of update messages to 10% of the cycle limit.
		msgInterval = cycleLimit * .1
		ci = msgInterval		
		print "WindowSize=" + str(windowSize) + " wheelSize=" + str(wheelSize) \
			  + " numberOfWheels=" + str(numberOfWheels)  
		bDone = False
		while(not bDone): 
			odoCycleCount += 1		
			currentCombos = odometer.readOdometer()
			
			for phrase in currentCombos:
				# if this phrase wasn't in the distict phrase list, add it.
				if(phraseList.count(phrase) == 0):
					phraseList.append(phrase) 
					
			# If at odometer is at max position mark as done, otherwise advance.
			if (odometer.isOdometerAtMax()):
				# remove last item, it is all maxes.
				if (len(phraseList) > 0):
					del phraseList[len(phraseList)-1]
				bDone = True
			else:
				oibefore = odometer.odometerIndexesToString()
				cuia = odometer.advanceOdometer()
				if (cuia > 1): 
					self.debugMsg("cc={3} CUIA={0} oibefore={1} after={2}".format(cuia,oibefore, odometer.odometerIndexesToString(), odoCycleCount))
				odoCycleCount += cuia - 1
				
			# Check governor for runaway process
			if (odoCycleCount > cycleLimit):
				print "do7lw: Cycle limit governor hit."
				print "Odometer indexes at " + odometer.odometerIndexesToString()
				print "Is odometer at max = " + str(odometer.isOdometerAtMax())
				bDone = True
				
			# if it's time to output an update message, do it and set threshold for next message.
			if (odoCycleCount > ci):
				percentDone = odoCycleCount * 1.0 / cycleLimit
				statusMsg = "Building potential phrase list is at {0:.0%}"
				print statusMsg.format(percentDone)
				ci += msgInterval

		print "Cycles used = %s " % odoCycleCount
	
		# Process phrases through jumble evaluation 
		print("Processing, phrase combos count = " + str(len(phraseList)))
		
		# Walk the phrase list, finding word matches, adding them to 
		#   the distinct match list.
		matchList = []
		loopCount = 0
		phraseCount = len(phraseList)
		msgInterval = phraseCount * .1
		ci = msgInterval
		for phrase in phraseList:
			loopCount += 1
			currentMatches = self.doSearch("word", phrase, True)
			if (len(currentMatches) > 0):
				for m in currentMatches:
					if (matchList.count(m) == 0):
						matchList.append(m)
						print "\t match detected = " + self.getPartFromCSV(m,0)
						
			if (loopCount > ci):
				percentDone = loopCount * 1.0 / phraseCount 
				searchMsg = "Searching dictionary, processed={0:.0%} matches={1}"
				print searchMsg.format(percentDone, len(matchList))
				ci += msgInterval
				
		# end for phrase...
		
		if (len(matchList) == 0):
			print "No matches found"
		else:
			print "Matches detected"
			for aMatch in matchList:
				print "\t" + self.getPartFromCSV(aMatch,0)
			print "Match count = " + str(len(matchList))

	
	def doJumblePt2(self, letterList, windowSize): 
		# process Jumble Part 2 using Odometer method.		
		phraseList = []

		# generate an odometer instance with wheels that are not CSV Lists.
		odometer = Odometer(letterList, windowSize, False, self.bInDebug) 
		
		# Generate Phrase List 
		print "Building distinct potential jumble list..."
		odoCycleCount = 0
		
		# set cycle limit to length of letter list factorial for windowsize range.
		# e.g. letter list of 7, widow size 2 --> 7*6 (stop, aka given 7 letters there are 42 2 letter combos).
		cycleLimit = len(letterList)
		for x in range(len(letterList)-1,len(letterList)-windowSize,-1):
			cycleLimit = cycleLimit * x
			
		# set the frequency of update messages to 10% of the cycle limit.
		msgInterval = cycleLimit * .1
		ci = msgInterval
		print "Cycle Limit set to " + str(cycleLimit)
		bDone = False
		while(not bDone): 
			odoCycleCount += 1
			
			# readOdometer always returns an array, but for 
			#   jumbles that array always only contains a single element.
			phrase = odometer.readOdometer()[0]
			sortedPhrase = self.doSortGen(phrase)
			
			self.debugMsg("doJumblePt2: phrase = " + phrase)
			
			# if this phrase wasn't in the distict phrase list, add it.
			if(phraseList.count(sortedPhrase) == 0):
				phraseList.append(sortedPhrase) 
			
			# If at odometer is at max position mark as done, otherwise advance.
			if (odometer.isOdometerAtMax()):
				# remove last item, it is all maxes.
				del phraseList[len(phraseList)-1]
				bDone = True
			else:
				odometer.advanceOdometer()
				
			# Check governor for runaway process
			if (odoCycleCount > cycleLimit):
				print "doJumblePt2: Cycle limit governor hit."
				bDone = True
				
			# if it's time to output an update message, do it and set threshold for next message.
			if (odoCycleCount > ci):
				print "Working, cycle limit percent consumed = " + str(odoCycleCount*1.0/cycleLimit)
				ci += msgInterval

		print "Cycles used = %s " % odoCycleCount
	
		# Process phrases through jumble evaluation 
		print("Processing, letter combos count = " + str(len(phraseList)))
		
		# Walk the phrase list, finding jumble matches, adding them to 
		#   the distinct match list.
		matchList = []
		loopCount = 0
		phraseCount = len(phraseList)
		msgInterval = phraseCount * .1
		ci = msgInterval
		for phrase in phraseList:
			loopCount += 1
			currentMatches = self.doSearch("jumble", phrase, True)
			if (len(currentMatches) > 0):
				for m in currentMatches:
					if (matchList.count(m) == 0):
						matchList.append(m)
						
			if (loopCount > ci):
				print "Working, combos processed = " + str(loopCount*1.0/phraseCount)
				ci += msgInterval
				
		# end for phrase...
		
		if (len(matchList) == 0):
			print "No matches found"
		else:
			for aMatch in matchList:
				print aMatch
			print "Match count = " + str(len(matchList))


	def showMsg(self, msg, bQuiet):
		if (not bQuiet):
			print(msg)

	
	def doSearch(self, searchType, targetPhrase, bQuiet):

		rval = []

		# Load the dictionary if not already set
		if (len(self.lines) < 1):
			print "Loading dictionary..."
			self.lines = self.getDictionaryLines()

		# determine which index to search; 0 for words, 2 for patterns
		idx = 0
		if (searchType == "pattern"):
			idx = 2
			self.showMsg("Searching for patterns.", False)
		
		if (searchType == "encword"):
			# find a pattern from the encrypted word and do a pattern search
			idx = 2
			targetPhrase = self.doMaskGen(targetPhrase)
			self.showMsg("Searching for generated pattern.", bQuiet)

		if (searchType == "jumble"):
			# find a sorted pattern from the target word and do a search
			idx = 3
			targetPhrase = self.doSortGen(targetPhrase)
			self.showMsg("Searching for jumbled word.", bQuiet)

		# If the word2find was a phrase, break up the phrase and search for each word
		w2fParts = targetPhrase.split(' ')
		if (len(w2fParts) > 1):
			self.showMsg("Searching for each word in the phrase '%s'." % targetPhrase, bQuiet)
	
		for word2find in w2fParts:
			# work on each word in the phrase
			bFound = False

			# Search for a word
			for line in self.lines:
				parts = line.split(',')
				# word is in part 0
				currentWord = parts[idx].strip()
				if(word2find.lower() == currentWord.lower()):
					self.showMsg(line.strip(), bQuiet)
					rval.append(line.strip())
					bFound = True

				# perf improvement: if not searching for a pattern stop after 1.
				if ((bFound) and (searchType != "pattern")):
					break

			# Print not found results
			if (not bFound):
				self.showMsg("%r not found" % word2find, bQuiet)
				
		return rval
			
	def doMaskGen(self, rawPhrase):
		# generate a mask for the value in targetPhrase
		rval = ""
		
		phraseLen = len(rawPhrase)
		distinctPhraseLetters = []
		patternLetters = []
	
		# build distinct phrase letters array
		for aLetter in rawPhrase:
			if(not self.isInArray(aLetter, distinctPhraseLetters)):
				distinctPhraseLetters.append(aLetter)
	
		# populate pattern letters array
		currASCIIVal = 65
		for x in range(0,len(distinctPhraseLetters)):
			patternLetters.append(chr(currASCIIVal))
			currASCIIVal += 1
		
		# generate mask
		for tpl in rawPhrase:
			maskLetter = self.getCorrespondingEntry(tpl,distinctPhraseLetters,patternLetters)
			rval += maskLetter
		
		# output result
		print("doMaskGen: The mask is " + rval)
	
		return(rval)
	
	def doSortGen(self, phrase):
		# Generate a string with chars from phrase in sorted order.
	
		newphrase=""
	
		for ac in sorted(phrase):
			newphrase += ac
	
		return(newphrase)
					
	def getCorrespondingEntry(self, letter, phraseArray, patternArray):

		rval = "?"
	
		for x in range(0,len(phraseArray)):
			if (letter == phraseArray[x]):
				rval = patternArray[x]
				break;
	
		return(rval)
		
	def isInArray(self, letter, phraseArray):
	
		rval = False
	
		for aLetter in phraseArray:
			if (letter == aLetter):
				rval = True
				break
			
		return(rval)
		
	def doMaint(self):

		self.debugMsg("doMaint: Processing maintenance type [%s]" % self.maintType)

		# determine which maintenance to do 		
		if (self.maintType == "gensortcolumn"):
			self.writeDictionaryLinesWithSortColumn()

		if (self.maintType == "addword"):
			self.addWordToDictionary(self.targetPhrase)		
		
	def doAction(self):
	
		self.debugMsg("doAction: Processing action [%s]" % self.action)
	
		# determine which action to execute
		if (self.action == "search"):
			self.doSearch(self.searchType, self.targetPhrase, False)
	
		if (self.action == "genmask"):
			self.doMaskGen(self.targetPhrase)
	
		if (self.action == "jumblept2"):
			self.doJumblePt2(self.targetPhrase, self.windowSize)

		if (self.action == "maint"):
			self.doMaint()
			
		if (self.action == "7lw"):
			self.do7lw(self.inputFile, self.windowSize)
				
	
	


