import requests
import re
from bs4 import BeautifulSoup
import json

def extract_text_from_medium(url):
    res = requests.get(url, headers={
        "User-Agent": "Mozilla/5.0"
    })
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
            pass  # Fall through to BeautifulSoup fallback

    # Fallback to parsing <article> content
    soup = BeautifulSoup(html, "html.parser")
    article_tag = soup.find("article")
    if not article_tag:
        raise Exception("Could not find <article> tag.")

    text_parts = []
    for tag in article_tag.find_all(["p", "h1", "h2", "li"]):
        text = tag.get_text(strip=True)
        if text:
            text_parts.append(text)

    if not text_parts:
        raise Exception("Article appears empty or inaccessible.")

    return "\n\n".join(text_parts)
