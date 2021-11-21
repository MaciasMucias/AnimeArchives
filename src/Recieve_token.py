# This file is launched on my computer to decrypt

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

import requests
import json

NEW_USER = ""

# decrypt the token that the friend sent over
with open("Encrypted_Token", "rb") as f:
    new_encrypted = [f.read(256) for i in range(10)]
    new_code_verifier = f.read()

with open("../._secrets/private_key.pem", "rb") as key_file:
    private_key = serialization.load_pem_private_key(
        key_file.read(),
        password=None,
        backend=default_backend()
    )

original_message = []
for i in new_encrypted:
    original_message.append(private_key.decrypt(
        i,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    ).decode('utf8'))

RECEIVED_TOKEN = ''.join(original_message)

with open("Verification_Code", "rb") as f:
    code_verifier = f.read().decode('utf-8')


# send the request for the access and refresh tokens
def get_access_token(code_verifier, authorisation_code):
    with open('../.secrets/client_id') as f:
        client_id = f.readline()

    url = 'https://myanimelist.net/v1/oauth2/token'
    data = {
        'client_id': client_id,
        'code': authorisation_code,
        'code_verifier': code_verifier,
        'grant_type': 'authorization_code'
    }

    response = requests.post(url, data)
    response.raise_for_status()  # Check whether the requests contains errors

    token = response.json()
    response.close()
    print('Token generated successfully!')

    # save the tokens to the tokens folder
    with open(f'../Tokens/{NEW_USER}Token.json', 'w') as file:
        json.dump(token, file, indent=4)
        print(f'Token saved in "{NEW_USER}Token.json"')

    return token


get_access_token(code_verifier, RECEIVED_TOKEN)
