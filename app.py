import os
from flask import Flask, Response, request, url_for
import plivoxml

AUTH_ID = 'ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
AUTH_TOKEN = 'YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY'
CALLER_ID = '+12345678901'

app = Flask(__name__)


@app.route('/response/speak/', methods=['GET'])
def speak():
    # Enter the message you want to play
    text = "Congratulations! You just made a text to speech app on Plivo cloud!"
    parameters = {'loop': 1, 'language': "en-US", 'voice': "WOMAN"}

    response = plivoxml.Response()
    response.addSpeak(text, **parameters)

    return Response(str(response), mimetype='text/xml')

@app.route("/hello", methods=['GET', 'POST'])
def hello():
    """Respond to incoming calls with a simple text message."""
    auth_id = os.environ.get("AUTH_ID", AUTH_ID)
    auth_token = os.environ.get("AUTH_TOKEN", AUTH_TOKEN)
    caller_id = os.environ.get("CALLER_ID", CALLER_ID)
    my_url = os.environ.get("MY_URL", "my_url")

    response = plivoxml.Response()
    #response.addSpeak(text, **parameters)
    client = request.values.get('client')
    #p = plivo.RestAPI(auth_id, auth_token)

    #response = p.send_message(params)
    response.addSpeak("client=" + client + auth_id + auth_token + caller_id + my_url)

    return Response(str(response), mimetype='text/xml')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
