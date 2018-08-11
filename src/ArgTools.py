
class ArgParser:

	def __init__(self, argsArray):
		self.args = argsArray

	def isInArgs(self, argName, bWithValue):
	
		rval = False
	
		# walk the args looking for the value
		for idx in range(len(self.args)):
			if (self.args[idx] == argName):
				# determine if a value is expected
				if (not bWithValue):
					# no value needed, just wanted the arg and found it.
					rval = True
				else:
					# 'with value' means there is something after this arg.
					if (len(self.args) > idx+1):
						rval = True
						
		return(rval)
						
	
	def getArgValue(self, argName):

		rval = "NOT_SET"
		
		# walk the args looking for the value
		for idx in range(len(self.args)):
			if ((self.args[idx] == argName) and (len(self.args) > idx+1)):
				# get the value after the current index
				rval = self.args[idx+1]
				
		return(rval)
		
	def isArgWithValue(self, argName, value):

		rval = False
		
		# walk the args looking for the value
		for idx in range(len(self.args)):
			if ((self.args[idx] == argName) and (len(self.args) > idx+1)):
				# get the value after the current index
				argValue = self.args[idx+1]
				
				# test argvalue
				if (argValue == value):
					rval = True
				
		return(rval)
	

				
		