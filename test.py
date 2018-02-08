from api import Fitbit

import os

CLIENT_ID = os.environ['CLIENT_ID']
CLIENT_SECRET = os.environ['CLIENT_SECRET']
TOKEN = os.environ['TOKEN']
REFRESH_TOKEN = os.environ['REFRESH_TOKEN']
REDIRECT_URI = os.environ['REDIRECT_URI']
EXPIRES_AT = float(os.environ['EXPIRES_AT'])

def refresh(d):
    print d

fitbit = Fitbit(
    CLIENT_ID,
    CLIENT_SECRET,
    access_token=TOKEN,
    refresh_token=REFRESH_TOKEN,
    expires_at=EXPIRES_AT,
    redirect_uri=REDIRECT_URI,
    refresh_cb=refresh,
    timeout=10,
)

print fitbit.set_bodyweight(161)