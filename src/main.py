import asyncio
import webscraper

if __name__ == '__main__':
    sportsbooks = [
        'FanDuel'
    ]
    sports = [
        'baseball',
        'basketball',
    ]

    bet_matrix = asyncio.run(webscraper.scrape(sportsbooks, sports))
    print(bet_matrix)