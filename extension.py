import argparse
import json
import threading
import time
import subprocess

import urllib.request

# Arguments
parser = argparse.ArgumentParser()

parser.add_argument("--appPid", help="APP PID")
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
	'text': 'Test message \nsent by extension {}'.format(args.name),
	'severity': 'info'
}

postRequest = urllib.request.Request('http://' + args.apiUrl + 'events')
postRequest.add_header('Authorization', args.authToken)
postRequest.add_header('Content-Type', 'application/json')

# calling adlchecker.py
def check_adl():
	adlfile = args.settingsPath + "/../../../" + "adlchecker.py"
	threading.Timer(60 * 60 * 24, check_adl).start()
	process = subprocess.run(["python3", adlfile], capture_output=True)
	stdout_as_str = process.stdout.decode("utf-8")
	if "Matched:      0 entries" in stdout_as_str:
		message['text'] = "ADL done, no warnings."
		response = urllib.request.urlopen(postRequest, json.dumps(message).encode('utf-8'))
	else:
		for line in stdout_as_str.splitlines():
			message['text'] = line
			response = urllib.request.urlopen(postRequest, json.dumps(message).encode('utf-8'))


check_adl()
