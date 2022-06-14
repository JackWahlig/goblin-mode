from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
import asyncio

async def scrape(url):
    async with async_playwright() as pw: 
        # Opening page in Chrome
        browser = await pw.chromium.launch(
            headless=True  # Show the browser
        )
        page = await browser.new_page()
        await page.goto(url)
        
        # Extracting page elements
        page_content = await page.content()
        soup = BeautifulSoup(page_content,'html.parser')

        for match in soup.find_all('div', {'class': 'ho x h'}):
            for team_name in match.find_all('span', {'class': 's x ig ih ii ij hq hr hs hw ik h fl dj il bb'}):
                print(team_name.text)

        await browser.close()

if __name__ == '__main__':
    asyncio.run(scrape('https://sportsbook.fanduel.com/baseball'))
