from bs4 import BeautifulSoup
import cloudscraper
import json
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
        # Scrape webpage
        scraper = cloudscraper.create_scraper()
        url = util.url_dict[BASE_URL] + util.url_dict[league]
        page_content = scraper.get(url)

        # Extract JSON from page
        soup = BeautifulSoup(page_content.text,'html.parser')
        data = json.loads(soup.find('script', {ID: ID_CLASS}).text)
        with open('test.json', 'w') as f:
            json.dump(data, f)

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
                            matrix_entry.append(f"{bet_1['name']:<{BET_NAME_LEN}} {' - ' + util.sportsbook_dict[bet_1[BEST_SB][:2]]:<{SP_NAME_LEN}} {' : ' + util.format_odds(bet_1[BEST_ODDS]):<{ODDS_LEN}}")
                            matrix_entry.append(f"{bet_2['name']:<{BET_NAME_LEN}} {' - ' + util.sportsbook_dict[bet_2[BEST_SB][:2]]:<{SP_NAME_LEN}} {' : ' + util.format_odds(bet_2[BEST_ODDS]):<{ODDS_LEN}}")
                            advice_1 = 'Bet ' + str(wager_1) + '/' + str(wager_2)
                            advice_2 = 'to win ' + str(round(win_1 - wager_1 - wager_2, 2)) + '/' + str(round(win_2 - wager_1 - wager_2, 2))
                            matrix_entry.append(f"{advice_1:<{ADVICE_LEN_1}}{advice_2:<{ADVICE_LEN_2}}")

                    if len(matrix_entry) > DEFAUL_ENTRY_LEN:
                        bet_matrix.append(matrix_entry)

    return bet_matrix