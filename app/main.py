
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import httpx
from bs4 import BeautifulSoup
import json

app = FastAPI()

# Function to extract medium article content
async def extract_medium_article(url: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
    
    # Check if request was successful
    if response.status_code != 200:
        return {"error": "Failed to fetch the article."}
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract the __APOLLO_STATE__ JSON
    apollo_state_script = soup.find('script', text=lambda t: '__APOLLO_STATE__' in t)
    
    if not apollo_state_script:
        return {"error": "Couldn't find __APOLLO_STATE__ in the page."}
    
    # Extract JSON from the script
    apollo_state_json = apollo_state_script.string.split('__APOLLO_STATE__=')[-1].split(';</script>')[0]
    try:
        apollo_data = json.loads(apollo_state_json)
    except json.JSONDecodeError:
        return {"error": "Error decoding JSON from __APOLLO_STATE__."}
    
    # Navigate through the data structure to get the article content
    try:
        article_data = apollo_data['ROOT_QUERY']['post({})'.format(url.split('/')[-1])]
        title = article_data['title']
        content = article_data['content']['bodyModel']['paragraphs']
        return {"title": title, "content": content}
    except KeyError:
        return {"error": "Couldn't extract article details from the JSON."}

@app.get("/shortextract")
async def short_extract(url: str):
    article_data = await extract_medium_article(url)
    
    # Return a short extract (first 100 words)
    if "content" in article_data:
        short_content = " ".join(article_data['content'][:100])
        return JSONResponse(content={"title": article_data['title'], "short_content": short_content})
    else:
        return JSONResponse(content=article_data, status_code=400)

@app.get("/fullextract")
async def full_extract(url: str):
    article_data = await extract_medium_article(url)
    
    # Return full content
    if "content" in article_data:
        full_content = " ".join(article_data['content'])
        return JSONResponse(content={"title": article_data['title'], "full_content": full_content})
    else:
        return JSONResponse(content=article_data, status_code=400)
