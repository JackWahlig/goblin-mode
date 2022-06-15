import asyncio
import webscraper
import util

if __name__ == '__main__':
    leagues = [
        'mlb',
        'nba'
    ]

    bet_matrix = asyncio.run(webscraper.scrape(leagues))
    util.print_matrix(bet_matrix)