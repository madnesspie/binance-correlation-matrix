from os import listdir, remove
from os.path import basename, splitext
from glob import glob
from itertools import permutations
from multiprocessing import Pool

from pandas import read_csv

# Валюты, которые нас интересуют 
CURRENCIES = ['btc', 'eth', 'bnb', 'xrp', 'xlm', 'ada', 'ltc', 'dash', 'xmr',
              'zec', 'etc', 'neo', 'doge', 'mkr', 'omg', 'zrx', 'dcr', 'qtum']


def get_ticker_names(currencies=CURRENCIES):
    return [''.join(pair) for pair in permutations(currencies, 2)]


def get_csv_files(tickers):
    return filter(lambda file: tickername(file) in tickers, 
                  listdir('data/csv/'))


def tickername(file):
    return splitext(basename(file))[0]


def pluck_ticker_dataframe(csv):
    dataframe = read_csv(
        f"data/csv/{csv}", index_col=0, usecols=['Date', 'Time', 'Close'],
        parse_dates=[['Date', 'Time']])
    return dataframe['Close']


def to_dataframe(csv):
    dataframe = pluck_ticker_dataframe(csv)
    dataframe.name = tickername(csv)
    return dataframe


def save_hdf(dataframe):
    ticker = dataframe.name
    dataframe.to_hdf(
        f"data/hdf/{ticker}.hdf", key=ticker, mode='w', complib='zlib')


def convert(csv):
    dataframe = to_dataframe(csv)
    save_hdf(dataframe)


def clean(path):
    files = [f"{path}{f}" for f in listdir(path)]
    list(map(remove, files))


def run():
    clean('data/hdf/')
    ticker_names = get_ticker_names()
    csv_files = get_csv_files(ticker_names)
    Pool().map(convert, csv_files)


if __name__ == '__main__':
    run()
