from os import listdir
from itertools import permutations

# import pandas

PATH = 'data/'
CURRENCIES = ['btc', 'eth', 'bnb', 'xrp', 'xlm', 'ada', 'ltc', 'dash', 'xmr', 
              'zec', 'etc', 'neo', 'doge', 'mkr', 'omg', 'zrx', 'dcr', 'qtum']


def get_tickers(currencies=CURRENCIES):
    return tuple(map(lambda p: ''.join(p), permutations(currencies, 2)))


def get_filenames(path=PATH):
    return tuple(map(lambda f: f.replace('.csv', ''), listdir(path)))


def filter_tickers(tickers, filenames):
    tickers = get_tickers()
    filenames = get_filenames()
    return sorted(filter(lambda f: f in tickers, filenames))


# class ParseTickers:
#     def __init__(self):
#         pass 
