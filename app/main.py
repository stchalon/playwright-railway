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
        await page.goto(url, timeout=60000)  # Allow longer load time
        await page.wait_for_load_state("networkidle")

        text = None

        # Try <article> first
        try:
            await page.wait_for_selector("article", timeout=5000)
            text = await page.eval_on_selector("article", "el => el.innerText")
        except:
            # Try a fallback (e.g. div with data-test or role)
            try:
                await page.wait_for_selector("main", timeout=5000)
                text = await page.eval_on_selector("main", "el => el.innerText")
            except:
                text = "Failed to extract article content."

        await browser.close()
        return {"text": text}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000)