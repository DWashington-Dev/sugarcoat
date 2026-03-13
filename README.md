# sugarCoat

Never wonder what your glucose data actually means again.

SugarCoat is a glucose companion app built by a Type 1 Diabetic, for Type 1 Diabetics. It connects to your Dexcom CGM, stores your readings, and uses AI to give you the kind of analysis your endocrinologist would give you. If you saw them for more than 15 minutes twice a year.

## Why I Built This

Living with Type 1 Diabetes means your CGM is basically a second brain. It tracks and reminds you of everything sugar related, around the clock. But most of that data just sits there unused. The average Type 1 Diabetic has no idea how to read their Clarity reports or assess their own patterns without an endocrinologist walking them through it. SugarCoat was built to change that. It finds the patterns, spots the gaps, and explains what is going on in a friendly, lifestyle-focused way. No medical degree required.

## What It Does

- **Dexcom Integration:** Connects to your CGM via OAuth and pulls real glucose data
- **Local Storage:** Saves every reading to a local database so nothing gets lost
- **Pattern Detection:** Tracks trends, values, and timestamps over time
- **AI Analysis:** Plain-English lifestyle insights powered by Anthropic Claude Sonnet 4.6

## Tech Stack

**Backend:** Python, Flask
**Database:** SQLite, SQLAlchemy
**API:** Dexcom API v3
**AI:** Anthropic Claude Sonnet 4.6

## Roadmap

- Predictive glucose modeling using time-series ML
- PDF upload support for Dexcom Clarity reports
- Mobile-friendly dashboard
- Web deployment

## Environment Configuration

Create a `.env` file in the `learning:labs` directory:
```
DEXCOM_CLIENT_ID=your_client_id_here
DEXCOM_CLIENT_SECRET=your_client_secret_here
DEXCOM_REDIRECT_URI=http://localhost:5000/callback
```

## Running Locally

1. Clone the repo
```bash
git clone https://github.com/DWashington-Dev/sugarcoat.git
cd sugarcoat/learning:labs
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Start the server
```bash
python3 app.py
```

The app will be available at `http://localhost:5000`
