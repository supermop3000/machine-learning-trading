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

def plot_bar_graph(learner_one, learner_two, learner_three, x_label, y_label, file, bar_one, bar_two, bar_three, title):
    plt.bar(bar_one, learner_one, color='g')
    plt.bar(bar_two, learner_two, color='r')
    plt.bar(bar_three, learner_three, color='b')

    plt.xlabel(x_label)
    plt.ylabel(y_label)

    plt.title(title)
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
    sv = 100000
    commission = 0


    # create strategy learner object with impact 0
    impact = 0
    learner_one = sl.StrategyLearner(verbose=False, impact=impact, commission=commission)
    learner_one.add_evidence(symbol=symbol, sd=start_date_in, ed=end_date_in, sv=sv)
    df_learner_one_trades_in = learner_one.testPolicy(symbol=symbol, sd=start_date_in, ed=end_date_in, sv=sv)
    df_learner_one_pv_in = ms.compute_portvals(df_learner_one_trades_in, start_date=start_date_in, end_date=end_date_in,
                                               commission=commission, impact=impact, symbol=symbol)

    # create strategy learner object with impact .1
    impact = .02
    learner_two = sl.StrategyLearner(verbose=False, impact=impact, commission=commission)
    learner_two.add_evidence(symbol=symbol, sd=start_date_in, ed=end_date_in, sv=sv)
    df_learner_two_trades_in = learner_two.testPolicy(symbol=symbol, sd=start_date_in, ed=end_date_in, sv=sv)
    df_learner_two_pv_in = ms.compute_portvals(df_learner_two_trades_in, start_date=start_date_in, end_date=end_date_in,
                                               commission=commission, impact=impact, symbol=symbol)

    # create strategy learner object with impact .2
    impact = .1
    learner_three = sl.StrategyLearner(verbose=False, impact=impact, commission=commission)
    learner_three.add_evidence(symbol=symbol, sd=start_date_in, ed=end_date_in, sv=sv)
    df_learner_three_trades_in = learner_three.testPolicy(symbol=symbol, sd=start_date_in, ed=end_date_in, sv=sv)
    df_learner_three_pv_in = ms.compute_portvals(df_learner_three_trades_in, start_date=start_date_in, end_date=end_date_in,
                                               commission=commission, impact=impact, symbol=symbol)


    learner_one_trade_count = df_learner_one_trades_in[df_learner_one_trades_in != 0].count()
    learner_two_trade_count = df_learner_two_trades_in[df_learner_two_trades_in != 0].count()
    learner_three_trade_count = df_learner_three_trades_in[df_learner_three_trades_in != 0].count()

    # graph portval for learners
    title = 'Experiment 2: In Sample - Portfolio Values vs. Changing Impact'
    x_label = 'Date'
    y_label = 'Normalized Price'
    file = 'experiment2_portvals.png'
    line_one = 'Learner One - Impact: 0'
    line_two = 'Learner Two - Impact: .02'
    line_three = 'Learner Three - Impact: .1'
    plot_graph(df_learner_one_pv_in, df_learner_two_pv_in, df_learner_three_pv_in, x_label, y_label, file, line_one, line_two, line_three, title)

    # bar graph number of trades per learner
    title = 'Experiment 2: In Sample - Trade Frequency vs. Changing Impact'
    x_label = 'Learner'
    y_label = 'Number of Trades'
    file = 'experiment2_trades.png'
    line_one = 'Learner One - Impact: 0'
    line_two = 'Learner Two - Impact: .02'
    line_three = 'Learner Three - Impact: .1'
    plot_bar_graph(learner_one_trade_count, learner_two_trade_count, learner_three_trade_count, x_label, y_label, file, line_one, line_two, line_three, title)

    print('* * * * * * * * * * * * EXPERIMENT TWO * * * * * * * * * * * * ')
    other_stats(df_learner_one_pv_in, start_date_in, end_date_in, 'LEARNER ONE - IMPACT: 0')
    other_stats(df_learner_two_pv_in, start_date_in, end_date_in, 'LEARNER TWO - IMPACT: .02')
    other_stats(df_learner_three_pv_in, start_date_in, end_date_in, 'LEARNER THREE - IMPACT: .1')
    print('* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * ')