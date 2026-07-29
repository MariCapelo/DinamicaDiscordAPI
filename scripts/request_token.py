import requests

API_ENDPOINT = 'https://discord.com/api/v10'
CLIENT_ID = '1531096870384959648'
CLIENT_SECRET = 'dwCqFBygtarFATOCKVaokUbm4fR_AuCE'
REDIRECT_URI = 'http://localhost/discord/redirect'

def exchange_code():
  data = {
    'grant_type': 'authorization_code',
    'code': '0b1MqMBoDqnHBV4Kv0QmGDBdgzFRMp',
    'redirect_uri': REDIRECT_URI
  }
  headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
  }
  r = requests.post('%s/oauth2/token' % API_ENDPOINT, data=data, headers=headers, auth=(CLIENT_ID, CLIENT_SECRET))
  r.raise_for_status()
  return r.json()


resposta = exchange_code()

print(resposta)