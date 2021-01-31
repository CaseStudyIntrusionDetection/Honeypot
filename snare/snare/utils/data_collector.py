import json
import os
import time 
import hashlib
import re
import atexit
from snare.utils.snare_helpers import ConfigValues

class DataCollector():
	"""Collects logs of all received requests.

	"""
    def __init__(self, path):
		"""Constructor.

			Args:
				path (str): Path to the directory where the data should be collected.
		"""
        self.path = path
        if not os.path.isdir(self.path):
            os.makedirs(self.path)

        self.sessionMap = {}
        self.firstEntry = True
        self.id = 0
        self.connection_id = 0
        self.filename = os.path.join( self.path, time.strftime( "%Y-%m-%d_%H-%M-%S" ) + ".json")

        atexit.register(self.endJSON)

    def log(self, method, uri, protocol, header, response_body, emulator, request_body, response_header, cur_sess_id, prev_sess_id, remote_ip, status_code):
		"""Logs a request.

			Args:
				method (str): The request method (GET, POST, ...).
				uri (str): The requested URI.
				protocol (HttpVersion): The HTTP protocol version.
				header (dict): The HTTP headers.
				response_body (str): The body of the response.
				emulator (str): The emulator used by Tanner.
				request_body (dict): The body of the request (e.g. for POST requests).
				response_header (dict): The headers of the response.
				cur_sess_id (str): The id of the current session.
				prev_sess_id (str): The id of the previous session.
				remote_ip (str): The ip address of the remote party that sent the request.
				status_code (str): The status code of the response.
		"""
        if not cur_sess_id in self.sessionMap:
            if prev_sess_id in self.sessionMap:
                self.sessionMap[cur_sess_id] = self.sessionMap[prev_sess_id]
            else:
                self.sessionMap[cur_sess_id] = self.connection_id
                self.connection_id += 1

        uri_str = str(uri)

        protocol_str = 'HTTP/' + str(protocol.major) + '.' + str(protocol.minor)

        header_dict = {}
        for name, value in header.items():
            header_dict[name] = value
        self.clearSessionCookie(header_dict)

        response_header_dict = {}
        for name, value in response_header.items():
            response_header_dict[name] = value
        self.clearSessionCookie(response_header_dict)

        response_body_str = str(response_body)

        if request_body != "":
            request_body_dict = {}
            for name, value in request_body.items():
                request_body_dict[name] = value
        else:
            request_body_dict = ""

        logentry = {
            "id" : self.id,
		    "timestamp" : int(time.time()),
		    "connection-id" : self.sessionMap[cur_sess_id],
		    "request" : {
				"method": method,
				"uri": uri_str,
				"protocol": protocol_str,
				"body": request_body_dict
            },
            "header" : header_dict,
            "sender" : {
                "ip" : remote_ip
            },
			"honeypot" : {
				"used-emulator" : emulator,
				"response-hash" : hashlib.sha512(response_body_str.encode('utf-8')).hexdigest(),
                "response-size" : len(response_body_str),
                "response-status-code" : status_code , 
                "response-header" : response_header_dict
			}
        }

        self.id += 1

        self.appendJSON(logentry)

        if ConfigValues.devMode:
            print(json.dumps(logentry, indent=4, sort_keys=False))

    def endJSON(self):
		"""Finishes the logfile with the closing array bracket.

		"""
        self.appendToLog('\n]')

    def appendJSON(self, logentry):
		"""Appends a given JSON object to the log.

			Args:
				logentry (dict): The JSON object to append.
		"""
        if self.firstEntry:
            string = '[\n'
        else:
            string = ",\n"
        self.firstEntry = False
        string += json.dumps([logentry], indent=4, sort_keys=False)[2:-2] # for indentation
        self.appendToLog(string)

    def appendToLog(self, append):
		"""Appends a string to the logfile.

			Args:
				append (str): The string to be appended to the logfile.
		"""
        if not ConfigValues.devMode:
            f = open(self.filename, "a")
            f.write(append)
            f.close()

    def clearSessionCookie(self, header):
		"""Removes the Tanner session cookie from a given HTTP header.

			Args:
				header (dict): Dictionary containing the HTTP headers.
		"""
        field = ''
        if 'Set-Cookie' in header:
            field = 'Set-Cookie'
        elif 'Cookie' in header:
            field = 'Cookie'

        if field != '': # remove tanner session cookie
            header[field] = re.sub(r'sess_uuid=[0-9a-f\-]+(; )?', '', header[field] )
            if header[field] == '':
                del header[field]