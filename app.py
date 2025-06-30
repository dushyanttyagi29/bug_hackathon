import streamlit as st
from jira_api import fetch_jira_issues
from matcher import match_posts

st.set_page_config(page_title="BugMatch - Jira AI", layout="centered")
st.title("BugSense: AI-Powered Jira Bug Matcher")

query = st.text_area("🐞 Paste your bug/error message here:")

if st.button("🔎 Find Similar Jira Issues"):
    with st.spinner("Thinking..."):
        jira_issues = fetch_jira_issues(query)

        if not jira_issues:
            st.warning("❌ No results found from Jira. Try rephrasing the error.")
        else:
            st.info(f"🐞 Jira returned {len(jira_issues)} issues.")

            for i, issue in enumerate(jira_issues[:3]):
                st.markdown(f"**Issue {i+1}: [{issue['title']}]({issue['link']})**")
                
                # Fix: safely convert description to string
                raw_desc = issue.get('description', '')
                desc_str = str(raw_desc)
                short_desc = desc_str.replace("\n", " ")
                
                st.caption(short_desc[:200] + "..." if len(short_desc) > 200 else short_desc)

            matches = match_posts(query, jira_issues)

            st.write("🧠 Match Titles:", [m['title'] for m in matches] if matches else "None")

            if matches:
                st.success(f"✅ Found {len(matches)} similar issues:")
                for match in matches:
                    st.markdown(f"**🔗 [{match['title']}]({match['link']})**")
                    st.caption(f"Similarity Score: `{match['score']:.2f}`")
            else:
                st.error("❌ No similar resolved Jira issues found. Try changing the wording or details.")
