import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        # Desktop Dark
        page = await browser.new_page(viewport={"width": 1600, "height": 817}, color_scheme="dark")
        await page.goto("http://127.0.0.1:7860")
        await page.wait_for_selector("button:has-text('Chạy demo')")
        
        # Click start demo
        await page.click("button:has-text('Chạy demo')")
        print("Clicked Chạy demo")
        
        # Wait 4s (mid-run)
        await asyncio.sleep(4.0)
        await page.screenshot(path=r"E:\VoiceAI\demo_running_dark.png")
        print("Captured running screenshot")
        
        # Wait until complete (7s more)
        await asyncio.sleep(7.0)
        await page.screenshot(path=r"E:\VoiceAI\demo_complete_dark.png")
        print("Captured complete screenshot")
        
        # Click rerun
        await page.click("button:has-text('Chạy lại')")
        print("Clicked Chạy lại")
        await asyncio.sleep(2.0)
        await page.screenshot(path=r"E:\VoiceAI\demo_rerun_dark.png")
        print("Captured rerun screenshot")
        
        await browser.close()

asyncio.run(run())
