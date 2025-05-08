import requests
import re
from bs4 import BeautifulSoup
import json

def extract_text_from_medium(url):
    res = requests.get(url)
    html = res.text

    # Medium embeds structured data in __APOLLO_STATE__
    match = re.search(r"window\.__APOLLO_STATE__\s*=\s*({.*?});", html)
    if not match:
        raise Exception("Could not locate embedded article data.")

    data = json.loads(match.group(1))

    # Get paragraphs
    paragraphs = []
    for key, value in data.items():
        if isinstance(value, dict) and value.get("__typename") == "Paragraph":
            text = value.get("text")
            if text:
                paragraphs.append(text.strip())

    return "\n\n".join(paragraphs)
