abstract-email
==============
Service to provide abstraction between multiple email service providers

Installation
------------
* Install required python libraries via 

		`pip install -r requirements.txt`

Configuration
-------------
* Copy config.py.sample to config.py and fill in appropriate values

* \*_API should be the full URI to the mail service api e.g. 

		`MANDRILL_API = "https://mandrillapp.com/api/1.0/messages/send.json"`

* PROVIDER can be either "mailgun" or "mandrill" (case sensitive). If not provided, mailgun will be used by default.

Running
-------
* Launch the dev Flask server by running

		`python ./run.py`

Testing
-------
* Launch test suite by running

		`python ./run_unittest.py`

Language & Framework
--------------------
abstract-email uses Python and Flask, mostly because I am most familiar with this duo, but Flask is also particularly suitable because it is quite lightweight and modular, and not much is required by this app besides basic URL routing and request handling. 

Trade-offs/Additional info
--------------------------
* I didn't attempt the extra tasks, but if I had defined the Mail object as a database model from the start, it would have made parameter validation a little more straightforward. 

* If the service was planned to have a few more endpoints, perhaps by implementing the 'opens and clicks' functionality, I may have used a REST plugin such as Flask-RESTless to easily parse and commit the POST data to the database.