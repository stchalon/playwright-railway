# Force update
#
from fastapi import FastAPI, Query, Request
from pydantic import BaseModel
from playwright.async_api import async_playwright
import asyncio
import logging

app = FastAPI()

class URLRequest(BaseModel):
    url: str

@app.get("/screenshot")
async def screenshot(url: str = Query(..., description="URL to capture")):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(url)
        await page.screenshot(path="screenshot.png", full_page=True)
        await browser.close()
        return {"status": "screenshot taken"}

@app.get("/shortextract")
async def extract(request: URLRequest):
    #url = request.query_params.get("url")
    url = request.url
    if not url:
        return {"error": "URL parameter is missing"}

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()
            await page.goto(url)
            content = await page.content()
            await browser.close()
            return {"content": content}
    except Exception as e:
        logging.error(f"Error in /extract endpoint: {e}")
        return {"error": str(e)}

#@app.get("/fullextract")
#async def extract_text(url: str = Query(..., description="Medium URL to extract")):
#    async with async_playwright() as p:
#        browser = await p.chromium.launch()
#        page = await browser.new_page()
#        await page.goto(url, timeout=60000)
#        await page.wait_for_load_state("networkidle")
#
#        text = None
#
#        # Try article
#        try:
#            await page.wait_for_selector("article", timeout=10000)
#            text = await page.eval_on_selector("article", "el => el.innerText")
#        except:
#            # Try main as fallback
#            try:
#                await page.wait_for_selector("main", timeout=10000)
#                text = await page.eval_on_selector("main", "el => el.innerText")
#            except:
#                text = "Failed to extract article content."
#
#        await browser.close()
#        return {"text": text}
