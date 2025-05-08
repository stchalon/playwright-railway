# Trigger redeploy
from fastapi import FastAPI, Query
from playwright.async_api import async_playwright
import uvicorn
import asyncio

app = FastAPI()

@app.get("/screenshot")
async def screenshot(url: str = Query(..., description="URL to capture")):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url)
        await page.screenshot(path="screenshot.png")
        await browser.close()
    return {"status": "screenshot taken"}

@app.get("/extract")
async def extract_text(url: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(url)

        # Try to extract the article text from <article>
        article = await page.eval_on_selector("article", "el => el.innerText")
        await browser.close()

        return {"text": article or "No article content found"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000)