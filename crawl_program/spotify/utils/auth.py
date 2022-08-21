import requests
import base64
from requests.auth import HTTPBasicAuth
from requests_oauthlib import OAuth2Session


# Using Spotify Client Credentials Flow
def getAccessToken(clientID, clientSecret):
    # curl -X "POST" -H "Authorization: Basic ZjM4ZjAw...WYØMzE=" -d grant type=client credentials https ://accounts.spotify.com/api/token
    authUrl = "https://accounts.spotify.com/api/token"
    authHeader = {}
    authData = {}

    # Base64 Encode Client ID and Client Secret
    message = f"{clientID}:{clientSecret}"
    message_bytes = message.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode('ascii')
    # print(base64_message)

    authHeader['Authorization'] = "Basic " + base64_message
    authData['grant_type'] = "client_credentials"
    res = requests.post(authUrl, headers=authHeader, data=authData)
    # print(res)
    responseObject = res.json()
    # print(json.dumps(responseObject, indent=2))
    accessToken = responseObject['access_token']
    return accessToken


# Using Authorization Code Flow
def getAuthorizationToken(clientID, clientSecret, scope):
    # Credentials you get from registering a new application
    redirect_uri = 'https://www.ccgcccccc.xyz'

    # OAuth endpoints given in the Spotify API documentation
    # https://developer.spotify.com/documentation/general/guides/authorization/code-flow/
    authorization_base_url = "https://accounts.spotify.com/authorize"
    token_url = "https://accounts.spotify.com/api/token"

    spotify = OAuth2Session(clientID, scope=scope, redirect_uri=redirect_uri)

    # Redirect user to Spotify for authorization
    authorization_url, state = spotify.authorization_url(
        authorization_base_url)
    print('Please go here and authorize: ', authorization_url)

    # Get the authorization verifier code from the callback url
    redirect_response = input('\nPaste the full redirect URL here: ')
    print()

    auth = HTTPBasicAuth(clientID, clientSecret)

    # Fetch the access token
    token = spotify.fetch_token(token_url, auth=auth,
                                authorization_response=redirect_response)
    # print(token, end='\n\n')
    return spotify, token


# GET request headers
def getHeader(token):
    return {
        "Authorization": "Bearer " + token,
        "accept-language": "zh-CN"
    }


# POST request headers
def postHeader(token):
    return {
        "Content-Type": "application/json"
    }
