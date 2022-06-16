from datetime import datetime
import pytz
import smtplib

url_dict = {
    'base_url': 'https://www.oddschecker.com/us/',
    'mlb':      'baseball/mlb',
    'nba':      'basketball/nba',
    'ncaab':    'basketball/ncaab',
    'ncaaf':    'football/college-football',
    'nfl':      'football/nfl',
    'nhl':      'hockey/nhl',
    'tennis':   'tennis'
}

sportsbook_dict = {
    'F5': 'BetMGM',
    'EG': 'BetRivers',
    'K2': 'Caesars',
    'D6': 'DraftKings',
    'U1': 'FanDuel',
    'ZY': 'PointsBet',
    'UV': 'UniBet',
}

def format_odds(odds):
    if int(odds) > 0:
        return '+' + odds
    else:
        return odds

def format_date(dt):
    date, time = dt.split('T')
    year, month, day = date.split('-')
    hour, min = time[:-4].split(':')
    d = datetime(int(year), int(month), int(day), int(hour), int(min))
    
    ct = pytz.timezone('America/Chicago')
    utc = pytz.utc
    
    utc_time = utc.localize(d)
    ct_time = utc_time.astimezone(ct)
    now = datetime.now(ct)

    # Return formatted time and whether the game is live
    return (ct_time.strftime('%Y-%m-%d, %I:%M %p'), now > ct_time)

def is_arbitrage(odds_1, odds_2):
    if odds_1 > 0:
        if odds_2 > 0 or -odds_2 < odds_1:
            return True
    elif odds_2 > 0 and -odds_1 < odds_2:
        return True
    return False

def arbitrage_calc(stake, odds_1, odds_2, rnd=0):
    payout_1, payout_2 = payout(odds_1), payout(odds_2)
    bet_1 = round((stake * payout_2) / (payout_1 + payout_2), 2)
    if rnd:
        bet_1 = rnd * round(bet_1 / rnd)
    bet_2 = round(stake - bet_1, 2)     # Round to avoid floating point error
    return (bet_1, round(bet_1 * payout_1, 2), bet_2, round(bet_2 * payout_2, 2))

def payout(odds):
    if int(odds) > 0:
        return (int(odds) / 100) + 1
    else:
        return (100 / -int(odds)) + 1

def print_matrix(matrix):
    matrix.insert(0, ['Away', 'Home'])
    # Pad Matrix
    max_len = max(map(len, matrix))
    for row in matrix:
        row.extend([''] * (max_len - len(row)))

    lens = [max(map(len, col)) for col in zip(*matrix)]
    fmt = '\t'.join(f'| {{:{x}}} |' for x in lens)
    matrix.insert(1, ['-' * len for len in lens])
    table = [fmt.format(*row) for row in matrix]
    f = open('output.txt', 'w')
    f.write('\n'.join(table))
    f.close()
    #print('\n'.join(table))