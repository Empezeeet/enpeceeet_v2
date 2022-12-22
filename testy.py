import requests

API_ENDPOINT = 'https://discord.com/api/v10'
CLIENT_ID = '1055370446347968584'
CLIENT_SECRET = 'wCLOefvgNirx3xsmzuVWEltZNHe3BDzo'
REDIRECT_URI = 'http://localhost:8080/callback'

def refresh_token(refresh_token):
  data = {
    "grant_type": "refresh_token",
    "refresh_token": "j6eKdER7VxU4wxoLtWBrj4yuQgRMAB"
  }
  headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
  }
  r = requests.post('%s/oauth2/token' % API_ENDPOINT, data=data, headers=headers, auth=(CLIENT_ID, CLIENT_SECRET))
  print(r.json())
  r.raise_for_status()
  return r.json()

refresh_token("hdf")