# import os
# from requests.auth import HTTPBasicAuth
# import requests
# from dotenv import load_dotenv

# # Load environment variables from .env file
# load_dotenv()

# # Jira credentials and configuration from environment
# JIRA_DOMAIN = os.getenv("JIRA_DOMAIN")
# JIRA_EMAIL = os.getenv("JIRA_EMAIL")
# JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")
# JIRA_PROJECT_KEY = os.getenv("JIRA_PROJECT_KEY")

# auth = HTTPBasicAuth(JIRA_EMAIL, JIRA_API_TOKEN)

# def fetch_jira_issues(query, num_results=15):
#     jql_query = (
#         f'project = {JIRA_PROJECT_KEY} '
#         f'AND status = Done '
#         f'AND (summary ~ "{query}" OR description ~ "{query}") '
#         f'ORDER BY created DESC'
#     )
    
#     url = f"{JIRA_DOMAIN}/rest/api/3/search"

#     headers = {
#         "Accept": "application/json",
#         "Content-Type": "application/json"
#     }

#     params = {
#         "jql": jql_query,
#         "maxResults": num_results,
#         "fields": "summary,description"
#     }

#     response = requests.get(
#         url,
#         headers=headers,
#         params=params,
#         auth=auth
#     )

#     if response.status_code == 200:
#         issues = response.json().get("issues", [])
#         return [{
#             "title": issue['fields']['summary'],
#             "description": issue['fields'].get('description', {}).get('content', [{}])[0].get('content', [{}])[0].get('text', ''),
#             "link": f"{JIRA_DOMAIN}/browse/{issue['key']}"
#         } for issue in issues]
#     else:
#         print("❌ Jira API Error:", response.status_code, response.text)
#         return []







import streamlit as st
import requests
from requests.auth import HTTPBasicAuth

# Load credentials from Streamlit secrets
JIRA_DOMAIN = st.secrets.get("JIRA_DOMAIN", "")
JIRA_EMAIL = st.secrets.get("JIRA_EMAIL", "")
JIRA_API_TOKEN = st.secrets.get("JIRA_API_TOKEN", "")
JIRA_PROJECT_KEY = st.secrets.get("JIRA_PROJECT_KEY", "")

# Validate environment variables
if not all([JIRA_DOMAIN, JIRA_EMAIL, JIRA_API_TOKEN, JIRA_PROJECT_KEY]):
    st.error("❌ Missing one or more JIRA credentials in secrets.toml.")
    st.stop()

# Ensure domain starts with https://
if not JIRA_DOMAIN.startswith("http"):
    JIRA_DOMAIN = "https://" + JIRA_DOMAIN

auth = HTTPBasicAuth(JIRA_EMAIL, JIRA_API_TOKEN)

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

    try:
        response = requests.get(
            url,
            headers=headers,
            params=params,
            auth=auth
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Jira API Error: {e}")
        return []

    issues = response.json().get("issues", [])

    formatted_issues = []
    for issue in issues:
        summary = issue["fields"]["summary"]
        desc_blocks = issue["fields"].get("description", {}).get("content", [])
        description = ""
        if desc_blocks:
            try:
                description = desc_blocks[0]["content"][0].get("text", "")
            except (KeyError, IndexError):
                description = ""

        formatted_issues.append({
            "title": summary,
            "description": description,
            "link": f"{JIRA_DOMAIN}/browse/{issue['key']}"
        })

    return formatted_issues
