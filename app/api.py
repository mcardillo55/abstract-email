from flask import request, jsonify
from app import app
from mail import Mail

@app.route('/email', methods=['POST'])
def email():
	data = request.get_json()
	response = {'success': 'false'}
	try:
		newMail = Mail(data)
	except KeyError:
		response['reason'] = "Missing required parameter"
		return jsonify(response)
	except ValueError as e:
		response['reason'] = str(e)
		return jsonify(response)
	return jsonify(newMail.send())
