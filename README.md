# Goblin-Mode
A sports betting arbitrage app (made for fun and to learn more about webscraping, use at your own risk)

This app works by scraping oddschecker.com/us for the best odds of upcoming matches and searching for arbitrage opportunities (https://en.wikipedia.org/wiki/Arbitrage_betting). For each arbitrage, the app will calculate how much to bet on each side and the guaranteed returned profit given the odds and a target stake. It can round these bets to any nearest value (e.g. nearest ten dollars, dollar, 50 cents, 10 cents, etc.) to simplify the amounts to bet. 

This app is still a WIP and is intended to include more sports and send email notifications. 

## Requirements
[cloudscraper](https://pypi.org/project/cloudscraper/)

[pytz](https://pypi.org/project/pytz/)

# Command line usage
You can run the app with command `python src/main.py`

Argument `--stake <float>` or `-s <float>` lets you set the total stake you wish to put on each arbitrage. Default = $10

Argument `--round <float>` or `-r <float>` lets you set the decimal value to round each bet to e.g. `-r 0.25` will round each bet to the nearest $0.25, so $3.21 would be rounded up to $3.25 while $6.59 would be rounded down to $6.50. Default = $0.00

More arguements will be added as features are added.
