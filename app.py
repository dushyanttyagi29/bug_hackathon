





# import streamlit as st
# from jira_api import fetch_jira_issues
# from matcher import match_posts
# from streamlit_lottie import st_lottie
# import requests
# from PIL import Image

# # ---- Safe Helper to load Lottie animations ----
# def load_lottieurl(url: str):
#     try:
#         r = requests.get(url)
#         if r.status_code != 200:
#             return None
#         return r.json()
#     except Exception as e:
#         st.warning(f"❌ Could not load Lottie animation: {e}")
#         return None

# # Load animations
# ai_lottie = load_lottieurl("https://assets6.lottiefiles.com/packages/lf20_tno6cg2w.json")  # AI bot
# search_lottie = load_lottieurl("https://assets4.lottiefiles.com/packages/lf20_puciaact.json")  # Search
# error_lottie = load_lottieurl("https://assets2.lottiefiles.com/packages/lf20_jcikwtux.json")  # Error Dev

# # Page setup
# st.set_page_config(page_title="BugSense - Smart Jira Matcher", page_icon="🐛", layout="wide")

# # Sidebar branding
# with st.sidebar:
#     st.image("https://i.ibb.co/dQ6zwhv/bugsense-logo.png", width=180)
#     st.markdown("## 👨‍💻 Built by Team BugSense")
#     st.markdown("🔗 [GitHub](https://github.com/dushyanttyagi29/bug_hackathon)")
#     st.markdown("📬 [Email](mailto:your.email@example.com)")
#     st.markdown("---")
#     if ai_lottie:
#         st_lottie(ai_lottie, height=180)
#     else:
#         st.info("🤖 Welcome to BugSense!")

# # App header
# st.markdown("""
#     <div style="text-align: center;">
#         <h1 style="color:#4CAF50;">🐞 BugSense</h1>
#         <h3>🔍 Smart Jira Bug Matcher Powered by AI</h3>
#         <p style="color:gray;">Paste an error message and find related Jira issues instantly.</p>
#     </div>
# """, unsafe_allow_html=True)

# # Main app layout
# query = st.text_area("📋 Enter your bug/error message here:", height=160, placeholder="e.g. NullPointerException in Login.java on line 42")

# col1, col2 = st.columns([1, 2])

# with col1:
#     if st.button("🔎 Match Issues", use_container_width=True):
#         if not query.strip():
#             st.warning("⚠️ Please enter a valid error message.")
#         else:
#             with st.spinner("🧠 Thinking with AI..."):
#                 jira_issues = fetch_jira_issues(query)

#             if not jira_issues:
#                 st.error("❌ No related issues found in Jira.")
#                 if error_lottie:
#                     st_lottie(error_lottie, height=180)
#             else:
#                 st.success(f"✅ Found {len(jira_issues)} related Jira issues.")
#                 st.markdown("### 📂 Top Jira Issues")

#                 for i, issue in enumerate(jira_issues[:3]):
#                     with st.container():
#                         st.markdown(f"**🔗 [{issue['title']}]({issue['link']})**")
#                         desc = str(issue.get("description", "")).replace("\n", " ")
#                         st.caption(desc[:200] + "..." if len(desc) > 200 else desc)
#                         st.divider()

#                 st.markdown("### 🤖 AI Similarity Matching")

#                 matches = match_posts(query, jira_issues)
#                 if matches:
#                     for match in matches:
#                         with st.container():
#                             st.markdown(f"**🔗 [{match['title']}]({match['link']})**")
#                             st.progress(int(match['score'] * 100))
#                             st.caption(f"🧠 Similarity Score: `{match['score']:.2f}`")
#                             st.divider()
#                 else:
#                     st.warning("❌ No high similarity found. Try changing the error message.")

# with col2:
#     if search_lottie:
#         st_lottie(search_lottie, height=400)

# # Footer
# st.markdown("---")
# st.markdown("<p style='text-align: center;'>🚀 Built with ❤️ by BugSense | © 2025</p>", unsafe_allow_html=True)









import streamlit as st
from jira_api import fetch_jira_issues
from matcher import match_posts

# Page configuration
st.set_page_config(page_title="Bug Search and Explanation using AI", layout="centered")

# Sidebar controls
with st.sidebar:
    st.markdown("## ⚙ Settings")
    mode = st.selectbox("🌈 Appearance Mode", options=["Light", "Dark"], index=0, key="theme_mode", label_visibility="visible")
    selected_date = st.date_input("📅 Filter by Date")

# Theme settings
is_dark = st.session_state.get("theme_mode", "Light") == "Dark"
st.session_state["dark_mode"] = is_dark

# Style variables
if is_dark:
    primary_bg = "#1e1e1e"
    primary_color = "#90caf9"
    text_color = "#ffffff"
    textarea_bg = "#2e2e2e"
    textarea_text = "#ffffff"
    placeholder_color = "#aaaaaa"
    button_bg = "#1565C0"
    button_text_color = "#ffffff"
    button_hover = "#42a5f5"
    label_color = "#ffffff"
    divider_color = "#444"
    sidebar_bg = "#222"
    help_icon_color = "#ffffff"
