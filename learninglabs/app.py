import pandas as pd
import os # way of talking to your operating system
import secrets 
import requests # separate Python library, it's what you use to make outgoing calls to external APIs
from dotenv import load_dotenv # loading the .env with dexcom client id
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask import Flask, session, jsonify , redirect, render_template, request # imported the 'Flask' library & jsonify is to convert our python contents into a webpage
from flask_sqlalchemy import SQLAlchemy # SQLAlchemy is the tool that lets you talk to a database using Python instead of SQL
import anthropic

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env')) # load the .env file
CLIENT_ID = os.getenv('DEXCOM_CLIENT_ID') 
CLIENT_SECRET = os.getenv('DEXCOM_CLIENT_SECRET') # grabs a specific value out of the .env by name
REDIRECT_URI = os.getenv('DEXCOM_REDIRECT_URI')


app = Flask(__name__) # creating the app and storing it in the 'app' variable
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sugarcoat.db'
app.secret_key = os.getenv('SECRET_KEY')
db = SQLAlchemy(app)
claude = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
limiter = Limiter(
    get_remote_address, # grabs the persons IP address, if too many requests are made from it, you're out.
    app=app,
    default_limits=["200 per day", "50 per hour"]
)

class GlucoseReading(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.String, nullable=False)
    value = db.Column(db.Integer, nullable=False)
    trend = db.Column(db.String)
    trend_rate = db.Column(db.Float)
    
    def __repr__(self):
        return f'<GlucoseReading {self.timestamp}: {self. value}>' # <Global Reading 2026-03-11: 114>

def get_glucose_stats():
    all_readings = GlucoseReading.query.all()
    df = pd.DataFrame([{
        'timestamp': r.timestamp,
        'value': r.value,
        'trend': r.trend
    } for r in all_readings])

    avg = df['value'].mean()
    high = df['value'].max()
    low = df['value'].min()
    in_range = df[(df['value'] >= 70) & (df['value'] <=160)]
    rec_range = df[(df['value'] >=90) & (df['value'] <=130)]
    tir = round(len(in_range) / len(df) * 100, 1)
    rec_tir = round(len(rec_range) / len(df) * 100, 1)
    
    return {
        'avg': round(avg, 1),
        'high': int(high),
        'low': int(low),
        'tir': tir,
        'rec_tir':rec_tir
    }

- Time in Range: {stats['tir']}%

def refresh_access_token():
    response = requests.post(
        "https://sandbox-api.dexcom.com/v3/oauth2/token",
        data={
            "grant_type": "refresh_token",
            "refresh_token": session['refresh_token'],
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
        }
    )
    tokens = response.json()
    session['access_token'] = tokens['access_token']
    session['refresh_token'] = tokens['refresh_token']

@app.route('/') # when someone visits the homepage ('/'), run this below:
def index():
    return render_template('index.html') # this the function that runs when someone hits the '/' route

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
    print("CLIENT_ID:", CLIENT_ID) 
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
    session['access_token'] = tokens['access_token']
    session['refresh_token'] = tokens['refresh_token']

    return redirect('/') # converts the dictionary back into JSON and sends to the browser to see token data

@app.route('/glucose') # This is what powers the dashboard chart
def glucose():
    response = requests.get(
        "https://sandbox-api.dexcom.com/v3/users/self/egvs",
        headers={
            "Authorization": "Bearer " + session['access_token']
        },
        params={
            "startDate": "2026-03-10T00:00:00",
            "endDate": "2026-03-20T00:00:00"
        }
    )
    if response.status_code == 401:
        refresh_access_token()
        response = requests.get(
            "https://sandbox-api.dexcom.com/v3/users/self/egvs",
            headers={"Authorization": "Bearer " + session['access_token']},
            params={"startDate": "2026-03-10T00:00:00", "endDate": "2026-03-20T00:00:00"}
        )

    data = response.json()

    for reading in data['records']:
        existing = GlucoseReading.query.filter_by(timestamp=reading['systemTime']).first()
        if not existing:
            new_reading = GlucoseReading(
                timestamp=reading['systemTime'],
                value=reading['value'],
                trend=reading['trend'],
                trend_rate=reading.get('trendRate')
            )
            db.session.add(new_reading)

    db.session.commit()
    return jsonify(data)

@app.route('/readings')
def readings():
    all_readings = GlucoseReading.query.order_by(GlucoseReading.timestamp.asc()).all()
    return jsonify([{
        'timestamp': r.timestamp,
        'value': r.value,
        'trend': r.trend
    } for r in all_readings])

@app.route('/stats')
def stats():
    stats = get_glucose_stats()
    return jsonify(stats)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route("/range") # powers data range selection
def range():
    response = requests.get(
        "https://sandbox-api.dexcom.com/v3/users/self/dataRange",
        headers={
            "Authorization": "Bearer " + session['access_token']
        }
    )
    return jsonify(response.json())

@app.route('/analyze', methods=['POST'])
@limiter.limit("5 per hour")
def analyze():
    life_choices = request.get_json()
    stats = get_glucose_stats()

    user_message = f"""
    Glucose Stats:
    - Average: {stats['avg']} mg/dl
    - High: {stats['high']} mg/dl
    - Low: {stats['low']} mg/dl
    - Time in Range: {stats['tir']}%
    - Recommended Time in Range: {stats['rec_tir']}%

    Lifestyle:
    - Diet: {life_choices['diet']}
    - Activity: {life_choices['activity']}
    - CGM Engagement: {life_choices['cgm']}
    - Dosing behavior: {life_choices['dosing']}
    """

    response = claude.messages.create(
        model = "claude-sonnet-4-6",
        max_tokens = 1024,
        system = """You are a knowledgeable T1D analysis assistant, similar to an endocrinologist reviewing glucose data between appointments.

Given a user's glucose stats and lifestyle inputs, provide a warm, plain-English analysis formatted in markdown that includes:
- An "Uncoated" summary paragraph of overall patterns
- **Bolded keywords** for important clinical terms and findings
- Key points written as complete sentences, not fragments
- A "Sugar Rushes" section identifying likely causes of highs
- A "Sugar Crashes" section identifying likely causes of lows  
- An "Off the Charts" section for outliers and unusual patterns most endocrinologists might miss
- 2-3 specific, actionable suggestions under "Next Steps"

Tone: warm, supportive, direct, never judgmental. Write like a knowledgeable friend explaining things over coffee, not a doctor writing a clinical report. Avoid medical jargon — if a technical term is necessary, explain it in plain English immediately after. No emojis. No medical disclaimers. Speak directly to the user.""",

        messages =[
            {"role": "user", "content": user_message}
        ]
    ) 

    return jsonify({'analysis': response.content[0].text})

if __name__ == '__main__': # only start the server if youre running this file directly (app.py)
    with app.app_context():
        db.create_all()
    app.run(debug=True) # if i change code, the server restarts
