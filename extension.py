import argparse
import json
import threading
import time

import urllib.request


# Spam a test message to event log once per minute

# Arguments
parser = argparse.ArgumentParser()

parser.add_argument("--apiUrl", help="API URL")
parser.add_argument("--name", help="Extension name")
parser.add_argument("--authToken", help="API session token")
parser.add_argument("--settingsPath", help="Setting directory")
parser.add_argument("--logPath", help="Log directory")
parser.add_argument("--debug", help="Enable debug mode", dest='debug', action='store_true')
parser.set_defaults(debug=False)

args = parser.parse_args()


# Initialize API request
message = {
	'text': 'Test message sent by extension {}'.format(args.name),
	'severity': 'info'
}

postRequest = urllib.request.Request('http://' + args.apiUrl + 'events')
postRequest.add_header('Authorization', args.authToken)
postRequest.add_header('Content-Type', 'application/json')

# Sending
def sendmessage():
	threading.Timer(60.0, sendmessage).start()
	response = urllib.request.urlopen(postRequest, json.dumps(message).encode('utf-8'))

sendmessage()