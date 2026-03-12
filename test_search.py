import time
import requests

try:
    print("Testing search endpoint with query 'Metformin'...")
    r = requests.get('http://localhost:8000/search', params={'query': 'Metformin'})
    print(f"Status Code: {r.status_code}")
    if r.status_code == 200:
        data = r.json()
        summary = data.get("ai_summary", "")
        print(f"AI Summary preview: {summary[:100]}...")
    else:
        print(f"Error: {r.text}")
except Exception as e:
    print(f"Request failed: {e}")
