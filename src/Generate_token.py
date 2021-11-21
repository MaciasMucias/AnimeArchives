# This file is sent to my friend who want for their anime list to be archived

import secrets
import json
import os
from urllib.parse import urlencode, urlparse
from http.server import HTTPServer, BaseHTTPRequestHandler
import webbrowser
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

from Auth import Serv, get_auth_url, get_new_code_verifier

# create and open a request link for request token generation
code_verifier = get_new_code_verifier()
auth_url = get_auth_url(code_verifier, 'user')
webbrowser.open(auth_url)

# create a server that will wait for response after user authorises access
# it will handle one request and shut down
httpd = HTTPServer(('localhost', 8800), Serv)
httpd.handle_request()


# server creates a tmp file with token information (simplest solution)
with open('tmp', 'r') as f:
    query = json.loads(f.readline())
os.remove('tmp')

# as tokens will be sent over the internet (and for playing around with cryptography)
# they are encrypted using a public key
with open("../.secrets/public_key.pem", "rb") as key_file:
    public_key = serialization.load_pem_public_key(
        key_file.read(),
        backend=default_backend()
    )


message = query['code'].encode('utf8')
# The message is split into 10 equal parts and each part is encoded individually
size = len(message)
n = 10
parts = [message[size//n*i:size//n*(i+1)] for i in range(n)]


encrypted = []
for i in parts:
    encrypted.append(public_key.encrypt(
        i,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    ))


with open("../Encrypted_Token", 'wb') as f:
    for i in encrypted:
        f.write(i)

# Verification code isn't encrypted

with open("Verification_Code", "wb") as f:
    f.write(code_verifier.encode("utf-8"))

