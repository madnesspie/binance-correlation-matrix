from os import listdir
from os.path import basename, splitext
from itertools import permutations
from multiprocessing import Pool

from pandas import DataFrame, read_csv, concat
from matplotlib import pyplot as plt

# from logger import log, get_logger
# logger = get_logger(__name__)

PATH = 'data/csv/'
CURRENCIES = ['btc', 'eth', 'bnb', 'xrp', 'xlm', 'ada', 'ltc', 'dash', 'xmr', 
              'zec', 'etc', 'neo', 'doge', 'mkr', 'omg', 'zrx', 'dcr', 'qtum']



def get_tickers(currencies=CURRENCIES):
    return [''.join(pair) for pair in permutations(currencies, 2)]


def tickername(file):
    return splitext(basename(file))[0]


def filter_tickers(tickers):
    return filter(lambda file: tickername(file) in tickers, listdir(PATH))


def downsample(dataframe):
    ticker = dataframe.columns[-1]
    dataframe[ticker] = dataframe[ticker].resample('H').min()
    return dataframe.dropna()


def pluck_ticker_dataframe(csv):
    dataframe = read_csv(
        f"{PATH}/{csv}", index_col=0, usecols=['Date', 'Time', 'Close'],
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


df = to_dataframe('adabnb.csv')
save_hdf(df)


def build_dataframe(tickers):
    # TODO: remove [:2]
    dfs = map(to_dataframe, list(tickers))
    downsampled_dfs = map(downsample, dfs)
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


# def wrest_two(df):
#     pass


# def build_plots(df):
#     for part in wrest_two(df):
#         plot_corr(df)
#     pass


# def main():
#     tickers = get_tickers()
#     filtred = filter_tickers(tickers)
    
#     df = build_dataframe(filtred)
#     print(df)

#     plot_corr(df)
#     # corr = df.corr()
#     # plt.matshow(corr)
#     plt.show()
    
#     # if 'adabnb.csv' != ticker:
#     #     continue
#     # df.plot()


# if __name__ == '__main__':
#     main()
