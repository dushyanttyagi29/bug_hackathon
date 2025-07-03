import os
from requests.auth import HTTPBasicAuth
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Jira credentials and configuration from environment
JIRA_DOMAIN = os.getenv("JIRA_DOMAIN")
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")
JIRA_PROJECT_KEY = os.getenv("JIRA_PROJECT_KEY")

auth = HTTPBasicAuth(JIRA_EMAIL, JIRA_API_TOKEN)

def extract_description(description_field):
    try:
        if not description_field or "content" not in description_field:
            return ""
        desc_blocks = description_field["content"]
        text_parts = []
        for block in desc_blocks:
            if "content" in block:
                for sub_block in block["content"]:
                    if sub_block.get("type") == "text":
                        text_parts.append(sub_block.get("text", ""))
        return " ".join(text_parts).strip()
    except Exception as e:
        print("⚠️ Error extracting Jira description:", e)
        return ""

def fetch_jira_issues(query, num_results=15):
    jql_query = (
        f'project = {JIRA_PROJECT_KEY} '
        f'AND status = Done '
        f'AND (summary ~ "{query}" OR description ~ "{query}") '
        f'ORDER BY created DESC'
    )
    
    url = f"{JIRA_DOMAIN}/rest/api/3/search"

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    params = {
        "jql": jql_query,
        "maxResults": num_results,
        "fields": "summary,description"
    }

    response = requests.get(url, headers=headers, params=params, auth=auth)

    if response.status_code == 200:
        issues = response.json().get("issues", [])
        results = []
        for issue in issues:
            summary = issue['fields']['summary']
            raw_description = issue['fields'].get('description', {})
            clean_description = extract_description(raw_description)
            results.append({
                "title": summary,
                "description": clean_description,
                "preview": clean_description[:200],
                "link": f"{JIRA_DOMAIN}/browse/{issue['key']}",
                "score": 0,
                "source": "Jira"
            })
        return results
    else:
        print("❌ Jira API Error:", response.status_code, response.text)
        return []
