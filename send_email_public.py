# Sending emails without attachments using Python.

import smtplib 
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# asks for gmail account credentials as gmail SMTP server settings are being used

def email(email_message, random_word):
	gmail_user = '<youremail@gmail.com>'
	gmail_password = '<your email password>'

	sent_from = gmail_user
	to = ['<any email>']
	subject = 'Daily robot for the word ' + random_word
	body_text = email_message

	# Create the container (outer) email message.
	msg = MIMEMultipart()

	msg['Subject'] = subject
	msg['From'] = gmail_user
	msg['To'] = ', '.join(to)
	
	text = MIMEText(body_text)
	msg.attach(text)

	imgURL = 'https://robohash.org/' + random_word + '.png'

	body_image ="""
	<!DOCTYPE html>
	<html>
	<head>
	</head>
	<body>
	<img src="{image_embed}">
	</body>
	</html>""".format(image_embed=imgURL) # Python variable in HTML email
	# if there are large number of variables: .format(**locals())

	html = MIMEText(body_image, 'html', "utf-8")
	msg.attach(html)

	try:
		# connect and authenticate in order to send an email
		server = smtplib.SMTP_SSL('smtp.gmail.com', 465) # SMTP port 465 for SSL
		server.ehlo()
		server.login(gmail_user, gmail_password)
		server.sendmail(sent_from, to, msg.as_string())
		server.close()

		print('\nEmail sent!')
	except Exception as e:
		print('\nError sending email: ')
		print(e)

