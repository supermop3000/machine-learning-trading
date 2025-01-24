import datetime as dt
import os
import numpy as np
import pandas as pd
from util import get_data, plot_data
from pprint import pprint as pp
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters

def author():
    return 'ccortvriendt3'

def generate_indicators(symbol='AAPL', sd = dt.datetime(2010, 1,1), ed=dt.datetime(2011,12,13)):
    symbol_list = [symbol]

    df_prices = get_data(symbol_list, pd.date_range(sd, ed), addSPY=False)
    mid_date = dt.datetime(2009, 1, 1)

    #normalize prices
    # df_prices.ffill(inplace=True)
    # df_prices.bfill(inplace=True)
    df_prices.dropna(axis=0, how='any', inplace=True)
    df_prices = df_prices/df_prices.ix[0,:]



    # calculate simple moving average
    df_sma = calc_SMA(df_prices, mid_date)
    df_bb_percent = calc_bollinger_bands(df_prices, mid_date)
    df_momentum = calc_momentum(df_prices, mid_date)
    df_cmf = calc_CMF(df_prices, symbol_list, sd, ed, mid_date)
    df_ema_short, df_ema_long = calc_EMA(df_prices, mid_date)

    return df_sma, df_momentum, df_cmf


def calc_SMA(df_prices, mid_date):
    df_sma = df_prices.copy()
    df_sma = df_sma.rolling(window=20).mean()
    df_sma_price = df_prices/df_sma -1

    fig = plt.figure(num=0, figsize = (8, 6))
    fig.suptitle("JPM Simple Moving Average (SMA)", fontsize=14)
    ax01 = plt.subplot2grid((8, 6), (0, 0), colspan=6, rowspan=4)
    ax02 = plt.subplot2grid((8, 6), (5, 0), colspan=6, rowspan=4)
    ax01.plot(df_sma, label='JPM SMA', color='slateblue')
    ax01.plot(df_prices, label='JPM Price', color='lightpink')
    ax01.set_xlabel("Date")
    ax01.set_xlim(df_sma.index.min(), df_sma.index.max())
    ax01.set_ylabel("Normalized Price")
    ax01.grid()
    ax01.text(mid_date, .8, 'Chad Cortvriendt', fontsize=40, color='gray', alpha=0.5,
        ha='center', va='center', rotation='20')
    ax01.legend()
    ax01.set_title('JPM SMA')

    ax02.plot(df_sma_price, label="JPM Price/SMA", color='olivedrab')
    ax02.set_title('JPM Price/SMA')
    ax02.set_xlabel('Date')
    ax02.set_xlim(df_prices.index.min(), df_prices.index.max())
    ax02.legend()
    ax02.grid()
    ax02.set_ylabel('Price/SMA Ratio')
    ax02.text(mid_date, 0, 'Chad Cortvriendt', fontsize=40, color='gray', alpha=0.5,
        ha='center', va='center', rotation='20')

    # plt.savefig("figure_sma.png")
    plt.clf()

    return df_sma_price

def calc_bollinger_bands(df_prices, mid_date):
    #bb_value[t] = (price[t] - SMA[t])/(2 * stdev[t])
    # 20 day simple moving average
    df_sma = df_prices.rolling(window=20).mean()

    #https://school.stockcharts.com/doku.php?id=technical_indicators:bollinger_bands
    # 20 day standard deviation
    df_std = df_prices.rolling(window=20).std()

    # calc upper band
    df_bb_upper = df_sma + (2 * df_std)

    # calc lower band
    df_bb_lower = df_sma - (2 * df_std)

    #https: // school.stockcharts.com / doku.php?id = technical_indicators:bollinger_band_perce
    df_bb_per = (df_prices - df_bb_lower)/(df_bb_upper - df_bb_lower)

    fig = plt.figure(num=0, figsize = (8, 6))
    fig.suptitle("JPM Bollinger Bands (BB)", fontsize=14)
    ax01 = plt.subplot2grid((8, 6), (0, 0), colspan=6, rowspan=5)
    ax02 = plt.subplot2grid((8, 6), (6, 0), colspan=6, rowspan=3)
    ax01.plot(df_bb_upper, label='JPM BB Upper', color='steelblue')
    ax01.plot(df_bb_lower, label='JPM BB Lower', color='palevioletred')
    ax01.plot(df_prices, label='JPM Price', color='lightseagreen')
    ax01.plot(df_sma, label='JPM SMA', color='red')
    ax01.set_xlabel("Date")
    ax01.set_xlim(df_sma.index.min(), df_sma.index.max())
    ax01.set_ylabel("Normalized Price")
    ax01.grid()
    ax01.text(mid_date, .8, 'Chad Cortvriendt', fontsize=40, color='gray', alpha=0.5,
        ha='center', va='center', rotation='30')
    ax01.legend()
    ax01.set_title('Bollinger Bands Upper and Lower')

    ax02.plot(df_bb_per, label="JPM BB Percent", color='plum')
    ax02.set_title('Bollinger Band Percent')
    ax02.set_xlabel('Date')
    ax02.set_xlim(df_sma.index.min(), df_sma.index.max())
    ax02.legend()
    ax02.grid()
    ax02.set_ylabel('Percent')
    ax02.text(mid_date, .5, 'Chad Cortvriendt', fontsize=40, color='gray', alpha=0.5,
        ha='center', va='center', rotation='10')

    # plt.savefig("figure_bollinger.png")
    plt.clf()

    return df_bb_per

