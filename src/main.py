import webscraper
import util

if __name__ == '__main__':
    leagues = [
        'mlb',
        'nba',
        'nhl',
        'nfl'
    ]

    bet_matrix = webscraper.scrape(leagues)
    util.print_matrix(bet_matrix)