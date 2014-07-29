"""
mail.py

"""

from flask import Markup
from app import app
import re
import json
import requests


class Mail():

    def __init__(self, data):
        """All params are required so we access keys directly or throw a KeyError exception
        """
        self.to_addr = self.isValidEmail(data['to'])
        self.to_name = data['to_name']
        self.from_addr = self.isValidEmail(data['from'])
        self.from_name = data['from_name']
        self.subject = data['subject']
        self.body = Markup(data['body']).striptags()

    def isValidEmail(self, email):
        """Basic email sanity check to avoid superfluous API calls
        """
        if re.match("[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}", email, flags=re.IGNORECASE):
            return email
        else:
            raise ValueError('Email address is not valid syntax')

    def sendMailgun(self):
        """Prepares and sends Mailgun API call
        Returns dict with response status
        """
        apiURI = app.config['MAILGUN_API']
        auth = ('api', app.config.get('MAILGUN_KEY'))
        data = {
            "from": self.from_name + " <" + self.from_addr + ">",
            "to": self.to_name + " <" + self.to_addr + ">",
            "subject": self.subject,
            "text": self.body
        }
        response = self.sendPost(apiURI=apiURI, data=data, auth=auth).json()
        if response.get('id'):
            return {"success": "true"}
        else:
            return {
                "success": "false",
                "reason": "Mailgun: " + response.get('message')
                }

    def sendMandrill(self):
        """Prepares and sends Mandrill API call
        Returns dict with response status
        """
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
        response = self.sendPost(apiURI=apiURI, data=data, headers=headers).json()[0]
        if (response.get('status') == 'sent'):
            return {"success": "true"}
        else:
            return {
                "success": "false",
                "reason": "Mandrill: " + response.get('status')
                }

    def sendPost(self, apiURI, data, auth=None, headers=None):
        return requests.post(apiURI, auth=auth, data=data, headers=headers)

    def send(self):
        if app.config.get('PROVIDER') == "mandrill":
            return self.sendMandrill()
        else:
            return self.sendMailgun()
