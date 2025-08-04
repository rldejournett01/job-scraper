import pandas as pd
import requests
from bs4 import BeautifulSoup
from serpapi import GoogleSearch
import os
from dotenv import load_dotenv

def scrape_google_jobs(keyword='engineer',location='United States'):
    api_key = os.getenv("SERP_APIKEY")  # 🔒 Replace with your key
    params = {
        "engine": "google_jobs",
        "q": keyword,
        "hl": "en",
        "location": location or "United States",
        "api_key": api_key
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    jobs = results.get("jobs_results", [])

    job_data = []

    for job in jobs:
        job_data.append({
            "title": job.get("title", "N/A"),
            "company": job.get("company_name", "N/A"),
            "link": job.get("share_link", "N/A"),
            "location": job.get("location", "N/A"),
            "salary": job.get("salary", "N/A"),
            "source": "Google Jobs"
        })

    return job_data


def scrape_remoteok(keyword='engineer'):
    url = f"https://remoteok.com/remote-dev+{keyword}-jobs"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    jobs = soup.find_all("tr", class_="job")

    job_data = []

    for job in jobs:

        #skip closed/inactive jobs
        if "closed" in job.get("class", []):
            continue

        #check for verified badge
        verified = job.find("span", class_="verified")
        if not verified:
            continue




        title_tag = job.find("h2")
        company_tag = job.find("h3")
        link_tag = job.find("a", {"itemprop": "url"})

        if not (title_tag and company_tag and link_tag):
            continue

        # 🔍 LOCATION & SALARY extraction
        location = "N/A"
        salary = "N/A"

        meta_divs = job.find_all("div", class_="location tooltip")
        for div in meta_divs:
            text = div.get_text(strip=True)
            if "💰" in text:
                salary = text.replace("💰", "").strip()
            else:
                location = div.get("title") or text


        if title_tag and company_tag and link_tag:
            job_data.append({
                "title": title_tag.get_text(strip=True),
                "company": company_tag.get_text(strip=True),
                "link": "https://remoteok.com" + link_tag["href"],
                "location": location,
                "salary": salary,
                "source": "RemoteOK"
            })

    return job_data

# Optional: Add DuckDuckGo and WeWorkRemotely here, but beware of scraping blocks
