from fastapi import FastAPI, Query
from playwright.async_api import async_playwright
import uvicorn

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

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000)