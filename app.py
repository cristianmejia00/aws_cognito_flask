from flask import Flask, redirect, request
from dotenv import load_dotenv
import requests
import boto3
import os


# Load environment variables from .env
load_dotenv(os.getenv('AWS_ACCESS_KEY_ID'))

# Initiate flask app
app = Flask(__name__)

# Initiate AWS SDK
client = boto3.client('cognito-idp', region_name='us-east-1')

# Endpoints
@app.route('/')
def home():
    return "<p>Hello, world!<p>"

@app.route('/login')
def login():
    return redirect(f"{os.getenv('COGNITO_DOMAIN')}/login?client_id={os.getenv('CLIENT_ID')}&response_type=code&scope=email+openid+phone&redirect_uri={os.getenv('REDIRECT_URI')}")

@app.route('/logged_in', methods=['GET'])
def logged_in():
    # Get the code from the URL
    code = request.args.get('code', None)

    # Token endpoint URL
    token_url = f"{os.getenv('COGNITO_DOMAIN')}/oauth2/token"

    # Headers and payload for the POST request
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    payload = {
        'grant_type': 'authorization_code',
        'client_id': os.getenv('CLIENT_ID'),
        'redirect_uri': os.getenv('REDIRECT_URI'),
        'code': code
    }

    # Making the POST request
    response = requests.post(token_url, headers=headers, data=payload)

    # Handling the response
    if response.status_code == 200:
        # Successful token exchange
        tokens = response.json()
        print("Access Token:", tokens['access_token'])
        print("ID Token:", tokens['id_token'])
        print("Refresh Token:", tokens['refresh_token'])
        
        # Get the user data
        user_data = client.get_user(AccessToken=tokens['access_token'])
        return user_data
        
    else:
        # Handle errors
        return f"Error exchanging code for tokens: {response.text}"




@app.route('/logout')
def logout():
    pass

if __name__ == "__main__":
    app.run(debug = True,  host='0.0.0.0', port=8080)