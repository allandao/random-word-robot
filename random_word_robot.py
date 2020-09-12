# version of project to run in terminal or command prompt

# import libraries
import requests
import json # the parsed data is in json format
import webbrowser
import random
import send_email

# using the following API for random words: https://random-word-api.herokuapp.com/home

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

		definitions = dictionary_data[0]['meanings'] # definitions is a list with dictionary objects
		definitions_list = [] # list to help handle words with multiple definitions

		if definitions:
			for i in definitions:

				# create a local dictionary using {} to append
				full_definition = {
					'partOfSpeech': i['partOfSpeech'],
					'definition': i['definitions'][0]['definition'],
					}

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
	global email_message 
	email_message = ''
	random_word = ''
	try: 
		random_word = get_random_word()
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
	email_message += ('Random word: ' + random_word + '\n' + '\n')

	print('-- Get Definition --')
	if isinstance(definitions, str):
		print(definitions)
		email_message += (definitions + '\n')
	else:
		for i in definitions:
			print(i['partOfSpeech'] + ": " + i['definition'])
			email_message += (i['partOfSpeech'] + ": " + i['definition'] + '\n')

	print('-- Get Random Robot --')
	print('URL of randomly generated robot based on word: ' + random_robot_url)
	# webbrowser.open(random_robot_url) # open link
	# when automating this script, I don't want it opening anything, just the browser

	email_message += ('\n' + 'URL of randomly generated robot based on word: ' + random_robot_url + '\n')

	# Call the send email method and pass in message and the random word received
	send_email.email(email_message, random_word) 
	# TypeError: 'module' object is not callable
	# The error above will appear if the method within a class is called with no reference to the class
	# or if a class is called with no reference to any methods
	# Ex: send_email(email_message) or only email(email_message)

if __name__ == "__main__":
	print('Running...\n')
	main()
