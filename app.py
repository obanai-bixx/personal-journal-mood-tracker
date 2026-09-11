from flask import Flask, render_template, request, redirect, url_for
from importlib import import_module
from datetime import datetime
import csv
import os

app = Flask(__name__)

SentimentIntensityAnalyzer = import_module(
    "vaderSentiment.vaderSentiment"
).SentimentIntensityAnalyzer
analyzer = SentimentIntensityAnalyzer()
DATA_DIR = "data"
CSV_FILE = os.path.join(DATA_DIR, "mood_history.csv")

os.makedirs(DATA_DIR, exist_ok=True)

if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["date", "text", "mood", "compound", "positive", "neutral", "negative"])


def classify_mood(compound):
    if compound >= 0.05:
        return "Positive"
    elif compound <= -0.05:
        return "Negative"
    return "Neutral"


def interpretation_for(mood):
    if mood == "Positive":
        return "Your words suggest a positive emotional tone. Keep holding on to the moments that make you feel this way."
    elif mood == "Negative":
        return "Your words suggest a difficult emotional tone. Consider giving yourself some space to reflect and reach out to someone you trust if you need support."
    return "Your words suggest a balanced or neutral emotional tone. Your entry may contain mixed feelings or mostly factual thoughts."


def save_entry(entry):
    with open(CSV_FILE, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([
            entry["date"],
            entry["text"],
            entry["mood"],
            entry["compound"],
            entry["positive"],
            entry["neutral"],
            entry["negative"],
        ])


def read_history():
    entries = []
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    row["compound"] = float(row["compound"])
                    row["positive"] = float(row["positive"])
                    row["neutral"] = float(row["neutral"])
                    row["negative"] = float(row["negative"])
                    entries.append(row)
                except (ValueError, TypeError):
                    pass
    return entries


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/journal")
def journal():
    return render_template("journal.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    text = request.form.get("journal_entry", "").strip()

    if not text:
        return redirect(url_for("journal"))

    scores = analyzer.polarity_scores(text)
    compound = scores["compound"]
    mood = classify_mood(compound)

    entry = {
        "date": datetime.now().strftime("%d %b %Y, %I:%M %p"),
        "text": text,
        "mood": mood,
        "compound": round(compound, 3),
        "positive": round(scores["pos"], 3),
        "neutral": round(scores["neu"], 3),
        "negative": round(scores["neg"], 3),
    }

    save_entry(entry)

    return render_template(
        "analysis.html",
        entry=entry,
        interpretation=interpretation_for(mood)
    )


@app.route("/history")
def history():
    entries = list(reversed(read_history()))
    return render_template("history.html", entries=entries)

@app.route("/graph")
def graph():
    entries = read_history()

    labels = []
    values = []

    for entry in entries:
        try:
            date_str = entry["date"].split(",")[0].strip()
            parsed_date = datetime.strptime(date_str, "%d %b %Y")

            labels.append(parsed_date.strftime("%d %b"))
            values.append(round((entry["compound"] + 1) * 50, 1))

        except Exception as e:
            print("GRAPH ERROR:", e)

    print("GRAPH LABELS:", labels)
    print("GRAPH VALUES:", values)

    return render_template(
        "graph.html",
        labels=labels,
        values=values
    )
if __name__ == "__main__":
    app.run(debug=True)
