import pyttsx3
import os
from flask import Flask, render_template, request, url_for
from scraper import scraper
from summarizer import summarizer, estimated_reading_time

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form.get('url')

        try:
            article_title, text = scraper(url)
            summary = summarizer(text)
            reading_time = estimated_reading_time(summary.split())

            engine = pyttsx3.init()
            engine.say(summary)
            engine.runAndWait()

            return render_template("index.html", article_title = article_title, reading_time = reading_time, summary = summary)
        
        except Exception as e:
            error_message = 'Invalid URL entered'
            return render_template("index.html", error_message = error_message)

    else: 
        return render_template("index.html")

if __name__ == "__main__":
    app.run(debug = True)