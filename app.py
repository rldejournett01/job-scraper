from flask import Flask, render_template, request, send_file
from scraper import scrape_remoteok, scrape_google_jobs
import pandas as pd
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    jobs = []
    keyword = ""
    location = ""
    loading = False

    if request.method == "POST":
        keyword = request.form["keyword"]
        location = request.form.get("location", "")
        loading = True  

        remoteok_jobs = scrape_remoteok(keyword) # doesnt support location filter yet. 
        google_jobs = scrape_google_jobs(keyword)

        jobs = remoteok_jobs + google_jobs
        if jobs:
            df = pd.DataFrame(jobs)
            df.to_csv("jobs.csv", index=False)

        loading = False

    return render_template("index.html", jobs=jobs, keyword=keyword, location=location, loading=loading)

@app.route("/download")
def download_csv():
    return send_file("jobs.csv", as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
