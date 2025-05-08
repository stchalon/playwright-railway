import requests
import re
from bs4 import BeautifulSoup
import json

def extract_text_from_medium(url, cookies=None):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    res = requests.get(url, headers=headers, cookies=cookies or {})
    html = res.text

    # Try __APOLLO_STATE__ first
    match = re.search(r"window\.__APOLLO_STATE__\s*=\s*({.*?});", html)
    if match:
        try:
            data = json.loads(match.group(1))
            paragraphs = []
            for key, value in data.items():
                if isinstance(value, dict) and value.get("__typename") == "Paragraph":
                    text = value.get("text")
                    if text:
                        paragraphs.append(text.strip())
            if paragraphs:
                return "\n\n".join(paragraphs)
        except Exception:
            pass

    # Fallback to <article>
    soup = BeautifulSoup(html, "html.parser")
    article_tag = soup.find("article")
    if not article_tag:
        raise Exception("Could not find <article> tag.")

    text_parts = [tag.get_text(strip=True) for tag in article_tag.find_all(["p", "h1", "h2", "li"])]
    return "\n\n".join(filter(None, text_parts))
