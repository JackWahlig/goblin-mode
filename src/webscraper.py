from bs4 import BeautifulSoup
import arbitrage
import cloudscraper
import json
import util

def scrape(leagues):
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
    DEFAUL_ENTRY_LEN = 3

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

        # Extract betting info from JSON
        for match_set in matches:
            date = util.format_date(match_set[DATE])
            for match in match_set[CARDS][0][DATA]:
                matrix_entry = [match[AWAY_TEAM][FULL_NAME], match[HOME_TEAM][FULL_NAME], date]
                for bets in (b for b in match[MARKETS] if len(b[BETS]) == 2):
                    bet1 = bets[BETS][0]
                    bet2 = bets[BETS][1]
                    if arbitrage.is_arbitrage(int(bet1[BEST_ODDS]), int(bet2[BEST_ODDS])):
                        matrix_entry.append(f"{bet1['name']:<{BET_NAME_LEN}} {' - ' + util.sportsbook_dict[bet1[BEST_SB][:2]]:<{SP_NAME_LEN}} {' : ' + util.format_odds(bet1[BEST_ODDS]):<{ODDS_LEN}}")
                        matrix_entry.append(f"{bet2['name']:<{BET_NAME_LEN}} {' - ' + util.sportsbook_dict[bet2[BEST_SB][:2]]:<{SP_NAME_LEN}} {' : ' + util.format_odds(bet2[BEST_ODDS]):<{ODDS_LEN}}")
                        
                if len(matrix_entry) > DEFAUL_ENTRY_LEN:
                    bet_matrix.append(matrix_entry)

    return bet_matrix
