import datetime as dt
import pandas as pd
from util import get_data, plot_data
import marketsimcode as ms
import matplotlib.pyplot as plt
import ManualStrategy as ml
import StrategyLearner as sl
import random as rand

def author():
    return 'ccortvriendt3'

def plot_graph(df_bench, df_manual, df_learner, x_label, y_label, file, line_one, line_two, line_three, title):
    # graph title
    plt.title(title)

    # plot line
    plt.plot(df_bench, label=line_one, color='g')
    plt.plot(df_manual, label=line_two, color='r')
    plt.plot(df_learner, label=line_three, color='b')

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

def compute_benchmark_portfolio(symbol, sd, ed, commission, impact):
    # create benchmark dataframe
    symbol_list = [symbol]
    df_bench = get_data(symbol_list, pd.date_range(sd, ed), addSPY=False)
    df_bench.dropna(axis=0, how='any', inplace=True)
    df_bench.index.rename('Date', inplace=True)
    df_bench.ix[:, 0] = 0
    df_bench.ix[0, 0] = 1000
    sd = (df_bench.index[0])
    ed = (df_bench.index[-1])

    # compute benchmark portval
    df_bench_pv = ms.compute_portvals(df_bench, start_date=sd, end_date=ed, commission=commission, impact=impact,
                                      symbol=symbol)
    return df_bench_pv


def other_stats(portval, start_date, end_date, fund):
    df_daily_returns = portval.copy()
    df_daily_returns[1:] = (portval[1:] / portval[:-1].values) - 1
    df_daily_returns = df_daily_returns.ix[1:]

    df_cum_returns = (portval[-1] / portval[0]) - 1
    std_daily_returns = df_daily_returns.std(axis=0)
    avg_daily_returns = df_daily_returns.mean(axis=0)

    print('- - - - - - - - - - - - ' + str(fund) + ' - - - - - - - - - - - -')
    print(f"Date Range: {start_date} to {end_date}")
    # print()
    # print(f"Sharpe Ratio of Fund: {sharpe_ratio}")
    # print(f"Sharpe Ratio of SPY : {sharpe_ratio_SPY}")
    # print()
    print(f"Cumulative Return of Fund: {df_cum_returns}")
    # print(f"Cumulative Return of SPY : {cum_ret_SPY}")
    # print()
    print(f"Standard Deviation of Fund: {std_daily_returns}")
    # print(f"Standard Deviation of SPY : {std_daily_ret_SPY}")
    # print()
    print(f"Average Daily Return of Fund: {avg_daily_returns}")
    # print(f"Average Daily Return of SPY : {avg_daily_ret_SPY}")
    # print()
    print(f"Final Portfolio Value: {portval[-1]}")

def complete_experiment():
    rand.seed(1)
    symbol = 'JPM'
    start_date_in = dt.date(2008, 1, 1)
    end_date_in = dt.date(2009, 12, 31)

    out_start = dt.date(2010, 1, 1)
    out_end = dt.date(2011, 12, 31)

    # starting cash
    sv = 100000

    # commission
    commission = 9.95

    # impact
    impact = .005

    # create manual strategy object
    manual_strategy = ml.ManualStrategy()

    # create strategy learner object
    learner = sl.StrategyLearner(verbose=False, impact=impact, commission=commission)

    # compute in sample benchmark
    df_bench_pv_in = compute_benchmark_portfolio(symbol, start_date_in, end_date_in, commission, impact)

    # compute in sample manual strategy
    df_manual_pv_in = manual_strategy.testPolicy(symbol=symbol, sd=start_date_in, ed=end_date_in, sv=sv)
    df_manual_pv_in = ms.compute_portvals(df_manual_pv_in, start_date=start_date_in, end_date=end_date_in,
                                          commission=commission, impact=impact, symbol=symbol)

    # train learner and calculate portval of insample
    learner.add_evidence(symbol=symbol, sd=start_date_in, ed=end_date_in, sv=sv)
    df_learner_trades_in = learner.testPolicy(symbol=symbol, sd=start_date_in, ed=end_date_in, sv=sv)
    df_learner_pv_in = ms.compute_portvals(df_learner_trades_in, start_date=start_date_in, end_date=end_date_in,
                                           commission=commission, impact=impact, symbol=symbol)



    df_manual_pv_out = manual_strategy.testPolicy(symbol=symbol, sd=out_start, ed=out_end, sv=sv)
    df_manual_pv_out = ms.compute_portvals(df_manual_pv_out, start_date=out_start, end_date=out_end,
                                          commission=commission, impact=impact, symbol=symbol)

    df_bench_pv_out = compute_benchmark_portfolio(symbol, out_start, out_end, commission, impact)

    df_learner_trades_out = learner.testPolicy(symbol=symbol, sd=out_start, ed=out_end, sv=sv)
    df_learner_pv_out = ms.compute_portvals(df_learner_trades_out, start_date=out_start, end_date=out_end,
                                           commission=commission, impact=impact, symbol=symbol)

    # graph bench vs manual
    title = 'Experiment 1: In Sample - Benchmark vs. Manual vs. Learner'
    x_label = 'Date'
    y_label = 'Normalized Price'
    file = 'experiment1.png'
    line_one = 'Benchmark - In Sample'
    line_two = 'Manual - In Sample'
    line_three = 'Learner - In Sample'
    plot_graph(df_bench_pv_in, df_manual_pv_in, df_learner_pv_in, x_label, y_label, file, line_one, line_two, line_three, title)

    # graph bench vs manual for out sample
    title = 'Experiment 1: Out Sample - Benchmark vs. Manual vs. Learner'
    x_label = 'Date'
    y_label = 'Normalized Price'
    file = 'experiment1_out.png'
    line_one = 'Benchmark - Out Sample'
    line_two = 'Manual - Out Sample'
    line_three = 'Learner - Out Sample'
    plot_graph(df_bench_pv_out, df_manual_pv_out, df_learner_pv_out, x_label, y_label, file, line_one, line_two, line_three, title)

    print('* * * * * * * * * * * * EXPERIMENT ONE * * * * * * * * * * * * ')
    other_stats(df_bench_pv_in, start_date_in, end_date_in, 'BENCHMARK PORTFOLIO - IN SAMPLE')
    other_stats(df_manual_pv_in, start_date_in, end_date_in, 'MANUAL PORTFOLIO - IN SAMPLE')
    other_stats(df_learner_pv_in, start_date_in, end_date_in, 'LEARNER PORTFOLIO - IN SAMPLE')
    print('* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * ')