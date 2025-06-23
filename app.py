import streamlit as st
from stack_api import fetch_stackoverflow_results
from matcher import match_posts

st.set_page_config(page_title="StackSmart", layout="centered")
st.title("BugSense: AI-Powered Bug Search & Explanation")

query = st.text_area("🔍 Paste your bug/error message here:")

if st.button("🔎 Find Similar Solutions"):
    with st.spinner("Thinking..."):
        so_posts = fetch_stackoverflow_results(query)

       
        st.info(f"🔍 StackOverflow returned {len(so_posts)} posts.")

        
        for i, post in enumerate(so_posts[:3]):
            st.markdown(f"**Post {i+1}: [{post['title']}]({post['link']})**")
            short_body = post['body'].replace("<p>", "").replace("</p>", "").replace("<code>", "`").replace("</code>", "`")
            st.caption(short_body[:200] + "..." if len(short_body) > 200 else short_body)

        if not so_posts:
            st.warning("❌ No results found from Stack Overflow. Try rephrasing the error.")
        else:
            matches = match_posts(query, so_posts)

           
            st.write("🧠 Match Titles:", [m['title'] for m in matches] if matches else "None")

            if matches:
                st.success(f"✅ Found {len(matches)} similar questions:")
                for match in matches:
                    st.markdown(f"**🔗 [{match['title']}]({match['link']})**")
                    st.caption(f"Similarity Score: `{match['score']:.2f}`")
            else:
                st.error("❌ No similar resolved issues found. Try changing the wording or details.")
