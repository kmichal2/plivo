import os
from flask import Flask, Response, request, url_for
import plivo
import plivoxml

AUTH_ID = 'ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
AUTH_TOKEN = 'YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY'
CALLER_ID = '+12345678901'
BOX_ID = '+12345678901'
MY_URL = 'http://morning-ocean-4669.herokuapp.com/report/'

app = Flask(__name__)


@app.route('/response/speak/', methods=['GET'])
def speak():
    # Enter the message you want to play
    text = "Congratulations! You just made a text to speech app on Plivo cloud!"
    parameters = {'loop': 1, 'language': "en-US", 'voice': "WOMAN"}

    response = plivoxml.Response()
    response.addSpeak(text, **parameters)

    return Response(str(response), mimetype='text/xml')

@app.route('/send', methods=['GET', 'POST'])
def send():
    # Enter the message you want to send
    auth_id = os.environ.get("AUTH_ID", AUTH_ID)
    auth_token = os.environ.get("AUTH_TOKEN", AUTH_TOKEN)
    caller_id = os.environ.get("CALLER_ID", CALLER_ID)
    box_id = os.environ.get("BOX_ID", BOX_ID)
    my_url = os.environ.get("MY_URL", MY_URL)
    params = {
        'src': caller_id, # Sender's phone number with country code
        'dst' : box_id, # Receiver's phone Number with country code
        'text' : u"Hello, how are you?", # Your SMS Text Message - English
        'url' : my_url, # The URL to which with the status of the message is sent
        'method' : 'POST' # The method used to call the url
    }
    if request.method == 'GET':
        response = plivoxml.Response()
        #response.addSpeak(auth_id + auth_token + caller_id + box_id + my_url)
    elif request.method == 'POST':
        p = plivo.RestAPI(auth_id, auth_token)
        response = p.send_message(params)
        
    return Response(str(response), mimetype='text/xml')
    
@app.route('/call', methods=['GET', 'POST'])
def call():
    # Enter the message you want to send
    auth_id = os.environ.get("AUTH_ID", AUTH_ID)
    auth_token = os.environ.get("AUTH_TOKEN", AUTH_TOKEN)
    caller_id = os.environ.get("CALLER_ID", CALLER_ID)
    box_id = os.environ.get("BOX_ID", BOX_ID)
    my_url = os.environ.get("MY_URL", MY_URL)
    client = request.values.get('client')
    params = {
        'from': caller_id, # Caller Id
        'to' : box_id, # User Number to Call
        'ring_url' : my_url+"call",
        'answer_url' : my_url+"call",
        'hangup_url' : my_url+"hangup",
    }
    if request.method == 'GET':
        response = plivoxml.Response()
        response.addSpeak("hello "+client)
        #response.addSpeak(auth_id + auth_token + caller_id + box_id + my_url)
    elif request.method == 'POST':
        response = plivoxml.Response()
        response.addSpeak("hello "+client)
        #p = plivo.RestAPI(auth_id, auth_token)
        #response = p.make_call(params)
        
    return Response(str(response), mimetype='text/xml')
    
@app.route("/hangup", methods=['POST'])
def hangup():
    response = plivoxml.Response()
    return Response(str(response), mimetype='text/xml')

@app.route("/hello", methods=['GET', 'POST'])
def hello():
    """Respond to incoming calls with a simple text message."""
    auth_id = os.environ.get("AUTH_ID", AUTH_ID)
    auth_token = os.environ.get("AUTH_TOKEN", AUTH_TOKEN)
    caller_id = os.environ.get("CALLER_ID", CALLER_ID)
    my_url = os.environ.get("MY_URL", MY_URL)

    response = plivoxml.Response()
    #response.addSpeak(text, **parameters)
    client = request.values.get('client')
    #p = plivo.RestAPI(auth_id, auth_token)

    #response = p.send_message(params)
    response.addSpeak("hello "+client)

    return Response(str(response), mimetype='text/xml')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
