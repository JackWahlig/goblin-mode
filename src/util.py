url_dict = {
    'base_url': 'https://www.oddschecker.com/us/',
    'mlb':      'baseball/mlb',
    'nba':      'basketball/nba',
    'ncaab':    'basketball/ncaab',
    'ncaaf':    'football/college-football',
    'nfl':      'football/nfl',
    'nhl':      'hockey/nhl',
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
    from datetime import datetime
    import pytz

    date, time = dt.split('T')
    year, month, day = date.split('-')
    hour, min = time[:-4].split(':')
    d = datetime(int(year), int(month), int(day), int(hour), int(min))

    ct = pytz.timezone('America/Chicago')
    utc = pytz.utc
    
    utc_time = utc.localize(d)
    ct_time = utc_time.astimezone(ct)
    
    return ct_time.strftime('%Y-%m-%d, %I:%M %p')

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