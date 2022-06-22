from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from time import sleep
from tabulate import tabulate
import argparse
import getpass
import smtplib
import util
import webscraper

STAKE = 10
ROUND = 0
WAIT = 3600

def parse_args():
    parser = argparse.ArgumentParser(description='Goblin Mode is a WIP sports arbitrage detection app')
    parser.add_argument('--stake', '-s', type=float, default=STAKE, help=f'Total stake to bet with one a single arb (default: {STAKE})')
    parser.add_argument('--round', '-r', type=float, default=ROUND, help=f'Decimal amount bets will be rounded too e.g. 0.25 will make 1.81 round to 1.75 (default: {ROUND})')
    parser.add_argument('--wait', '-w', type=int, default=WAIT, help=f'Number of seconds the bot will wait before scraping again to find new arbitrages (default: {WAIT})')
    return parser.parse_args()


if __name__ == '__main__':
    leagues = [
        'mlb',
        'nhl',
        'nfl'
    ]
    
    args = parse_args()
    email = input('Email: ')
    password = getpass.getpass()

    try:
        smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
        smtp_server.starttls()
        smtp_server.login(email, password)
    except smtplib.SMTPAuthenticationError:
        print("The username and/or password you entered were incorrect")
        exit()
    except:
        print("An error occured when trying to connect to the email server")
        exit()

    old_bet_matrix = [['Away', 'Home']]
    while(True):
        bet_matrix = webscraper.scrape(leagues, args.stake, args.round)
        print(old_bet_matrix)
        print(bet_matrix)
        if len(bet_matrix) > 1 and old_bet_matrix != bet_matrix:
            util.matrix_to_txt(bet_matrix)

            html = """<html><body><p>An arbitrage oppotunity has been found: </p>{table}</body></html>""".format(table=tabulate(bet_matrix, headers='firstrow', tablefmt='html'))

            message = MIMEMultipart('alternative', None, [MIMEText(html, 'html')])
            message['Subject'] = 'Goblin Mode Found an Arbitrage'
            message['From'] = email
            message['To'] = email

            smtp_server.send_message(message)
            old_bet_matrix = bet_matrix

        sleep(args.wait)