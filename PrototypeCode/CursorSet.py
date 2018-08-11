
class CursorSet:

	def __init__(self, cursorCount, maxValue):
		self.cvCount = cursorCount
		self.maxVal = maxValue
		self.nextIdx2Move = cursorCount-1 # zero based indexes
		self.cursorVals = []		
		for x in range(0,self.cvCount):
			self.cursorVals.append(x)


	def getNextAvailableIndex(self, startAt):
	
		ic = startAt
		bIndexAvailable = False
		while (not bIndexAvailable):
			# determine if another cv is using this index
			bIndexUsed = False
			for x in range(self.cvCount):
				if (self.cursorVals[x] == ic):
					bIndexUsed = True
					break
			
			if (bIndexUsed):
				ic += 1
			else:
				bIndexAvailable = True

		return ic

			
	def step(self):
	
		# increment the "one's" digit, skipping indexes in use.
		ci = self.cursorVals[self.nextIdx2Move] + 1
		self.cursorVals[self.nextIdx2Move] = self.getNextAvailableIndex(ci)  
		if (self.cursorVals[self.nextIdx2Move] > self.maxVal):
			# "one's" digit maxed out, carry the one to the left,
			#  checking for max outs and carrying again if needed.
			bCarryDone = False
			carryIndex = self.nextIdx2Move - 1
			while(not bCarryDone):
				if(self.cursorVals[carryIndex] < self.maxVal):
					ci = self.cursorVals[carryIndex] + 1
					self.cursorVals[carryIndex] = self.getNextAvailableIndex(ci)
					bCarryDone = True
				else:
					carryIndex -= 1
					
				if(carryIndex < 0):
					# give up, no more carry positions.
					bCarryDone = True
					
			# init all positions to the right of the carry index
			# This is optimized to skip index values currently in use.
			for x in range(carryIndex+1, self.cvCount):
				self.cursorVals[x] = self.getNextAvailableIndex(0)
									

	def atEnd(self):
	
		bAtEnd = True 
	
		for x in range(self.cvCount):
			if (self.cursorVals[x] < self.maxVal-x): 
				bAtEnd = False

		return(bAtEnd)
		
		
	def getVals(self):
	
		return(self.cursorVals)
		