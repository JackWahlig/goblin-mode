from operator import truediv


def is_arbitrage(odd_1, odd_2):
    if odd_1 > 0:
        if odd_2 > 0 or -odd_2 < odd_1:
            return True
    elif odd_2 > 0 and -odd_1 < odd_2:
        return True
    return False