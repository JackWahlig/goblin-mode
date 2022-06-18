from bs4 import BeautifulSoup
from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import json
import logging
import os
import util

def scrape(leagues, stake, rnd):
    BASE_URL = 'base_url'
    CARD = 'card'
    CARDS = 'cards'
    MATCHES = 'matches'
    ID = 'id'
    ID_CLASS = 'initial-data'
    DATE = 'date'
    DATA = 'data'
    AWAY_TEAM = 'awayTeam'
    HOME_TEAM = 'homeTeam'
    FULL_NAME = 'fullName'
    MARKETS = 'marketsForNewCard'
    BETS = 'bets'
    NAME = 'name'
    BEST_ODDS = 'bestOddsUs'
    BEST_SB = 'bestOddsBookmakers'
    BET_NAME_LEN = 25
    SP_NAME_LEN = 15
    ADVICE_LEN_1 = 20
    ADVICE_LEN_2 = 20
    ODDS_LEN = 7
    DEFAUL_ENTRY_LEN = 3

    bet_matrix = []
    for league in leagues:
        # Setup webpage scraper
        url = util.url_dict[BASE_URL] + util.url_dict[league]

        options = Options()
        options.add_argument('--headless')
        options.add_experimental_option('excludeSwitches', ['enable-automation', 'enable-logging'])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument('--disable-blink-features=AutomationControlled')
        logging.getLogger('WDM').setLevel(logging.NOTSET)
        os.environ['WDM_LOG'] = 'false'
        driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options)


        stealth(driver,
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True,
        )

        # Extract JSON from page and write to temp file
        driver.get(url)
        soup = BeautifulSoup(driver.page_source,'html.parser')
        data = json.loads(soup.find('script', {ID: ID_CLASS}).text)
        with open('./output/data.json', 'w') as f:
            json.dump(data, f)

        driver.quit()

        # Extract betting info from JSON
        matches = data[CARD][MATCHES]
        for match_set in matches:
            date, live = util.format_date(match_set[DATE])
            if not live:        # Do not consider live games; avoids clutter
                for match in match_set[CARDS][0][DATA]:
                    matrix_entry = [match[AWAY_TEAM][FULL_NAME], match[HOME_TEAM][FULL_NAME], date]
                    for bets in (b for b in match[MARKETS] if len(b[BETS]) == 2):
                        bet_1, bet_2 = bets[BETS][0], bets[BETS][1]
                        if bet_1[BEST_SB] != bet_2[BEST_SB] and util.is_arbitrage(int(bet_1[BEST_ODDS]), int(bet_2[BEST_ODDS])):
                            wager_1, win_1, wager_2, win_2 = util.arbitrage_calc(stake, bet_1[BEST_ODDS], bet_2[BEST_ODDS], rnd)
                            matrix_entry.append(f"{bet_1[NAME]:<{BET_NAME_LEN}} {' - ' + util.sportsbook_dict[bet_1[BEST_SB][:2]]:<{SP_NAME_LEN}} {' : ' + util.format_odds(bet_1[BEST_ODDS]):<{ODDS_LEN}}")
                            matrix_entry.append(f"{bet_2[NAME]:<{BET_NAME_LEN}} {' - ' + util.sportsbook_dict[bet_2[BEST_SB][:2]]:<{SP_NAME_LEN}} {' : ' + util.format_odds(bet_2[BEST_ODDS]):<{ODDS_LEN}}")
                            advice_1 = 'Bet ' + str(wager_1) + '/' + str(wager_2)
                            advice_2 = 'to win ' + str(win_1) + '/' + str(win_2)
                            matrix_entry.append(f"{advice_1:<{ADVICE_LEN_1}}{advice_2:<{ADVICE_LEN_2}}")

                    if len(matrix_entry) > DEFAUL_ENTRY_LEN:
                        bet_matrix.append(matrix_entry)

    return bet_matrix