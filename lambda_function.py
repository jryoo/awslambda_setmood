"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

#from __future__ import print_function

import os
import pprint
import spotipy
import boto3
import spotipy
import spotipy.oauth2 as oauth2
import urllib3
import json

client = boto3.client('lambda')
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
http = urllib3.PoolManager()


SPOTIPY_CLIENT_ID = os.environ['SPOTIPY_CLIENT_ID']
SPOTIPY_CLIENT_SECRET = os.environ['SPOTIPY_CLIENT_SECRET']
SPOTIPY_REDIRECT_URI = os.environ['SPOTIPY_REDIRECT_URI']
SPOTIPY_SCOPE = os.environ['SPOTIPY_SCOPE']
SPOTIPY_TOKEN_INFO = os.environ['SPOTIPY_TOKEN_INFO']
ALEXA_APPLICATION_ID = os.environ['ALEXA_APPLICATION_ID']
ALEXA_TEST_APPLICATION_ID = os.environ['ALEXA_TEST_APPLICATION_ID']
SPOTIPY_DEVICE_ID = os.environ['SPOTIPY_DEVICE_ID']
SPOTIPY_CONTEXT_URI = os.environ['SPOTIPY_CONTEXT_URI']
IFTTT_URI = os.environ['IFTTT_URI']

alexa_trusted_appids = [ALEXA_APPLICATION_ID, ALEXA_TEST_APPLICATION_ID]

# handle new tokens here
def token_info_handler(token_info=None):
    if token_info:
        client.update_function_configuration(
            FunctionName='setMood',
            Environment={
                'Variables': {
                    'SPOTIPY_CLIENT_ID': SPOTIPY_CLIENT_ID,
                    'SPOTIPY_CLIENT_SECRET': SPOTIPY_CLIENT_SECRET,
                    'SPOTIPY_REDIRECT_URI': SPOTIPY_REDIRECT_URI,
                    'SPOTIPY_SCOPE': SPOTIPY_SCOPE,
                    'ALEXA_APPLICATION_ID': ALEXA_APPLICATION_ID,
                    'ALEXA_TEST_APPLICATION_ID': ALEXA_TEST_APPLICATION_ID,
                    'SPOTIPY_TOKEN_INFO': json.dumps(token_info),
                    'SPOTIPY_DEVICE_ID': SPOTIPY_DEVICE_ID,
                    'SPOTIPY_CONTEXT_URI': SPOTIPY_CONTEXT_URI,
                    'IFTTT_URI' : IFTTT_URI
                }
            }
        )
    if SPOTIPY_TOKEN_INFO:
        return json.loads(SPOTIPY_TOKEN_INFO)
    else:
        return None

if not SPOTIPY_CLIENT_ID or not SPOTIPY_CLIENT_SECRET or not SPOTIPY_REDIRECT_URI:
    print('''
        You need to set your Spotify API credentials. You can do this by
        setting environment variables like so:

        export SPOTIPY_CLIENT_ID='your-spotify-client-id'
        export SPOTIPY_CLIENT_SECRET='your-spotify-client-secret'
        export SPOTIPY_REDIRECT_URI='your-app-redirect-url'

        Get your credentials at
            https://developer.spotify.com/my-applications
    ''')
    raise spotipy.SpotifyException(550, -1, 'no credentials set')

cache_path = ".cache-user"
sp_oauth = oauth2.SpotifyOAuth(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET,
    SPOTIPY_REDIRECT_URI, scope=SPOTIPY_SCOPE, cache_path=cache_path,
    token_info_handler=token_info_handler)

# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }

def get_ok_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Setting the mood"
    speech_output = "Setting the mood"
    should_end_session = True
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, None, should_end_session))

def handle_session_end_request():
    session_attributes = {}
    card_title = "Setting the mood Session Ended"
    speech_output = "Setting the mood"
    should_end_session = True
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, None, should_end_session))

# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here

# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])


    # try to get a valid token for this user, from the cache,
    # if not in the cache, the create a new (this will send
    # the user to a web page where they can authorize this app)

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """

    if (event['session']['application']['applicationId'] not in alexa_trusted_appids):
        raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    token_info = sp_oauth.get_cached_token()
    if not token_info:
        print('''
            Invalid or no token
        ''')
        raise spotipy.SpotifyException(401, -1, 'Invalid or no token')

    token = token_info['access_token']
    sp = spotipy.Spotify(auth=token)
    sp.trace = False
    results = sp.start_playback(device_id=SPOTIPY_DEVICE_ID,
        context_uri=SPOTIPY_CONTEXT_URI)
    print(results)
    # print("[<<DEVELOPER>>] launch request:")
    # pp = pprint.PrettyPrinter(indent=4)
    # pp.pprint(event)

    #### trigger IFTTT mood lighting
    r = http.request('GET', IFTTT_URI)
    print("IFTTT request status: " + str(r.status))

    return handle_session_end_request()
    # silently error

    # if event['request']['type'] == "LaunchRequest":
    #     return on_launch(event['request'], event['session'])
    # elif event['request']['type'] == "IntentRequest":
    #     return on_intent(event['request'], event['session'])
    # elif event['request']['type'] == "SessionEndedRequest":
    #     return on_session_ended(event['request'], event['session'])
