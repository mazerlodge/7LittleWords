class Odometer:

	# mark member variables
	bInitOK = False
	bInDebug = False
	bSegmentListIsCSV = False
	segmentList = "NOT_SET"
	odometer = []
	odometerIndexes = [] 
	windowSize = -1
	
	def __init__(self, segmentList, windowSize, bSegmentListIsCSV, bInDebug):
		self.bInDebug = bInDebug
		if (self.generateOdometer(segmentList, windowSize, bSegmentListIsCSV)):
			self.bInitOK = True
		else:
			print("Init failed in generateOdometer().")
	
	
	def generateOdometer(self, segmentList, windowSize, bSegmentListIsCSV):
		# Called by init to populate the member odometer (array of strings). 
		
		self.windowSize = windowSize
		self.bSegmentListIsCSV = bSegmentListIsCSV
		
		# The number of wheels required is reduced when the 
		#  segment list is a CSV b/c each segment must be at 
		#  least 2 characters.
		numberOfWheels = windowSize
		if (bSegmentListIsCSV):
			numberOfWheels = numberOfWheels / 2
		
		# No shortening of the wheels to remove dupes, 
		#  those dupes are skipped by advanceOdometer().
		for x in range(0,numberOfWheels): 
			self.odometer.append(segmentList)
			self.odometerIndexes.append(x)
			
		self.debugMsg("generateOdometer: wheel indexes at " + self.odometerIndexesToString())
			
		return True # used to return odometer object, now member var.
	
	def debugMsg(self, msg):
		if (self.bInDebug):
			print msg
			
	def isOdometerAtMax(self):
		# Checks each wheel in the odometer to see if all are maxed out.
		rval = False 
		mv = []
		
		numberOfWheels = self.getNumberOfWheels()
		maxCount = 0
		for x in range(0, numberOfWheels):
			wheelLength = self.getOdometerWheelSize(x)
			maxIndexForThisWheel = wheelLength - (numberOfWheels - x)				
			mv.append(maxIndexForThisWheel)
			
			if (self.odometerIndexes[x] == maxIndexForThisWheel):
				maxCount += 1
				
		if (maxCount == numberOfWheels):
			rval = True
				
		return rval

	def getNumberOfWheels(self):
		return len(self.odometer)
	
	def getOdometerWheelSize(self, wheelIndex):
		# Returns the length of a wheel, it is either the length of the wheel 
		#  or the number of segments if csv based.
		rval = -1
		
		# make sure the wheelIndex specified is valid and get that wheel.
		if (wheelIndex > len(self.odometer)):
			return rval
		currentWheel = self.odometer[wheelIndex] 
		
		if (self.bSegmentListIsCSV):
			# Count the number of segments in the specified wheel.
			parts = currentWheel.split(',')
			rval = len(parts)
		else:
			# wheel is just a list of letters, its length is its size.
			rval = len(currentWheel) 
			
		return rval	

	def getOdometerWheelValue(self, wheelNumber):
		# Given a wheelNumber (aka zero-based index in the odometer),
		#   return the value currently pointed to by odometerIndexes for that wheel.
		rval = "NOT_SET" 
		
		# if the specified wheelNumber is too large, exit.
		if (wheelNumber > self.getNumberOfWheels()-1):
			print "ERROR in getOdometerWheelValue(): wheelNumber requested =" + str(wheelNumber)
			return rval
			
		# get current index within the wheel specified
		wheelIndex = self.odometerIndexes[wheelNumber]
		
		# if the wheelIndex is too large exit
		if (wheelIndex > self.getOdometerWheelSize(wheelNumber)-1):
			print "ERROR in getOdometerWheelValue(): wheelIndex requested =" + str(wheelIndex)
			return rval 
			
		# parse based on wheel type (e.g. CSV list or not) 
		if (self.bSegmentListIsCSV):
			# Extract the segments in the specified wheel's CSV list. 
			parts = self.odometer[wheelNumber].split(',')
			
			if (wheelIndex > len(parts)-1):
				rval = "ERROR_WHEEL_INDEX_OUT_OF_RANGE" 
			else:
				rval = parts[wheelIndex]
				
		else:
			# get letter pointed at by wheelIndex.
			rval = self.odometer[wheelNumber][wheelIndex]
			
		return rval
			
	def odometerIndexesToString(self): 
		rval = "["
		
		for x in range(len(self.odometerIndexes)):
			rval += str(self.odometerIndexes[x]) + ", "
			
		rval = rval[0:len(rval)-2] 
		rval += "]"
		
		return rval
		
	def advanceOdometer(self):
		# Chooses between basic and CSV odometer advancement methods.
		# Return number of cycles used (includes skipped positions) 
		rval = 0
		
		if (self.bSegmentListIsCSV):
			rval = self.advanceCSVOdometer()
		else:
			rval = self.advanceBasicOdometer()
			
		return rval
		
	def advanceBasicOdometer(self):
		# Advance the odometer and skip any combos where a letter would be repeated.
		# Said another way, each odometerIndex value must be distinct.
		# Example: given 1-2-0, 1-2-1 is invalid, so is 1-2-2, skip to 1-2-3)
			
		indexToAdvance = -1
		
		# The following is pulled from wheel zero since all wheels are the same length.
		wheelLength = self.getOdometerWheelSize(0)
		numberOfWheels = self.getNumberOfWheels()
		
		cycleCount = 0
		cycleLimit = wheelLength**numberOfWheels
		bDone = False
		while (not bDone): 
			cycleCount += 1
			
			# walk odometer wheels right to left ( <-- )
			for i in range(numberOfWheels-1, -1, -1):
				# max index is of the form 2,3,4 when wheel size is 5 and number of wheels is 3.
				maxIndexForThisWheel = wheelLength - (numberOfWheels - i)
				if (self.odometerIndexes[i] < maxIndexForThisWheel):
					# this index can be advanced 
					indexToAdvance = i
					break
			
			# advance specified index and neighbors to the right
			if (indexToAdvance > -1):
				self.odometerIndexes[indexToAdvance] += 1
				# set all indexes to the right of this one.
				# Use values this high plus 1 per position to the right (e.g. +1, +2, +3,... for neghbors to the right).
				# This ONLY WORKS because this result is used in a context where order of elements doesn't matter.
				# 	(e.g. 012 and 021 are considered dupes so rolling over from 019 to 023 skipping 020 and 021 is desirable)
				#  Note: the step after this will correct any that exceeded the max.
				for x in range(indexToAdvance+1, self.getNumberOfWheels()):
					self.odometerIndexes[x] = self.odometerIndexes[indexToAdvance]+(x-indexToAdvance)

				# The max value is based on combo of number of wheels and position of wheel in the odometer.
				# E.G. With 5 values in each wheel, and 3 wheels, 
				#        max values are 2-3-4 (indexes are zero based).
				for x in range(0, self.getNumberOfWheels()):
					maxIndexForThisWheel = wheelLength - (numberOfWheels - x)
					if (self.odometerIndexes[x] > maxIndexForThisWheel):
						self.odometerIndexes[x] = maxIndexForThisWheel 
			
			# Done if there are no dupes except for all maxes
			bDone = True
			maxCount = 0
			for x in range(0, len(self.odometerIndexes)):
				maxIndexForThisWheel = wheelLength - (numberOfWheels - x)

				# check for dupe values for the value pointed to by this wheel 	
				# the careful selection of index to advance and adjustment of 
				#   neighboring wheels (above) should prevent this from ever happening.		
				if (self.odometerIndexes.count(self.odometerIndexes[x]) > 1): 
					print "WARNING in advanceOdometer(): dupe indexes, handled but should never happen."
					bDone = False
					
				if (self.odometerIndexes[x] == maxIndexForThisWheel):
					maxCount += 1
					
				if (maxCount == numberOfWheels):
					bDone = True
					
			# check governor
			if (cycleCount > cycleLimit):
				print "WARNING in advanceOdometer(): Odometer indexes at " + self.odometerIndexesToString() 
				print "advanceOdometer() hit cycleLimit " + str(cycleLimit) + ", exiting."
				bDone = True
				
		return cycleCount

	def advanceCSVOdometer(self):
		# Advance the odometer and skip any combos where a letter would be repeated.
		# Said another way, each odometerIndex value must be distinct.
		# Example: given 1-2-0, 1-2-1 is invalid, so is 1-2-2, skip to 1-2-3)
		# Note: This version differs from advanceBasicOdometer in that order of elements
		#        matters.  For example, ab+cd+ef is different from ab+ef+cd.
		
		indexToAdvance = -1
		
		# The following is pulled from wheel zero since all wheels are the same length.
		wheelLength = self.getOdometerWheelSize(0)
		numberOfWheels = self.getNumberOfWheels()
		
		cycleCount = 0
		cycleLimit = wheelLength**numberOfWheels
		bDone = False
		while (not bDone): 
			cycleCount += 1
			
			# walk odometer wheels right to left ( <-- )
			for i in range(numberOfWheels-1, -1, -1):
				# max index is of the form 2,3,4 when wheel size is 5 and number of wheels is 3.
				maxIndexForThisWheel = wheelLength - (numberOfWheels - i)
				if (self.odometerIndexes[i] < maxIndexForThisWheel):
					# this index can be advanced 
					indexToAdvance = i
					break
			
			# advance specified index and neighbors to the right
			if (indexToAdvance > -1):
				self.odometerIndexes[indexToAdvance] += 1
				# set all indexes to the right of this one.
				# Use zero-based values offset by wheel position (e.g. 0,1,2...).
				# This DIFFERS FROM advanceBasicOdmeter() where the order of elements doesn't matter.
				#  Note: the step after this will correct any that exceeded the max.
				for x in range(indexToAdvance+1, numberOfWheels):
					# first wheel gets 0, next gets 1, etc.
					indexValueToSet = x - (indexToAdvance + 1)
					self.odometerIndexes[x] = indexValueToSet 

				# The max value is based on combo of number of wheels and position of wheel in the odometer.
				# E.G. With 5 values in each wheel, and 3 wheels, 
				#        max values are 2-3-4 (indexes are zero based).
				for x in range(0, self.getNumberOfWheels()):
					maxIndexForThisWheel = wheelLength - (numberOfWheels - x)
					if (self.odometerIndexes[x] > maxIndexForThisWheel):
						self.odometerIndexes[x] = maxIndexForThisWheel 
			
			# Done if there are no dupes except for all maxes
			bDone = True
			maxCount = 0
			for x in range(0, len(self.odometerIndexes)):
				maxIndexForThisWheel = wheelLength - (numberOfWheels - x)

				# check for dupe values for the value pointed to by this wheel 	
				if (self.odometerIndexes.count(self.odometerIndexes[x]) > 1): 
					bDone = False
					
				if (self.odometerIndexes[x] == maxIndexForThisWheel):
					maxCount += 1
					
				if (maxCount == numberOfWheels):
					bDone = True
					
			# check governor
			if (cycleCount > cycleLimit):
				print "WARNING in advanceOdometer(): Odometer indexes at " + self.odometerIndexesToString() 
				print "advanceOdometer() hit cycleLimit " + str(cycleLimit) + ", exiting."
				bDone = True
				
		return cycleCount 
		
	def getPermutations(self):
		# given the current wheel settings, return permutations that match the
		#  windowSize.  This is only relevant when bSegmentListIsCSV is True. 
		phrases = []
		numberOfWheels = self.getNumberOfWheels() 

		# In some cases, not all of the wheels are required to gen the target window size.
		# e.g. windowsize=7, there are 3 wheels, possible to get 7 with 2 wheels (3+4) 
		
		# Minimum number of wheels is the windowSize / 4 but rounded up on any 
		#   fractional amount.  e.g. 7 / 4 = 1.75 so 2 wheels is the min required. 
		#   The reason 4 is used is that is the max length of a segment.
		minWheels = self.windowSize / 4 
		if (self.windowSize % 4 > 0):
			minWheels += 1
			
		if (minWheels < numberOfWheels): 
			# need to evaluate all permutations of wheel combos to identify phrases
			#   that could be produced by the current wheel settings	
			currentPhrase = ""
			for Wheel2Skip 	in range(numberOfWheels): 
				for Wheel2Read in range (numberOfWheels):
				   if (Wheel2Read != Wheel2Skip):
						currentPhrase += self.getOdometerWheelValue(Wheel2Read) 
					
				if (len(currentPhrase) == self.windowSize):					
					phrases.append(currentPhrase) 
					
				currentPhrase = ""
		
		# after doing wheel skipping (if done), try using all wheels at once.
		currentPhrase = ""
		for Wheel2Read in range (numberOfWheels):
			currentPhrase += self.getOdometerWheelValue(Wheel2Read) 
		
		if (len(currentPhrase) == self.windowSize):					
			phrases.append(currentPhrase) 
					 
		return phrases
		
			
	def readOdometer(self):
		# grab the current odometer setting potential values.
		# for jumbles (bSegmentListIsCSV = False), array always has 1 element.
		# for 7lw (Segment list is a CSV), array may contain multiple elements.
		rval = [] 
		
		if (self.bSegmentListIsCSV):
			rval = self.getPermutations()
			
		else:
			# the concatenation of the letter pointed at by each wheel. 
			phrase = ""
			for x in range(0,len(self.odometer)): 
				phrase += self.getOdometerWheelValue(x)
			rval.append(phrase)
		
		return rval
			