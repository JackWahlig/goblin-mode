import asyncio
import webscraper
import util

if __name__ == '__main__':
    leagues = [
        'mlb',
        'nba',
        'nhl',
        'nfl'
    ]

    bet_matrix = asyncio.run(webscraper.scrape(leagues))
    util.output_matrix(bet_matrix)