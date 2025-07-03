import requests

def fetch_stackoverflow_posts(query, num_results=10):
    url = "https://api.stackexchange.com/2.3/search/advanced"
    params = {
        "order": "desc",
        "sort": "relevance",
        "q": query,
        "site": "stackoverflow",
        "accepted": True,
        "filter": "withbody",
        "pagesize": num_results
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return [{
            "title": item.get("title", "No Title"),
            "description": item.get("body", ""),
            "link": item.get("link", "#"),
            "preview": item.get("body", "")[:200],
            "score": 0,
            "source": "StackOverflow"
        } for item in data.get("items", [])]
    else:
        print("❌ StackOverflow API Error:", response.status_code, response.text)
        return []
