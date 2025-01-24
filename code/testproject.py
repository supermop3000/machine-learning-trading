import datetime as dt
import os
import numpy as np
import pandas as pd
from util import get_data, plot_data
from pprint import pprint as pp
from ManualStrategy import ManualStrategy
import marketsimcode as market_sim
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
import StrategyLearner as sl
import experiment1 as ex1
import experiment2 as ex2

register_matplotlib_converters()

def author():
    return 'ccortvriendt3'

def compute_benchmark_portfolio(symbol, sd, ed, commission, impact):
    # create benchmark trades dataframe
    symbol_list = [symbol]
    df_bench_trades = get_data(symbol_list, pd.date_range(sd, ed), addSPY=False)
    df_bench_trades.dropna(axis=0, how='any', inplace=True)
    df_bench_trades.index.rename('Date', inplace=True)
    df_bench_trades.ix[:, 0] = 0
    df_bench_trades.ix[0, 0] = 1000
    sd = (df_bench_trades.index[0])
    ed = (df_bench_trades.index[-1])

    # compute benchmark portval
    return df_bench_trades

if __name__ == "__main__":
    symbol = 'JPM'
    # symbol = 'ML4T-220'

    # data, details, dates, rules
    in_start_date = dt.date(2008, 1, 1)
    in_end_date = dt.date(2009, 12, 31)
    out_start_date = dt.date(2010, 1, 1)
    out_end_date = dt.date(2011, 12, 31)
    sv = 100000
    commission = 9.95
    impact = .005

    # create manual strategy object
    ms = ManualStrategy()

    # create strategy learner object
    learner = sl.StrategyLearner(verbose=False, impact=impact, commission=commission)

    # train learner on in sample data, get learner in sample portvals, get learner out of sample portvals
    learner.add_evidence(symbol=symbol, sd=in_start_date, ed=in_end_date, sv=sv)
    df_in_learner_trades = learner.testPolicy(symbol=symbol, sd=in_start_date, ed=in_end_date, sv=sv)
    df_in_learner_pv = market_sim.compute_portvals(df_in_learner_trades, start_date=in_start_date, end_date=in_end_date,
                                           commission=commission, impact=impact, symbol=symbol)
    df_out_learner_trades = learner.testPolicy(symbol=symbol, sd=out_start_date, ed=out_end_date, sv=sv)
    df_out_learner_pv = market_sim.compute_portvals(df_out_learner_trades,start_date=out_start_date, end_date=out_end_date,
                                   commission=commission, impact=impact, symbol=symbol)

    # compute in sample benchmark trades
    df_in_bench_trades = compute_benchmark_portfolio(symbol, in_start_date, in_end_date, commission, impact)

    # compute in sample manual portfolio trades
    df_in_manual_trades = ms.testPolicy(symbol=symbol, sd=in_start_date, ed=in_end_date, sv=sv)

    # compute out sample benchmark trades
    df_out_bench_trades = compute_benchmark_portfolio(symbol, out_start_date, out_end_date, commission, impact)

    # compute out sample manual trades
    df_out_manual_trades = ms.testPolicy(symbol=symbol, sd=out_start_date, ed=out_end_date, sv=sv)

    # generate charts and print stats for benchmark vs manual strategy
    ms.main(df_in_bench_trades, df_in_manual_trades, df_out_bench_trades, df_out_manual_trades)

    # conduct experiment 1
    ex1.complete_experiment()

    # conduct experiment 2
    ex2.complete_experiment()
