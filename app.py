# import streamlit as st
# from jira_api import fetch_jira_issues
# from matcher import match_posts

# st.set_page_config(page_title="BugMatch - Jira AI", layout="centered")
# st.title("BugSense: AI-Powered Jira Bug Matcher")

# query = st.text_area("🐞 Paste your bug/error message here:")

# if st.button("🔎 Find Similar Jira Issues"):
#     with st.spinner("Thinking..."):
#         jira_issues = fetch_jira_issues(query)

#         if not jira_issues:
#             st.warning("❌ No results found from Jira. Try rephrasing the error.")
#         else:
#             st.info(f"🐞 Jira returned {len(jira_issues)} issues.")

#             for i, issue in enumerate(jira_issues[:3]):
#                 st.markdown(f"**Issue {i+1}: [{issue['title']}]({issue['link']})**")
                
#                 # Fix: safely convert description to string
#                 raw_desc = issue.get('description', '')
#                 desc_str = str(raw_desc)
#                 short_desc = desc_str.replace("\n", " ")
                
#                 st.caption(short_desc[:200] + "..." if len(short_desc) > 200 else short_desc)

#             matches = match_posts(query, jira_issues)

#             st.write("🧠 Match Titles:", [m['title'] for m in matches] if matches else "None")

#             if matches:
#                 st.success(f"✅ Found {len(matches)} similar issues:")
#                 for match in matches:
#                     st.markdown(f"**🔗 [{match['title']}]({match['link']})**")
#                     st.caption(f"Similarity Score: `{match['score']:.2f}`")
#             else:
#                 st.error("❌ No similar resolved Jira issues found. Try changing the wording or details.")










# 





import streamlit as st
from jira_api import fetch_jira_issues
from matcher import match_posts
from streamlit_lottie import st_lottie
import requests
from PIL import Image

# ---- Safe Helper to load Lottie animations ----
def load_lottieurl(url: str):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except Exception as e:
        st.warning(f"❌ Could not load Lottie animation: {e}")
        return None

# Load animations
ai_lottie = load_lottieurl("https://assets6.lottiefiles.com/packages/lf20_tno6cg2w.json")  # AI bot
search_lottie = load_lottieurl("https://assets4.lottiefiles.com/packages/lf20_puciaact.json")  # Search
error_lottie = load_lottieurl("https://assets2.lottiefiles.com/packages/lf20_jcikwtux.json")  # Error Dev

# Page setup
st.set_page_config(page_title="BugSense - Smart Jira Matcher", page_icon="🐛", layout="wide")

# Sidebar branding
with st.sidebar:
    st.image("https://i.ibb.co/dQ6zwhv/bugsense-logo.png", width=180)
    st.markdown("## 👨‍💻 Built by Team BugSense")
    st.markdown("🔗 [GitHub](https://github.com/dushyanttyagi29/bug_hackathon)")
    st.markdown("📬 [Email](mailto:your.email@example.com)")
    st.markdown("---")
    if ai_lottie:
        st_lottie(ai_lottie, height=180)
    else:
        st.info("🤖 Welcome to BugSense!")

# App header
st.markdown("""
    <div style="text-align: center;">
        <h1 style="color:#4CAF50;">🐞 BugSense</h1>
        <h3>🔍 Smart Jira Bug Matcher Powered by AI</h3>
        <p style="color:gray;">Paste an error message and find related Jira issues instantly.</p>
    </div>
""", unsafe_allow_html=True)

# Main app layout
query = st.text_area("📋 Enter your bug/error message here:", height=160, placeholder="e.g. NullPointerException in Login.java on line 42")

col1, col2 = st.columns([1, 2])

with col1:
    if st.button("🔎 Match Issues", use_container_width=True):
        if not query.strip():
            st.warning("⚠️ Please enter a valid error message.")
        else:
            with st.spinner("🧠 Thinking with AI..."):
                jira_issues = fetch_jira_issues(query)

            if not jira_issues:
                st.error("❌ No related issues found in Jira.")
                if error_lottie:
                    st_lottie(error_lottie, height=180)
            else:
                st.success(f"✅ Found {len(jira_issues)} related Jira issues.")
                st.markdown("### 📂 Top Jira Issues")

                for i, issue in enumerate(jira_issues[:3]):
                    with st.container():
                        st.markdown(f"**🔗 [{issue['title']}]({issue['link']})**")
                        desc = str(issue.get("description", "")).replace("\n", " ")
                        st.caption(desc[:200] + "..." if len(desc) > 200 else desc)
                        st.divider()

                st.markdown("### 🤖 AI Similarity Matching")

                matches = match_posts(query, jira_issues)
                if matches:
                    for match in matches:
                        with st.container():
                            st.markdown(f"**🔗 [{match['title']}]({match['link']})**")
                            st.progress(int(match['score'] * 100))
                            st.caption(f"🧠 Similarity Score: `{match['score']:.2f}`")
                            st.divider()
                else:
                    st.warning("❌ No high similarity found. Try changing the error message.")

with col2:
    if search_lottie:
        st_lottie(search_lottie, height=400)

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center;'>🚀 Built with ❤️ by BugSense | © 2025</p>", unsafe_allow_html=True)
