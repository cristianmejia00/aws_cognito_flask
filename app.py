from flask import Flask, redirect, request
from dotenv import load_dotenv
import requests
import os

# Load environment variables from .env
load_dotenv(os.getenv('AWS_ACCESS_KEY_ID'))

# Initiate flask app
app = Flask(__name__)

# Endpoints
@app.route('/')
def home():
    return "<p>Hello, world!<p>"

@app.route('/login')
def login():
    return redirect(f"{os.getenv('COGNITO_DOMAIN')}/login?client_id={os.getenv('CLIENT_ID')}&response_type=code&scope=email+openid+phone+profile+aws.cognito.signin.user.admin&redirect_uri={os.getenv('REDIRECT_URI')}")

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
        'client_secret':os.getenv('CLIENT_SECRET'),
        'redirect_uri': os.getenv('REDIRECT_URI'),
        'scope': 'profile',
        'code': code
    }

    # Making the POST request
    tokens_response = requests.post(token_url, headers=headers, data=payload)

    # Handling the response
    if tokens_response.status_code == 200:
        # Successful token exchange
        tokens = tokens_response.json()
        #print("Access Token:", tokens['access_token'])
        #print("ID Token:", tokens['id_token'])
        #print("Refresh Token:", tokens['refresh_token'])

        user_info_url = f"{os.getenv('COGNITO_DOMAIN')}/oauth2/userInfo"
        headers = {
            'Authorization': f"Bearer {tokens['access_token']}"
        }
        user_data_response = requests.get(user_info_url, headers=headers)
        print(user_data_response.json())
        
        return 'success!'
        
    else:
        # Handle errors
        return f"Error exchanging code for tokens: {response.text}"


@app.route('/logout')
def logout():
    print('logging out!')
    # Log the user out and redirect her/him to any other page
    #return redirect(f"{os.getenv('COGNITO_DOMAIN')}/logout?client_id={os.getenv('CLIENT_ID')}&logout_uri=http://localhost:8080/logged_out")
    # Automatically return to the log in hosted UI 
    return redirect(f"{os.getenv('COGNITO_DOMAIN')}/logout?client_id={os.getenv('CLIENT_ID')}&response_type=code&scope=email+openid+phone+profile+aws.cognito.signin.user.admin&redirect_uri={os.getenv('REDIRECT_URI')}")

if __name__ == "__main__":
    app.run(debug = True,  host='0.0.0.0', port=8080)