def calc_momentum(df_prices, mid_date):
    #momentum[t] = (price[t]/price[t-N]) - 1
    n = 20
    df_momentum = (df_prices/df_prices.shift(n)) - 1

    fig = plt.figure(num=0, figsize = (8, 6))
    fig.suptitle("JPM Momentum", fontsize=14)
    ax01 = plt.subplot2grid((8, 6), (0, 0), colspan=6, rowspan=4)
    ax02 = plt.subplot2grid((8, 6), (5, 0), colspan=6, rowspan=4)
    ax01.plot(df_momentum, label='JPM Momentum', color='steelblue')
    ax01.set_xlabel("Date")
    ax01.set_xlim(df_momentum.index.min(), df_momentum.index.max())
    ax01.set_ylabel("Momentum Value")
    ax01.grid()
    ax01.text(mid_date, .2, 'Chad Cortvriendt', fontsize=40, color='gray', alpha=0.5,
        ha='center', va='center', rotation='20')
    ax01.legend()
    ax01.set_title('JPM Momentum')

    ax02.plot(df_prices, label="JPM Price", color='burlywood')
    ax02.set_title('JPM Stock Price')
    ax02.set_xlabel('Date')
    ax02.set_xlim(df_prices.index.min(), df_prices.index.max())
    ax02.legend()
    ax02.grid()
    ax02.set_ylabel('Normalized Price')
    ax02.text(mid_date, .8, 'Chad Cortvriendt', fontsize=40, color='gray', alpha=0.5,
        ha='center', va='center', rotation='20')

    # plt.savefig("figure_momentum.png")
    plt.clf()

    return df_momentum

def calc_CMF(df_prices, symbol, sd, ed, mid_date):
    df_close = get_data(symbol, pd.date_range(sd, ed), addSPY=False, colname='Close')
    # df_close = df_close/df_close.ix[0,:]
    # df_close.ffill(inplace=True)
    # df_close.bfill(inplace=True)
    df_close.dropna(axis=0, how='any', inplace=True)


    df_low = get_data(symbol, pd.date_range(sd, ed), addSPY=False, colname='Low')
    # df_low = df_low/df_low.ix[0,:]
    # df_low.ffill(inplace=True)
    # df_low.bfill(inplace=True)
    df_low.dropna(axis=0, how='any', inplace=True)


    df_high = get_data(symbol, pd.date_range(sd, ed), addSPY=False, colname='High')
    # df_high = df_high/df_high.ix[0,:]
    # df_high.ffill(inplace=True)
    # df_high.bfill(inplace=True)
    df_high.dropna(axis=0, how='any', inplace=True)


    df_vol = get_data(symbol, pd.date_range(sd, ed), addSPY=False, colname='Volume')
    # df_vol = df_vol/df_vol.ix[0,:]
    # df_vol.ffill(inplace=True)
    # df_vol.bfill(inplace=True)
    df_vol.dropna(axis=0, how='any', inplace=True)

    close = df_close
    low = df_low.rolling(window=20).min()
    high = df_high.rolling(window=20).max()

    # calculate money flow multiplier
    df_mfp = ((close - low) - (high - close))/(high - low)

    # calculate money flow volume
    df_mfv = df_mfp * df_vol

    # calculate 20 period CMF
    df_cmf = df_mfv.rolling(window=20).sum() / df_vol.rolling(window=20).sum()

    fig = plt.figure(num=0, figsize = (8, 6))
    fig.suptitle("JPM Chaikin Money Flow (CMF)", fontsize=14)
    ax01 = plt.subplot2grid((8, 6), (0, 0), colspan=6, rowspan=3)
    ax02 = plt.subplot2grid((8, 6), (4, 0), colspan=6, rowspan=5)
    ax01.plot(df_cmf, label='JPM CMF', color='crimson')
    ax01.set_xlabel("Date")
    ax01.set_xlim(df_cmf.index.min(), df_cmf.index.max())
    ax01.set_ylabel("CMF Value")
    ax01.grid()
    ax01.text(mid_date, 0, 'Chad Cortvriendt', fontsize=40, color='gray', alpha=0.5,
        ha='center', va='center', rotation='20')
    ax01.legend()
    ax01.set_title('JPM CMF Value')

    ax02.plot(df_prices, label="JPM Price", color='gold')
    ax02.set_title('JPM Stock Price')
    ax02.set_xlabel('Date')
    ax02.set_xlim(df_prices.index.min(), df_prices.index.max())
    ax02.legend()
    ax02.grid()
    ax02.set_ylabel('Normalized Price')
    ax02.text(mid_date, .8, 'Chad Cortvriendt', fontsize=40, color='gray', alpha=0.5,
        ha='center', va='center', rotation='20')

    # plt.savefig("figure_cmf.png")
    plt.clf()

    return df_cmf

