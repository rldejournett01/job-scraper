from flask import Flask, render_template, request, send_file
from scraper import scrape_remoteok, scrape_google_jobs
import pandas as pd
import os
from dotenv import load_dotenv
import requests
import concurrent.futures

load_dotenv()
app = Flask(__name__)

def get_economy_news():
    api_key = os.getenv('NEWS_API')
    url = f"https://newsdata.io/api/1/news?apikey={api_key}&q=economy&country=us&language=en&category=business"

    try:
        response = requests.get(url)
        data = response.json()
        articles = data.get("results", [])[:5] # Showing the top 5 articles
        return articles
    except Exception as e:
        print(f"Error fetching economy news: {e}")
        return []



@app.route("/", methods=["GET", "POST"])
def index():
    jobs = []
    keyword = ""
    location = ""
    loading = False
    economy_news = []

    if request.method == "POST":
        keyword = request.form["keyword"]
        location = request.form.get("location", "")
        loading = True  

        # #Run scrapes syncronoulsy
        # remoteok_jobs = scrape_remoteok(keyword) 
        # google_jobs = scrape_google_jobs(keyword)

        #Run scrapes in parallel
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_remoteok = executor.submit(scrape_remoteok, keyword)
            future_google = executor.submit(scrape_google_jobs, keyword, location)

            remoteok_jobs = future_remoteok.result()
            google_jobs = future_google.result()


        jobs = remoteok_jobs + google_jobs

        if jobs:
            df = pd.DataFrame(jobs)
            df.to_csv("jobs.csv", index=False)

        loading = False
        economy_news = get_economy_news()

    return render_template("index.html", jobs=jobs, keyword=keyword, location=location, loading=loading, economy_news=economy_news)

@app.route("/download")
def download_csv():
    return send_file("jobs.csv", as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
