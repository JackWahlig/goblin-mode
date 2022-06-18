import argparse
import util
import webscraper

STAKE = 10
ROUND = 0

def parse_args():
    parser = argparse.ArgumentParser(description='Goblin Mode is a WIP sports arbitrage detection app')
    parser.add_argument('--stake', '-s', type=float, default=STAKE, help=f'Total stake to bet with one a single arb (default: {STAKE})')
    parser.add_argument('--round', '-r', type=float, default=ROUND, help=f'Decimal amount bets will be rounded too e.g. 0.25 will make 1.81 round to 1.75 (default: {ROUND})')
    return parser.parse_args()


if __name__ == '__main__':
    leagues = [
        'mlb',
        'nba',
        'nhl',
        'nfl'
    ]

    args = parse_args()
    bet_matrix = webscraper.scrape(leagues, args.stake, args.round)
    util.print_matrix(bet_matrix)