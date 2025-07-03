from sentence_transformers import SentenceTransformer, util
import re

model = SentenceTransformer("all-MiniLM-L6-v2")

def strip_html_and_shorten(text, max_len=200):
    clean_text = re.sub('<[^<]+?>', '', text)
    return clean_text[:max_len] + "..." if len(clean_text) > max_len else clean_text

# def match_posts(user_input, posts, top_k=3):
#     """Return top-k similar posts for the user input."""
#     user_embed = model.encode("query: " + user_input, convert_to_tensor=True)

#     texts = ["passage: " + (post['title'] + " " + post['description']) for post in posts]
#     post_embeds = model.encode(texts, convert_to_tensor=True)

#     similarities = util.cos_sim(user_embed, post_embeds)[0]

#     scored_posts = [
#         (posts[i], float(similarities[i]))
#         for i in range(len(posts))
#     ]
#     scored_posts.sort(key=lambda x: x[1], reverse=True)

#     results = []
#     for post, score in scored_posts[:top_k]:
#         results.append({
#             "title": post['title'],
#             "link": post['link'],
#             "score": round(score, 3),
#             "preview": strip_html_and_shorten(post['description']),
#             "source": post.get("source", "Unknown")  # ✅ Fix here
#         })

#     return results




def match_posts(user_input, posts, top_k=3):
    """Return top-k similar posts for the user input."""
    user_embed = model.encode("query: " + user_input, convert_to_tensor=True)

    texts = ["passage: " + (post['title'] + " " + post['description']) for post in posts]
    post_embeds = model.encode(texts, convert_to_tensor=True)

    similarities = util.cos_sim(user_embed, post_embeds)[0]

    scored_posts = [
        (posts[i], float(similarities[i]))
        for i in range(len(posts))
    ]
    scored_posts.sort(key=lambda x: x[1], reverse=True)

    results = []
    for post, score in scored_posts[:top_k]:
        results.append({
            "title": post['title'],
            "link": post['link'],
            "score": round(score, 3),
            "preview": strip_html_and_shorten(post['description']),
            "source": post.get('source', 'Unknown')  # Safely include source
        })

    return results
