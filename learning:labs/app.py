import os # way of talking to your operating system
import secrets 
from dotenv import load_dotenv # loading the .env with dexcom client id
import requests # separate Python library, it's what you use to make outgoing calls to external APIs

access_token = None
load_dotenv() # load the .env file

CLIENT_ID = os.getenv('DEXCOM_CLIENT_ID') 
CLIENT_SECRET = os.getenv('DEXCOM_CLIENT_SECRET') # grabs a specific value out of the .env by name
REDIRECT_URI = os.getenv('DEXCOM_REDIRECT_URI')

from flask import Flask , jsonify , redirect, request # imported the 'Flask' library & jsonify is to convert our python contents into a webpage
from flask_sqlalchemy import SQLAlchemy # SQLAlchemy is the tool that lets you talk to a database using Python instead of SQL

app = Flask(__name__) # creating the app and storing it in the 'app' variable
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sugarcoat.db'
db = SQLAlchemy(app)

class GlucoseReading(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.String, nullable=False)
    value = db.Column(db.Integer, nullable=False)
    trend = db.Column(db.String)
    trend_rate = db.Column(db.Float)
    
    def __repr__(self):
        return f'<GlucoseReading {self.timestamp}: {self. value}>' # <Global Reading 2026-03-11: 114>

@app.route('/') # when someone visits the homepage ('/'), run this below:
def home():
    return "SugarCoat is ALIVE" # this the function that runs when someone hits the '/' route

@app.route('/data') # when someone visits the data page ('/data'), run this below:
def data(): # will replace with real data soon
    readings = [
        {"time": "8:00am", "glucose": 138},
        {"time": "9:00am", "glucose": 142}, # COMMAS AFTER THE SQUIGLY BRACKETS!
        {"time": "10:00am", "glucose": 135}
    ]
    return jsonify(readings) # TIP: press tab so its in the section....

@app.route('/about') # when someone visits the about page ('/about'), run this below:
def about(): # "define [page]", could become an about page
    return "Sugarcoat is a personal glucose companion for Type 1 diabetics. It connects to your Dexcom CGM data, tracks patterns over time, and uses AI to give you the kind of honest, plain-English analysis your endo doesn't have "

@app.route('/login') # powers the login screeen
def login():
    state = secrets.token_hex(16) # generates a 32-char token string, required in v3
    auth_url = (
        "https://sandbox-api.dexcom.com/v3/oauth2/login?" # running v3 * NOT V2 *
        "client_id=" + CLIENT_ID +
        "&redirect_uri=" + REDIRECT_URI +
        "&response_type=code" + # sends a temporary code after the user logs in
        "&scope=offline_access" + # allows the app to pull data in the background (saves data)
        "&state=" + state
    )
    return redirect(auth_url)

@app.route('/callback') # happens behind the scenes after auth
def callback():
    global access_token
    code = request.args.get('code') # Dexcom sends the auth code back to your callback
    response = requests.post(
        "https://sandbox-api.dexcom.com/v3/oauth2/token", # V3!!
        data={ # triggers the token exchange
            "grant_type": "authorization_code", # trading a code for a token
            "code": code, # the temp code that Dexcom sends
            "redirect_uri": REDIRECT_URI, # has to match what was registered for verification
            "client_id": CLIENT_ID, # app credentials
            "client_secret": CLIENT_SECRET, # app credentials
        }
    )
    tokens = response.json() # Dexcom's response, and .json() converts it from raw text to Python dictonary
    access_token = tokens['access_token']
    return jsonify(tokens) # converts the dictionary back into JSON and sends to the browser to see token data 

@app.route('/glucose') # This is what powers the dashboard chart
def glucose():
    response = requests.get(
        "https://sandbox-api.dexcom.com/v3/users/self/egvs",
        headers={
            "Authorization": "Bearer " + access_token
        },
        params={
            "startDate": "2026-03-01T00:00:00",
            "endDate": "2026-03-11T00:00:00"
        }
    )
    return jsonify(response.json())

@app.route("/range") # powers data range selection
def range():
    response = requests.get(
        "https://sandbox-api.dexcom.com/v3/users/self/dataRange",
        headers={
            "Authorization": "Bearer " + access_token
        }
    )
    return jsonify(response.json())

if __name__ == '__main__': # only start the server if youre running this file directly (app.py)
    with app.app_context():
        db.create_all()
    app.run(debug=True) # if i change code, the server restarts
