import requests

def fetch_reddit_posts(query, num_results=10):
    url = "https://api.pushshift.io/reddit/search/submission/"
    params = {
        "q": query,
        "subreddit": "learnprogramming+python+java",
        "size": num_results,
        "sort": "desc",
        "sort_type": "score"
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json().get("data", [])
        return [{
            "title": post.get("title", "No Title"),
            "description": post.get("selftext", ""),
            "link": f"https://reddit.com{post.get('permalink', '')}",
            "preview": post.get("selftext", "")[:200],
            "score": 0,
            "source": "Reddit"
        } for post in data if post.get("selftext")]
    else:
        print("❌ Reddit API Error:", response.status_code, response.text)
        return []
