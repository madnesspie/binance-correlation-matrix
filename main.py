from os import listdir
from itertools import permutations

from pandas import read_csv, concat
from matplotlib import pyplot

from logger import log, get_logger

PATH = 'data/'
CURRENCIES = ['btc', 'eth', 'bnb', 'xrp', 'xlm', 'ada', 'ltc', 'dash', 'xmr', 
              'zec', 'etc', 'neo', 'doge', 'mkr', 'omg', 'zrx', 'dcr', 'qtum']

logger = get_logger(__name__)


def get_tickers(currencies=CURRENCIES):
    return [''.join(pair) for pair in permutations(currencies, 2)]


def filter_tickers(tickers):
    return filter(lambda f: f.replace('.csv', '') in tickers, listdir(PATH))


def to_dataframe(csv):
    df = read_csv(f"{PATH}/{csv}", index_col=0, parse_dates=[['Date', 'Time']])
    df['Ticker'] = csv.replace('.csv', '')
    return df


def resample(df):
    df['Open'] = df.Open.resample('H').first()
    df['High'] = df.High.resample('H').max()
    df['Low'] = df.Low.resample('H').min()
    df['Close'] = df.Close.resample('H').min()
    df['Volume'] = df.Volume.resample('H').sum()
    return df.dropna()


def build_df(tickers):
    dfs = map(to_dataframe, tickers)
    downsampled_dfs = map(resample, dfs)
    return concat(downsampled_dfs)

    # if 'adabnb.csv' != ticker:
    #     continue
    # print(downsampled)
    # df.plot()
    # pyplot.show()
    # break


def main():
    tickers = filter_tickers(get_tickers())
    df = build_df(tickers)
    print(df)
    
if __name__ == '__main__':
    main()

# class ParseTickers:
#     def __init__(self):
#         pass 
