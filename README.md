# aws_cognito_flask
Connecting Flask app to AWS cognito's user pool


## Requirements
Assuming we want to set emails to our users from a verified account and domain
- a domain we own and have access to its DNS records
- an email address

Optionally, we would need to opt in for Cognito to send messages in our behalf.
This option is for testing purposes and is limited to 50 emails per day. 


## Key configuration during pool creation
This step is necessary to exchange code for token.
- When creating the app client, thick `Generate a client secret`. 
- When selecting about `OpenID connect scopes`, be sure to thick the boxes `aws.cognito.signin.user.admin` and `profile`.
    - `aws.cognito.signin.user.admin` allows to perform operations using boto3
    - `profile` will bring all user data in the ID token. Otherwise we get only email and ID. 

## Hosted UI
The hosted UI link is located in
```
Amazon Cognito > 
User pools > 
{Your User Pool} > 
App integration > 
App client list > 
{Your app client} > 
Hosted UI > 
View Hosted UI
```
Copy the URL.

In the same location verify that the callback and signout urls correctly point to your routes.
![Alt text](image.png)

When using the hosted UI we cannot require the user to fill `custom attributes` at signup. 
We either create our own sign up form, or set them programatically (e.g., with boto3), or create a form for the user to fill after registration. 

---
Notes: 

How to get the user data.
__by user data we mean the user attributes we set when creating the user pool__
To get **all** attributes we must pass `profile` as part of the scope string in the login URL of the Hosted UI. (see line 24 in app.py)
When users log in we receive the code in the callback url. This is then exchanged by tokens.
- ID token: User data
- access token: Authorization code for the user to interact with our app (for eaxmaple retrieve or update his/her user data)
- refresh token: to re-generate the ID and access tokens. The refresh token has a longer life than the other two (30 days vs 1 hour by default)

Option 1 - JWT:
The `ID Token` is a JWT that contains the user data. If we decode it we can get the user attributes.
In Python we can decode it with the PyJWT package. The encoding is RS256.

Option 2 - /oauth2/userInfo (this is what we use in this code)
Use the `access token` as Authorization when calling the GET /oauth2/userInfo endpoint.

Option 3 - Boto3:
Basically a wrapper of the above.
The access token mus contain the `aws.cognito.signin.user.admin` scope. This is set when invoquing the hosted UI (see line 24)
```python
import boto3
client = boto3.client('cognito-idp', region_name='us-east-1')
response = client.get_user(
    AccessToken=access_token
)
response.json()
```

- About custom user attributes:
    - >"AWS says that at this moment, unfortunately, it is not possible to show the custom attributes on the Cognito hosted UI sign-up page. Also, the custom attributes cannot be marked as “required”."
    - >"As for the second Question. Custom attributes will not be reflected in the Users/Groups area until they are added to the user, which, again, cannot be done through the Hosted UI."