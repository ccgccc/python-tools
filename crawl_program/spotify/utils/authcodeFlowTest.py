from auth import *

# Retrive user infomation test


# https://developer.spotify.com/documentation/general/guides/authorization/scopes/
scope = [
    "user-read-email",
    "playlist-read-collaborative"
]
spotify, token = getAuthorizationToken(scope)

# Fetch a protected resource, i.e. user profile
r = spotify.get('https://api.spotify.com/v1/me')
# print(type(r))
print(r.content)
