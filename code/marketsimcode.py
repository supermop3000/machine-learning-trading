import datetime as dt
import os
import numpy as np
import pandas as pd
from util import get_data, plot_data
from pprint import pprint as pp
import matplotlib.pyplot as plt


def compute_portvals(
        df_trades,
        start_val=100000,
        commission=0,
        impact=0.0,
        start_date=dt.date(2008, 1, 1),
        end_date=dt.date(2009, 12, 31),
        symbol='AAPL'
):
    start_date = (df_trades.index[0])
    end_date = (df_trades.index[-1])


    # Read in orders file
    df_ord = df_trades

    # Create prices data frame
    df_prices = df_ord.copy()

    # Extract order symbols from dataframe
    ord_symbols = list(df_prices.columns.values)

    # Get price data for all symbols in the orders file
    df_prices = get_data(ord_symbols, pd.date_range(start_date, end_date))
    df_prices = df_prices[ord_symbols]


    # Add CASH column and set to 1.00
    df_prices['CASH'] = 1.00

    # Create holdings data frame
    df_holdings = df_prices.copy()
    for i in range(len(ord_symbols)):
        for col in df_prices:
            if col == ord_symbols[i]:
                df_holdings[ord_symbols[i]] = 0.0
    df_holdings['COST'] = 0.0
    df_holdings['CASH'] = 0.0
    df_holdings.at[start_date, 'CASH'] = start_val

    # Get holdings based on orders in order data frame
    for i in range(len(df_ord)):
        date = df_ord.index[i]
        shares = df_ord.iloc[i][0]
        order = None
        if shares > 0:
            order = "BUY"

        elif shares < 0:
            order = "SELL"

        order_cost = shares * df_prices.loc[date, symbol] * (1 + impact) + commission

        # If buy order
        if order == "BUY":

            df_holdings.loc[date, symbol] += shares
            df_holdings.loc[date, 'COST'] -= order_cost
            df_holdings.loc[date, 'CASH'] -= order_cost

        # If sell order
        elif order == "SELL":
            df_holdings.loc[date, symbol] = shares
            df_holdings.loc[date, 'COST'] += -order_cost
            df_holdings.loc[date, 'CASH'] += -order_cost

    # Sum holdings to get daily holding amounts
    df_holdings = df_holdings.cumsum()

    # Create daily portfolio data frame by multiplying prices dataframe by holdings
    df_portfolio = df_holdings * df_prices

    # Drop cost column
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.drop.html
    df_portfolio = df_portfolio.drop(columns=['COST'])

    # Create data frame of sum of column values from portfolio data frame
    df_port_val = df_portfolio.sum(axis=1)

    df_port_val = df_port_val/df_port_val.ix[0, :]

    return df_port_val

def author():
    return 'ccortvriendt3'


def plot_graph(df_bench, df_manual, x_label, y_label, file, line_one, line_two, title, manual_shorts, manual_longs):
    # graph title
    plt.title(title)

    # plot line
    plt.plot(df_bench, label=line_one, color='g')
    plt.plot(df_manual, label=line_two, color='r')

    min_y = min(df_bench.min(), df_manual.min())
    max_y = max(df_bench.max(), df_manual.max())

    plt.vlines(x=manual_shorts, ymin=min_y, ymax=max_y, colors='black', label='Short', linestyles='dashed')
    plt.vlines(x=manual_longs, ymin=min_y, ymax=max_y, colors='blue', label='Long', linestyles='dashed')

    # create labels
    plt.xlabel(x_label)
    plt.ylabel(y_label)

    # set x bounds
    plt.xlim(df_bench.index.min(), df_bench.index.max())

    # plot grid
    plt.grid()

    # plot legend
    plt.legend()

    plt.savefig(file)
    plt.clf()