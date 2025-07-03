# app.py
import streamlit as st
from jira_api import fetch_jira_issues
from stackoverflow_api import fetch_stackoverflow_posts
from matcher import match_posts

# Page configuration
st.set_page_config(page_title="BugSense", page_icon="🐞", layout="centered")

# Sidebar controls
with st.sidebar:
    st.markdown("## ⚙ Settings")
    mode = st.selectbox("🌈 Mode", options=["Light", "Dark"], index=0, key="theme_mode", label_visibility="visible")
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
    success_text = "#d0f0d0"
    alert_bg_success = "#1b4332"
    alert_text_success = "#d8f3dc"
    alert_bg_error = "#671e1e"
    alert_text_error = "#fddede"
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
    divider_color = "#ddd"
    sidebar_bg = "rgba(255, 255, 255, 0.6)"
    help_icon_color = "#000000"
    success_text = "#0f5132"
    alert_bg_success = "#d1e7dd"
    alert_text_success = "#0f5132"
    alert_bg_error = "#f8d7da"
    alert_text_error = "#842029"

# Inject styles
st.markdown(f"""
    <style>
    body, .stApp {{ background-color: {primary_bg}; color: {text_color}; }}
    .fade-in {{ animation: fadeIn 0.6s ease-in forwards; opacity: 0; }}
    @keyframes fadeIn {{ to {{ opacity: 1; }} }}
    .stTextArea textarea {{ background-color: {textarea_bg} !important; color: {textarea_text} !important; border-radius: 10px; border: none !important; box-shadow: none !important; }}
    .stTextArea textarea::placeholder {{ color: {placeholder_color} !important; }}
    .stButton > button {{ background-color: {button_bg} !important; color: {button_text_color} !important; border-radius: 8px; border: none !important; }}
    .stButton > button:hover {{ background-color: {button_hover} !important; }}
    div[data-testid="stHorizontalBlock"] label {{ color: {label_color} !important; }}
    section[data-testid="stSidebar"] > div:first-child {{ background: {sidebar_bg}; backdrop-filter: blur(12px); border-radius: 0px; box-shadow: 0 0 8px rgba(0, 0, 0, 0.1); }}
    .stTextArea div[data-testid="stMarkdownContainer"] svg {{ color: {help_icon_color} !important; }}
    .result-card {{
        background-color: {'#2a2a2a' if is_dark else '#ffffff'};
        border-radius: 12px;
        padding: 1rem;
        margin: 1rem 0;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        box-shadow: 0 2px 6px rgba(0,0,0,0.2);
        position: relative;
    }}
    .result-card:hover {{ transform: scale(1.02); box-shadow: 0 8px 16px rgba(0,0,0,0.25); }}
    .source-tag {{
        position: absolute;
        top: 10px;
        right: 10px;
        background-color: {'#0D47A1' if not is_dark else '#90caf9'};
        color: {'#ffffff' if not is_dark else '#000000'};
        font-size: 0.75rem;
        padding: 4px 10px;
        border-radius: 8px;
        font-weight: bold;
    }}
    </style>
""", unsafe_allow_html=True)

# App header
st.markdown("""
    <div style="text-align: center;">
        <h1 style="color:#B32020;">BugSense</h1>
        <p style='font-size: 1rem;'>Find similar bug reports from Jira and StackOverflow</p>
        <p style="color:gray;">Paste an error message and get real-world matches instantly.</p>
    </div>
""", unsafe_allow_html=True)

query = st.text_area("", height=150, placeholder="e.g. NullPointerException in Login.java on line 42")

col1, col2 = st.columns([1, 4])
with col1:
    search_clicked = st.button("Find Solutions", use_container_width=True)

with col2:
    st.markdown(f"""
        <div style='display: flex; align-items: center; height: 100%;'>
            <p style='font-size: 0.9rem; color: gray; margin: 0;'>
                BugSense compares your input with Jira and StackOverflow to find close matches.
            </p>
        </div>
    """, unsafe_allow_html=True)

# Processing and results
if search_clicked:
    with st.spinner("Analyzing your error and fetching matches from multiple sources..."):
        jira_posts = fetch_jira_issues(query)
        stack_posts = fetch_stackoverflow_posts(query)

        combined_posts = jira_posts[:5] + stack_posts[:5]

        if not combined_posts:
            st.markdown(f"""
                <div role='alert' style='background-color: {alert_bg_error}; color: {alert_text_error}; padding: 1rem; border-radius: 10px;'>
                    ❌ No similar issues found. Try rephrasing your query.
                </div>
            """, unsafe_allow_html=True)
        else:
            matches = match_posts(query, combined_posts)

            # Sort by score and take top N (not fixed by source)
            matches = sorted(matches, key=lambda x: x['score'], reverse=True)[:6]

            match_word = "match" if len(matches) == 1 else "matches"
            st.markdown(f"""
                <div role='alert' style='background-color: {alert_bg_success}; color: {alert_text_success}; padding: 1rem; border-radius: 10px;'>
                    ✅ Found {len(matches)} similar {match_word}:
                </div>
            """, unsafe_allow_html=True)

            for match in matches:
                st.markdown(f"""
                    <div class='fade-in result-card'>
                        <div class='source-tag'>{match.get('source', 'Unknown')}</div>
                        <h4><a href='{match['link']}' target='_blank'>{match['title']}</a></h4>
                        <p style='color: gray; margin-top: 0.5rem;'>Similarity Score: {match['score']:.2f}</p>
                        <p>{match['preview']}</p>
                    </div>
                """, unsafe_allow_html=True)

# Footer
st.markdown(f"""
    <div style='width: 100%; text-align: center; margin-top: 3rem;'>
        <hr style='margin-bottom: 5px ; width: 100%; border: 1px solid {divider_color};'>
        <p style='text-align: center;'>Built with ❤️ by BugSense | © 2025</p>
    </div>
""", unsafe_allow_html=True)
