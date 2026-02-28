import asyncio
from playwright.async_api import async_playwright
import re

async def main():
    total_sum = 0
    seeds = range(16, 26)  # Seeds 16 through 25
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        for seed in seeds:
            url = f"https://sanand0.github.io/tdsdata/js_table/?seed={seed}"
            await page.goto(url, wait_until="networkidle")
            
            # Extract all numbers from <td> elements
            cells = await page.locator("td").all_inner_texts()
            for cell in cells:
                clean_val = re.sub(r'[^\d\.-]', '', cell.strip())
                if clean_val and clean_val not in [".", "-"]:
                    try:
                        total_sum += float(clean_val)
                    except ValueError:
                        continue
        
        await browser.close()
    
    print(f"TOTAL_SUM_RESULT: {total_sum}")

if __name__ == "__main__":
    asyncio.run(main())
