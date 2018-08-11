#!/usr/bin/python

# Version: 20170825-2015

# Opens dictionary and checks for a word, pattern, substitution encrypted word, or jumble. 

"""
Usage: python dict.py -os [mac | win] -action [search | genmask | jumblept2 | maint | 7lw ] {-debug}
About searches: find a word, pattern (like ABBC), substitution encoded word (like GBRRCB),
 or jumbled word (like ISFH, returns fish).
	Params for -action search: -searchtype [word | pattern | encword | jumble] -target targetPhrase 
	Params for -action jumblept2: -target letterList -windowsize n  
	Params for -action 7lw: -infile filename (a 7LW data file) -windowsize n (target word length)  
	Params for -action genmask: -target targetPhrase 
	Params for -action maint: -mainttype [ gensortcolumn | addword ] -target word_to_add 
 	Note: search for word or encword returns first match, pattern returns all matches.

"""

import sys
from DictionaryTools import DictionaryEngine

#### EXECUTION Starts Here ####

de = DictionaryEngine(sys.argv)

# If startup parameters are OK do action specified.
if (not de.bInitOK):
	de.showUsage()
	sys.exit()
else:
	de.doAction()
	
	

	



