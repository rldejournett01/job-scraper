# test_serpapi.py
from serpapi import GoogleSearch

params = {
    "engine": "google_jobs",
    "q": "software engineer",
    "location": "United States",
    "api_key": "YOUR_API_KEY"
}

search = GoogleSearch(params)
results = search.get_dict()
print(results.keys())
