"""
run_unitest.py

"""

import unittest
import json
import copy
from app import app
from app.mail import Mail


class EmailAbstractTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.goodParams = {
            'to': 'fake@example.com',
            'to_name': 'Ms. Fake',
            'from': 'noreply@uber.com',
            'from_name': 'Uber',
            'subject': 'A Message from Uber',
            'body': '<h1>Your Bill</h1><p>$10</p>'
            }

    def test_success_mailgun(self):
        app.config['PROVIDER'] = "mailgun"
        rv = self.app.post('/email', data=json.dumps(self.goodParams), content_type="application/json")
        assert '"success": "true"' in rv.data

    def test_success_mandrill(self):
        app.config['PROVIDER'] = "mandrill"
        rv = self.app.post('/email', data=json.dumps(self.goodParams), content_type="application/json")
        assert '"success": "true"' in rv.data

    def test_success_default(self):
        del app.config['PROVIDER']
        rv = self.app.post('/email', data=json.dumps(self.goodParams), content_type="application/json")
        assert '"success": "true"' in rv.data

    def test_post_missing_param(self):
        tempParams = copy.deepcopy(self.goodParams)
        del tempParams['body']
        rv = self.app.post('/email', data=json.dumps(tempParams), content_type="application/json")
        assert '"success": "false"' in rv.data
        assert '"reason": "Missing required parameter"' in rv.data

    def test_post_invalid_email(self):
        tempParams = copy.deepcopy(self.goodParams)
        tempParams['to'] = "$*#&#*@fake.com"
        rv = self.app.post('/email', data=json.dumps(tempParams), content_type="application/json")
        assert '"success": "false"' in rv.data
        assert '"reason": "Email address is not valid syntax"' in rv.data


class MailTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.goodParams = {
            'to': 'fake@example.com',
            'to_name': 'Ms. Fake',
            'from': 'noreply@uber.com',
            'from_name': 'Uber',
            'subject': 'A Message from Uber',
            'body': '<h1>Your Bill</h1><p>$10</p>'
            }

    def test_missing_body(self):
        tempParams = copy.deepcopy(self.goodParams)
        del tempParams['body']
        self.assertRaises(KeyError, Mail, tempParams)

    def test_post_invalid_email(self):
        tempParams = copy.deepcopy(self.goodParams)
        tempParams['to'] = "$*#&#*@fake.com"
        self.assertRaises(ValueError, Mail, tempParams)

if __name__ == '__main__':
    unittest.main()
