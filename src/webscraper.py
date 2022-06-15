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

    bet_matrix = [['Away', 'Home', 'Best Away Odds', 'Best Home Odds', 'Time of Game']]
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
                away_name = match[AWAY_TEAM][FULL_NAME]
                home_name = match[HOME_TEAM][FULL_NAME]
                for all_bets in match[MARKETS]:
                    for bet in all_bets[BETS]:
                        if bet[NAME] == away_name:
                            away_odds = util.format_odds(bet[BEST_ODDS])
                            away_sb = util.sportsbook_dict[bet[BEST_SB][:2]]
                        elif bet[NAME] == home_name:
                            home_odds = util.format_odds(bet[BEST_ODDS])
                            home_sb = util.sportsbook_dict[bet[BEST_SB][:2]]
                
                bet_matrix.append([away_name, home_name, away_sb + ' : ' + away_odds, home_sb + ' : ' + home_odds, date])


    return bet_matrix
