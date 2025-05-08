from fastapi import FastAPI, Query
from playwright.async_api import async_playwright
import asyncio

app = FastAPI()

@app.get("/screenshot")
async def screenshot(url: str = Query(..., description="URL to capture")):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(url)
        await page.screenshot(path="screenshot.png", full_page=True)
        await browser.close()
        return {"status": "screenshot taken"}

@app.get("/extract")
async def extract_text(url: str = Query(..., description="Medium URL to extract")):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(url, timeout=60000)
        await page.wait_for_load_state("networkidle")

        text = None

        # Try article
        try:
            await page.wait_for_selector("article", timeout=10000)
            text = await page.eval_on_selector("article", "el => el.innerText")
        except:
            # Try main as fallback
            try:
                await page.wait_for_selector("main", timeout=10000)
                text = await page.eval_on_selector("main", "el => el.innerText")
            except:
                text = "Failed to extract article content."

        await browser.close()
        return {"text": text}