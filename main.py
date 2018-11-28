from os import listdir
from itertools import permutations

from pandas import read_csv, concat
from matplotlib import pyplot as plt

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
    df = read_csv(
        f"{PATH}/{csv}", index_col=0, 
        usecols=['Date', 'Time', 'Close'], parse_dates=[['Date', 'Time']])
    df['Ticker'] = csv.replace('.csv', '')
    return df


def resample(df):
    # df['Open'] = df.Open.resample('H').first()
    # df['High'] = df.High.resample('H').max()
    # df['Low'] = df.Low.resample('H').min()
    # df['Volume'] = df.Volume.resample('H').sum()
    df['Close'] = df.Close.resample('H').min()
    return df.dropna()


def build_df(tickers):
    # TODO: remove [:2]
    dfs = map(to_dataframe, list(tickers)[:2])
    downsampled_dfs = map(resample, dfs)
    return concat(downsampled_dfs)


def plot_corr(df, size=10):
    '''Function plots a graphical correlation matrix for each pair of columns in the dataframe.

    Input:
        df: pandas DataFrame
        size: vertical and horizontal size of the plot'''

    corr = df.corr()
    fig, ax = plt.subplots(figsize=(size, size))
    ax.matshow(corr)
    plt.xticks(range(len(corr.columns)), corr.columns)
    plt.yticks(range(len(corr.columns)), corr.columns)


def main():
    tickers = filter_tickers(get_tickers())
    df = build_df(tickers)
    print(df)

    plot_corr(df)
    
    # corr = df.corr()
    # plt.matshow(corr)
    plt.show()
    
    # if 'adabnb.csv' != ticker:
    #     continue
    # df.plot()


if __name__ == '__main__':
    main()

# class ParseTickers:
#     def __init__(self):
#         pass 
