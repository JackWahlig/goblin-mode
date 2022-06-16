import webscraper
import util
import arbitrage

if __name__ == '__main__':
    leagues = [
        'mlb',
        'nba',
        'nhl',
        'nfl'
    ]

    bet_matrix = webscraper.scrape(leagues, 25, 0.25)
    util.print_matrix(bet_matrix)