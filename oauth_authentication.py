import os
import webbrowser
import threading
import requests
from flask import Flask, request

app=Flask(__name__)

#CONSTANTS
BITBUCKET_ACCESS_URL="https://bitbucket.org/site/oauth2/access_token"
BITBUCKET_AUTHORIZE="https://bitbucket.org/site/oauth2/authorize"

#AUTHENTICATION INFO
CLIENT_KEY=os.getenv("CLIENT_KEY")
CLIENT_SECRET=os.getenv("CLIENT_SECRET")
HEADERS={"Content-Type": "application/json"}

stop_event = threading.Event()
auth_code = None

def start_web_server():
    app.run(port=3000)

@app.route('/callback')
def callback():
    global auth_code
    auth_code=request.args.get('code')
    stop_event.set()
    return "Authorization code received!"

def get_token():
    data = {"grant_type": "authorization_code", "code": auth_code}
    response = requests.post(url=BITBUCKET_ACCESS_URL, auth=(CLIENT_KEY, CLIENT_SECRET), data=data)

    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        print("Error:", response.status_code, response.text)

def authenticate():
    webbrowser.open(f"{BITBUCKET_AUTHORIZE}?client_id={CLIENT_KEY}&response_type=code")
    server_thread = threading.Thread(target=start_web_server, daemon=True)
    server_thread.start()

    stop_event.wait()
    print("Flask server has stopped")

    access_token=get_token()

    return access_token

