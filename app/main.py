
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from bs4 import BeautifulSoup
import httpx

app = FastAPI()

# Optional: Allow CORS (e.g. from web browser or mobile client)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/shortextract")
async def shortextract(request: Request):
    try:
        data = await request.json()
        url = data.get("url")
        if not url:
            raise HTTPException(status_code=400, detail="Missing 'url' in request")

        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            html = response.text

        soup = BeautifulSoup(html, "html.parser")

        # Find the __APOLLO_STATE__ script tag
        script_tag = soup.find("script", string=lambda text: text and "__APOLLO_STATE__" in text)
        if not script_tag:
            raise HTTPException(status_code=404, detail="Could not find __APOLLO_STATE__ in page")

        # Return a short portion (for now just return the first 1000 characters of raw HTML as a placeholder)
        return {
            "status": "ok",
            "shortextract": html[:1000]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
