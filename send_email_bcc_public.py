# Sending emails without attachments using Python.

import smtplib 
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Testing a different solution
# from PIL import Image
# from io import BytesIO
# from io import StringIO

def email(email_message, random_word):
	gmail_user = '<youremail@gmail.com>'
	gmail_password = '<your email password>'

	sent_from = gmail_user
	to = gmail_user
	bcc = ['<any email>', '<any email>']
	subject = 'Daily robot for the word ' + random_word
	body_text = email_message

	# Create the container (outer) email message.
	msg = MIMEMultipart()

	msg['Subject'] = subject
	msg['From'] = gmail_user
	msg['To'] = to
	
	text = MIMEText(body_text)
	msg.attach(text)

	imgURL = 'https://robohash.org/' + random_word + '.png'

	body_image ="""
	<!DOCTYPE html>
	<html>
	<head>
	</head>
	<body>
	<img src="{image_embed}" style = "max-width: 40%; max-height: 40%; padding: 5px;">
	</body>
	</html>""".format(image_embed=imgURL) # Python variable in HTML email
	# if there are large number of variables: .format(**locals())
	# cannot center as each email service renders dom different (never able to perfectly center)

	html = MIMEText(body_image, 'html', "utf-8")
	msg.attach(html)

	try:
		server = smtplib.SMTP_SSL('smtp.gmail.com', 465) # SMTP port 465 for SSL
		server.ehlo() # Extended helo clause
		# The SMTP HELO clause is the stage of the SMTP protocol where a SMTP server provides introductions. 
		# The sending server will identify who it is and the receiving server will (as per RFC) accept any given name. 
		# There is no requirement to give the correct information at this stage.
		# https://www.gordano.com/knowledge-base/what-is-the-smtp-heloehlo-clause/
		server.login(gmail_user, gmail_password)
		server.sendmail(sent_from, [to] + bcc, msg.as_string())
		server.close()

		print('\nEmail sent!')
	except Exception as e:
		print('Error sending email: ')
		print(e)

