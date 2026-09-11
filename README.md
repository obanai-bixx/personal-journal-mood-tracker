# Personal Journal Mood Tracker Using NLP

## 1. Open this folder in VS Code

## 2. Create a virtual environment

Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

## 3. Install requirements
```bash
pip install -r requirements.txt
```

## 4. Run the project
```bash
python app.py
```

## 5. Open in browser
Go to:
http://127.0.0.1:5000

## Project flow
Closed journal -> Open animation -> Journal entry -> Python VADER analysis -> Result -> History -> Mood graph

## Files
- app.py: Flask backend + VADER NLP
- templates/: HTML screens
- static/style.css: complete vintage diary design and animation
- data/mood_history.csv: saved journal entries