def calc_EMA(df_prices, mid_date):
    #https://corporatefinanceinstitute.com/resources/knowledge/trading-investing/exponential-moving-average-ema/
    n = 10
    k = 2/(n+1)

    df_ema_short = df_prices.copy()
    df_ema_short.ix[:, 0] = 1

    # 10 day simple moving average
    df_sma_short = df_prices.rolling(window=n).mean()

    # First exponential moving average is the simple moving average for the nth term
    df_ema_short.ix[n-1, 0] = df_sma_short.ix[n-1, 0]

    # Use formula to calculate the remaining exponential moving averages
    for x in range(len(df_ema_short)-n):
        i = x + n
        df_ema_short.ix[i, 0] = k * (df_prices.ix[i, 0] - df_ema_short.ix[i-1, 0]) + df_ema_short.ix[i-1, 0]

    df_ema_short.ix[:50, 0] = 1.0

    n = 50
    k = 2/(n+1)
    df_ema_long = df_prices.copy()
    df_ema_long.ix[:, 0] = 1
    # 50 day simple moving average
    df_sma_long = df_prices.rolling(window=n).mean()

    # First exponential moving average is the simple moving average for the nth term
    df_ema_long.ix[n-1, 0] = df_sma_long.ix[n-1, 0]

    # Use formula to calculate the remaining exponential moving averages
    for x in range(len(df_ema_long)-n):
        i = x + n
        df_ema_long.ix[i, 0] = k * (df_prices.ix[i, 0] - df_ema_long.ix[i-1, 0]) + df_ema_long.ix[i-1, 0]

    df_ema_long.ix[:50, 0] = 1.0

    fig = plt.figure(num=0, figsize = (8, 6))
    fig.suptitle("JPM Exponential Moving Average (EMA)", fontsize=14)
    ax01 = plt.subplot2grid((8, 6), (0, 0), colspan=6, rowspan=4)
    ax02 = plt.subplot2grid((8, 6), (5, 0), colspan=6, rowspan=4)
    ax01.plot(df_ema_short, label='JPM EMA 10 Day', color='darkorange')
    ax01.plot(df_ema_long, label='JPM EMA 50 Day', color='darkblue')
    ax01.set_xlabel("Date")
    ax01.set_xlim(df_ema_short.index.min(), df_ema_short.index.max())
    ax01.set_ylabel("EMA Value")
    ax01.grid()
    ax01.text(mid_date, .8, 'Chad Cortvriendt', fontsize=40, color='gray', alpha=0.5,
        ha='center', va='center', rotation='20')
    ax01.legend()
    ax01.set_title('JPM EMA Value')

    ax02.plot(df_prices, label="JPM Price", color='olivedrab')
    ax02.set_title('JPM Stock Price')
    ax02.set_xlabel('Date')
    ax02.set_xlim(df_prices.index.min(), df_prices.index.max())
    ax02.legend()
    ax02.grid()
    ax02.set_ylabel('Normalized Price')
    ax02.text(mid_date, .8, 'Chad Cortvriendt', fontsize=40, color='gray', alpha=0.5,
        ha='center', va='center', rotation='20')

    # plt.savefig("figure_ema.png")
    plt.clf()

    return df_ema_short, df_ema_long