from canva_secret import canva_client_id, canva_secret
import os
import hashlib
import base64
import random
import string
from flask import Flask, request, redirect
import requests
import secrets
import from dotenv

allowed_chars = string.ascii_letters + string.digits + '-._~'

# Function to generate a code_verifier
def generate_code_verifier(length=128):
    if not 43 <= length <= 128:
        raise ValueError("Code verifier must be between 43 and 128 characters long.")
    
    # Use secrets to generate a cryptographically secure random string
    code_verifier = ''.join(secrets.choice(allowed_chars) for _ in range(length))
    
    return code_verifier


# Generate code_verifier
code_verifier = generate_code_verifier()
print(code_verifier)

# Function to generate code_challenge from code_verifier using SHA-256
def generate_code_challenge(code_verifier):
    # Step 1: Hash the code_verifier with SHA-256
    sha256_hash = hashlib.sha256(code_verifier.encode('utf-8')).digest()
    
    # Step 2: Encode the result in URL-safe Base64 without padding
    code_challenge = base64.urlsafe_b64encode(sha256_hash).decode('utf-8').replace('=', '')
    
    return code_challenge

# Generate code_challenge from the code_verifier
code_challenge = generate_code_challenge(code_verifier)

Authorization_url = f"https://www.canva.com/api/oauth/authorize?code_challenge_method=s256&response_type=code&client_id=OC-AZI5UsSmaEqh&redirect_uri=http%3A%2F%2F127.0.0.1%3A3000%2Fcallback%2F&scope=app:read%20app:write%20design:content:read%20design:content:write%20design:permission:read%20design:permission:write%20asset:read%20asset:write%20brandtemplate:meta:read%20brandtemplate:content:read&code_challenge={code_challenge}"

print(Authorization_url)



app = Flask(__name__)

@app.route('/callback', methods=["GET"])
def callback():
    
    authorization_code = request.args.get('code')
    
    if authorization_code:
        print(f"Authorization code received: {authorization_code}")
        token_response = exchange_code_for_token(authorization_code)
        return token_response
    else:
        return "Authorization code not found", 400
    
    
def exchange_code_for_token(authorization_code):
    token_url = "client_credentials"
    client_id = canva_client_id
    client_secret = canva_secret
    redirect_uri = "http://127.0.0.1:3000/"
    
    
    token_data = {
        'grant_type': 'authorization_code',
        'code': authorization_code,
        'redirect_uri': redirect_uri,
        'client_id': client_id,
        'client_secret': client_secret
    }
    
    
    response = requests.post(token_url, data=token_data)
    
    if response.status_code == 200:
        
        return response.json()  
    else:
        return f"Failed to get access token: {response.status_code}", 400

#if __name__ == '__main__':
    #app.run(debug=True, port=3000)
    
    


