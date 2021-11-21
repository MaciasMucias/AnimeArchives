import secrets
from typing import Dict, Union, Any

import requests
import json
import os
from urllib.parse import urlencode, urlparse
from http.server import HTTPServer, BaseHTTPRequestHandler


def get_new_code_verifier() -> str:
    token = secrets.token_urlsafe(100)
    return token[:128]


def get_auth_url(challenge, status) -> str:
    # read client id from the file
    with open('../.secrets/client_id') as f:
        client_id = f.readline()

    parameters = {
        'response_type': 'code',
        'client_id': client_id,
        'code_challenge': challenge,
        'status': status
    }

    # generate a request link for request token generation
    url = 'https://myanimelist.net/v1/oauth2/authorize?' + urlencode(parameters)
    return url


# a simple server that will receive the token and inform the user about it
class Serv(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        query = urlparse(self.path).query
        query_components = dict(qc.split("=") for qc in query.split("&"))
        with open('tmp', 'w') as f:
            f.write(json.dumps(query_components))
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"<html><head><title>Token odebrany.</title></head>")
        path = os.getcwd()
        self.wfile.write(f"<font size=7>Wygenerowany token znajduje sie w: {path}\\Encrypted_Token <br>"
                         f"Kod weryfikacyjny znajduje sie w: {path}\\Verification_Code</font>".encode("utf-8"))
        self.wfile.write(b"</body></html>")
        return