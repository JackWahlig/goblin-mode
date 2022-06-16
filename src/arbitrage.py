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