from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
import util

async def scrape(sportsbooks, sports):
    bet_matrix = [['Away', 'Home'].extend(sportsbooks)]
    async with async_playwright() as pw: 
        # Opening page in Chrome
        browser = await pw.chromium.launch(
            headless=True  # Show the browser
        )
        page = await browser.new_page()
        for sportsbook in sportsbooks:
            for sport in sports:
                url = util.sportsbook_url_dict[sportsbook]['base_url'] + util.sportsbook_url_dict[sportsbook][sport]
                await page.goto(url)
                
                # Extracting page elements into betting matrix
                page_content = await page.content()
                soup = BeautifulSoup(page_content,'html.parser')

                AWAY_NAME_INDEX = 0
                HOME_NAME_INDEX = 1

                for match in soup.find_all('div', {'class': util.html_class_dict[sportsbook]['match']}):
                    team_names =  match.find_all('span', {'class': util.html_class_dict[sportsbook][sport + '_team_name']})
                    if len(team_names) == 2:
                        away_name, home_name = team_names
                        found = False
                        for e in bet_matrix[1:]:
                            if away_name == e[AWAY_NAME_INDEX] and home_name == e[HOME_NAME_INDEX]:
                                print("TODO")
                                found = True
                                break
                        if not found:
                            bet_matrix.append([away_name, home_name].extend(['ODDS'] * len(sportsbook) * 2))
        await browser.close()
    return bet_matrix