else:
    primary_bg = "#f5f5f5"
    primary_color = "#0D47A1"
    text_color = "#222222"
    textarea_bg = "#ffffff"
    textarea_text = "#000000"
    placeholder_color = "#888888"
    button_bg = "#0D47A1"
    button_text_color = "#ffffff"
    button_hover = "#2196F3"
    label_color = "#222222"
    divider_color = "#999"
    sidebar_bg = "rgba(255, 255, 255, 0.6)"
    help_icon_color = "#000000"

# Inject styles
st.markdown(f"""
    <style>
    body, .stApp {{
        background-color: {primary_bg};
        color: {text_color};
    }}
    .fade-in {{ animation: fadeIn 0.6s ease-in forwards; opacity: 0; }}
    @keyframes fadeIn {{ to {{ opacity: 1; }} }}

    .stTextArea textarea {{
        background-color: {textarea_bg} !important;
        color: {textarea_text} !important;
        border-radius: 10px;
        border: 1px solid #cccccc !important;
        box-shadow: none !important;
    }}
    .stTextArea textarea:hover,
    .stTextArea textarea:focus,
    .stTextArea textarea:active {{
        border: 1px solid {button_hover} !important;
        outline: none !important;
    }}
    .stTextArea textarea::placeholder {{ color: {placeholder_color} !important; }}

    .stButton > button {{
        background-color: {button_bg} !important;
        color: {button_text_color} !important;
        border-radius: 8px;
        border: none !important;
    }}
    .stButton > button:hover {{ background-color: {button_hover} !important; }}

    div[data-testid="stHorizontalBlock"] label {{ color: {label_color} !important; }}

    section[data-testid="stSidebar"] > div:first-child {{
        background: {sidebar_bg};
        backdrop-filter: blur(12px);
        border-radius: 12px;
        box-shadow: 0 0 8px rgba(0, 0, 0, 0.1);
    }}

    .stTextArea div[data-testid="stMarkdownContainer"] svg {{
        color: {help_icon_color} !important;
    }}

    footer {{ display: none !important; }}
    </style>
""", unsafe_allow_html=True)


# App header
st.markdown("""
    <div style="text-align: center;">
        <h1 style="color:#4CAF50;">🐞 BugSense</h1>
        <p style='font-size: 1rem;'>🔍 Smart Jira Bug Matcher Powered by AI</p>
        <p style="color:gray;">Paste an error message and find related Jira issues instantly.</p>
    </div>
""", unsafe_allow_html=True)


# Main UI
# st.markdown(f"""
#     <h1 style='color: {primary_color};'>🔎 Bug Search and Explanation using AI</h1>
#     <p style='font-size: 1.1rem;'>Paste your bug or error message below and let AI help you find similar solutions from trusted sources.</p>
# """, unsafe_allow_html=True)

query = st.text_area("", height=150, placeholder="e.g. NullPointerException in Login.java on line 42", help="Paste the error or bug message you're encountering.")

col1, col2 = st.columns([1, 4])
with col1:
    search_clicked = st.button("Find Solutions", use_container_width=True)

with col2:
    st.markdown(f"""
        <div style='display: flex; align-items: center; height: 100%;'>
            <p style='font-size: 0.9rem; color: gray; margin: 0;'>
                Your input will be processed securely. Results are based on semantic similarity with Jira tickets.
            </p>
        </div>
    """, unsafe_allow_html=True)

# Processing and results
if search_clicked:
    with st.spinner("Analyzing your error and fetching similar ticket..."):
        so_posts =  fetch_jira_issues(query)
        if not so_posts:
            st.warning("❌ No results found from Jira. Try rephrasing the error.")
        else:
            matches = match_posts(query, so_posts)
            if matches:
                st.success(f"✅ Found {len(matches)} similar questions:")
                for match in matches:
                    with st.container():
                        st.markdown(f"<div class='fade-in'><h4><a href='{match['link']}' target='_blank'>{match['title']}</a></h4></div>", unsafe_allow_html=True)
                        st.caption(f"Similarity Score: {match['score']:.2f}")
            else:
                st.error("❌ No similar resolved issues found. Try changing the wording or details.")

# Footer
# st.markdown(f"""
#     <div style='width: 100%; text-align: center; margin-top: 4rem;'>
#         <hr style='margin: 0 auto; width: 50%; border: 1px solid {divider_color};'>
#         <p style='font-size: 0.85rem; color: gray;'>
#             This tool follows WCAG accessibility standards for color contrast, layout, and keyboard navigation.
#         </p>
#     </div>
# """, unsafe_allow_html=True)

#Footer
st.markdown("---")
st.markdown("<p style='text-align: center;'>Built with ❤️ by BugSense | © 2025</p>", unsafe_allow_html=True)