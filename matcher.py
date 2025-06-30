from sentence_transformers import SentenceTransformer, util
import re


model = SentenceTransformer("all-MiniLM-L6-v2")

def strip_html_and_shorten(text, max_len=200):
    """Remove HTML tags and limit text length."""
    clean_text = re.sub('<[^<]+?>', '', text)
    return clean_text[:max_len] + "..." if len(clean_text) > max_len else clean_text

def match_posts(user_input, stack_posts, threshold=0.3):
   
    user_embed = model.encode(user_input, convert_to_tensor=True)
    texts = [post['title'] + " " + post['body'] for post in stack_posts]
    post_embeds = model.encode(texts, convert_to_tensor=True)

    similarities = util.cos_sim(user_embed, post_embeds)[0]

    results = []
    for idx, score in enumerate(similarities):
        score_float = float(score)

        if score_float >= threshold:
            results.append({
                "title": stack_posts[idx]['title'],
                "link": stack_posts[idx]['link'],
                "score": round(score_float, 3),
                "preview": strip_html_and_shorten(stack_posts[idx]['body'])
            })

    sorted_results = sorted(results, key=lambda x: x["score"], reverse=True)
    return sorted_results[:3] if sorted_results else []
