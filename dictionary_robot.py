# version of project to open in terminal or command prompt

# import libraries
import requests
import json # the parsed data is in json format
import webbrowser
import random

# using the following API for random words: https://random-word-api.herokuapp.com/home
# Possible alternative: https://www.wordgenerator.net/
# https://www.wordgenerator.net/application/p.php?id=dictionary_words&type=1&spaceflag=false
# https://www.wordgenerator.net/application/p.php?id=dictionary_words&type=2&spaceflag=false - with definition

def get_random_word():
	try:
		url = 'https://random-word-api.herokuapp.com/word?number=1'
		random_word = requests.get(url).json()
		return random_word[0]

	except Exception as e:
		  print('requesting a random word failed. Here is the exception: ')
		  print(e)

# using the (unofficial) Google Dictionary API found here: https://dictionaryapi.dev/

def get_definition(word):
	# API Format: https://api.dictionaryapi.dev/api/v2/entries/<language_code>/<word>
		url = 'https://api.dictionaryapi.dev/api/v2/entries/en/' + word
		dictionary_data = requests.get(url).json()
		# JSON strings may come as an list with a dictionary inside, 
		# so access the dictionary directly by accessing item 0, as seen above.

		# print(dictionary_data) - testing
		definitions = dictionary_data[0]['meanings'] # definitions is a list with dictionary objects
		definitions_list = [] # list to help handle words with multiple definitions

		# print(definitions) - testing
		# Testing: confirm if definitions is an list or dictionary
		"""if isinstance(definitions, dict):
			print('definitions is a dict')
		else:
			print('definitions is a list')"""
		# Using lists as they are native to Python. Use case is general, as no functions such as math is being performed

		if definitions:
			for i in definitions:

				# create a local dictionary using {}
				full_definition = {
					'partOfSpeech': i['partOfSpeech'],
					'definition': i['definitions'][0]['definition'],
					}

				# if directly printing is desired:
				# print(i['partOfSpeech'] + ': ', end = '') # print without new line
				# print(i['definitions'][0]['definition'] + ' ')

				definitions_list.append(full_definition) # appending a dictionary into a list
		else:
			return 'No definition available.'
			exit() # do not return empty definitions_list
			# in other words, do not continue onwards after handling exception

		return definitions_list

def get_robot(word):
	try:
		# Uncomment the following if usage of the different image sets from robohash are desired
		# .randint is inclusive of both endpoints
		#random_int = random.randint(1,5)
		url = 'https://robohash.org/' + word # + '?set=set' + str(random_int) 
		return url

	except Exception as e:
		  print('failed requesting a random robot. Here is the exception: ')
		  print(e)

def main():
	print('Running...')
	random_word = ''
	try: 
		random_word = get_random_word()
		# print('Random word: ' + random_word)
		definitions = get_definition(random_word)
		random_robot_url = get_robot(random_word)
	except Exception as e:
		# print('error: ')
		# print(e) # error: 0 -> key error due to altered JSON string received when no definitions are found
		# the returned string does not featured an array that we can choose the first object ([0]) from 
		main()
		exit() # do not continue onwards after handling exception

	print('-- Get Random Word --')
	print('Random word: ' + random_word)

	print('-- Get Definition --')
	if isinstance(definitions, str):
		print(definitions)
	else:
		for i in definitions:
			print(i['partOfSpeech'] + ": " + i['definition'])

	print('-- Get Random Robot --')
	print('URL of randomly generated robot based on word: ' + random_robot_url)
	webbrowser.open(random_robot_url) # open link

if __name__ == "__main__":
	main()
