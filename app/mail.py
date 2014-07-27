from flask import Markup
from app import app
import json
import requests

class Mail():
	def __init__(self, data):
		self.to_addr = self.isValidEmail(data['to'])
		self.to_name = data['to_name']
		self.from_addr = data['from']
		self.from_name = data['from_name']
		self.subject = data['subject']
		self.body = Markup(data['body']).striptags()

	def isValidEmail(self, email):
		return email
		raise ValueError('Email address is not valid syntax')

		
	def sendMailgun(self):
		apiURI = app.config['MAILGUN_API']
		auth = ('api', app.config.get('MAILGUN_KEY'))
		data = {
			"from": self.from_name + " <" + self.from_addr + ">",
			"to": self.to_name + " <" + self.to_addr + ">",
			"subject": self.subject,
			"text": self.body
		}
		response = self.sendPost(apiURI=apiURI, data=data, auth=auth)
		if response.json().get('id'):
			return {"success": "true"}
		else:
			return {"success": "false"}


	def sendMandrill(self):
		headers = {'content-type': 'application/json'}
		apiURI = app.config['MANDRILL_API']
		data = {
			"key": app.config.get('MANDRILL_KEY'),
			"message": {
				"from_email": self.from_addr,
				"from_name": self.from_name,
				"to": [
					{
						"email": self.to_addr,
						"name": self.to_name,
						"type": "to"
					}
				],
				"subject": self.subject,
				"text": self.body
			}
		}
		data = json.dumps(data)
		response = self.sendPost(apiURI=apiURI, data=data, headers=headers)
		if (response.json()[0].get('status') == 'sent'):
			return { "success": "true" }
		else:
			return { "success": "false" }

	def sendPost(self, apiURI, data, auth=None, headers=None):
		return requests.post(apiURI, auth=auth, data=data, headers=headers)

	def send(self):
		if app.config['PROVIDER'] == "mailgun":
			return self.sendMailgun()
		elif app.config['PROVIDER'] == "mandrill":
			return self.sendMandrill()
