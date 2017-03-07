#Here provide user-defined method of mapping unseen words to a
#small finite set depending on prefix, suffixes etc.
import re

def transform(original_word):
#here we're using a very simple rule, categorize the word depend
#on whether it includes numbers or not
	if bool(re.search(r'\d', original_word)):
		return 'SP_NUM' #special class that include numbers
	else:
		return 'SP_CHAR' #special class with no numbers
