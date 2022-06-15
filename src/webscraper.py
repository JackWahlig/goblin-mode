from bs4 import BeautifulSoup
import cloudscraper
import json
import util

async def scrape(leagues):
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
    ODDS_LEN = 7

    bet_matrix = []
    for league in leagues:
        # Scrape webpage
        scraper = cloudscraper.create_scraper()
        url = util.url_dict[BASE_URL] + util.url_dict[league]
        page_content = scraper.get(url)

        # Extract JSON from page
        soup = BeautifulSoup(page_content.text,'html.parser')
        data = json.loads(soup.find('script', {ID: ID_CLASS}).text)
        matches = data[CARD][MATCHES]

        with open('test.json', 'w') as f:
            json.dump(matches, f)

        for match_set in matches:
            date = util.format_date(match_set[DATE])
            for match in match_set[CARDS][0][DATA]:
                matrix_entry = [match[AWAY_TEAM][FULL_NAME], match[HOME_TEAM][FULL_NAME], date]
                for all_bets in match[MARKETS]:
                    for bet in all_bets[BETS]:
                        matrix_entry.append(f"{bet['name']:<{BET_NAME_LEN}} {' - ' + util.sportsbook_dict[bet[BEST_SB][:2]]:<{SP_NAME_LEN}} {' : ' + util.format_odds(bet[BEST_ODDS]):<{ODDS_LEN}}")
                        
                bet_matrix.append(matrix_entry)


    return bet_matrix
