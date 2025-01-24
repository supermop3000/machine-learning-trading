import datetime as dt
import os
import numpy as np
import pandas as pd
from util import get_data, plot_data
import indicators as ind
import marketsimcode as market_sim

class ManualStrategy:

    def __init__(self):
        pass

    def author(self):
        return 'ccortvriendt3'

    def other_stats(self, portval, start_date, end_date, fund):
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

    def main(self, df_in_bench_trades, df_in_manual_trades, df_out_bench_trades, df_out_manual_trades):
        # data, details, dates, rules
        symbol = 'JPM'
        in_start_date = dt.date(2008, 1, 1)
        in_end_date = dt.date(2009, 12, 31)
        out_start_date = dt.date(2010, 1, 1)
        out_end_date = dt.date(2011, 12, 31)
        sv = 100000
        commission = 9.95
        impact = .005

        df_in_bench_pv = market_sim.compute_portvals(df_in_bench_trades, start_date=in_start_date, end_date=in_end_date,
                                                     commission=commission, impact=impact, symbol=symbol)
        df_in_manual_pv = market_sim.compute_portvals(df_in_manual_trades, start_date=in_start_date,
                                                      end_date=in_end_date, commission=commission, impact=impact,
                                                      symbol=symbol)
        df_out_bench_pv = market_sim.compute_portvals(df_out_bench_trades, start_date=out_start_date,
                                                      end_date=out_end_date, commission=commission, impact=impact,
                                                      symbol=symbol)
        df_out_manual_pv = market_sim.compute_portvals(df_out_manual_trades, start_date=out_start_date,
                                                       end_date=out_end_date, commission=commission, impact=impact,
                                                       symbol=symbol)

        x_label = 'Date'
        y_label = 'Normalized Price'

        in_manual_shorts = []
        in_manual_longs = []
        out_manual_shorts = []
        out_manual_longs = []

        # get trades data
        for x in range(len(df_in_manual_trades)):
            if df_in_manual_trades.ix[x, 0] == 2000 or df_in_manual_trades.ix[x, 0] == 1000:
                in_manual_longs.append(df_in_manual_trades.index[x])

            elif df_in_manual_trades.ix[x, 0] == -2000 or df_in_manual_trades.ix[x, 0] == -1000:
                in_manual_shorts.append(df_in_manual_trades.index[x])

        for x in range(len(df_out_manual_trades)):
            if df_out_manual_trades.ix[x, 0] == 2000 or df_out_manual_trades.ix[x, 0] == 1000:
                out_manual_longs.append(df_out_manual_trades.index[x])

            elif df_out_manual_trades.ix[x, 0] == -2000 or df_out_manual_trades.ix[x, 0] == -1000:
                out_manual_shorts.append(df_out_manual_trades.index[x])


        # graph bench vs manual
        title = 'In Sample - Benchmark Strategy vs. Manual Strategy'
        file = 'insample_bench_vs_manual.png'
        line_one = 'Benchmark - In Sample'
        line_two = 'Manual - In Sample'
        # generate plots for report
        market_sim.plot_graph(df_in_bench_pv, df_in_manual_pv, x_label, y_label, file, line_one, line_two, title,
                              in_manual_shorts, in_manual_longs)

        title = 'Out Sample - Benchmark Strategy vs. Manual Strategy'
        file = 'outsample_bench_vs_manual.png'
        line_one = 'Benchmark - Out Sample'
        line_two = 'Manual - Out Sample'
        market_sim.plot_graph(df_out_bench_pv, df_out_manual_pv, x_label, y_label, file, line_one, line_two, title,
                              out_manual_shorts, out_manual_longs)

        print('* * * * * * * * * * * * MANUAL STRATEGY VS. BENCHMARK * * * * * * * * * * * * ')
        self.other_stats(df_in_bench_pv, in_start_date, in_end_date, 'BENCHMARK PORTFOLIO - IN SAMPLE')
        self.other_stats(df_in_manual_pv, in_start_date, in_end_date, 'MANUAL PORTFOLIO - IN SAMPLE')
        self.other_stats(df_out_bench_pv, out_start_date, out_end_date, 'BENCHMARK PORTFOLIO - OUT SAMPLE')
        self.other_stats(df_out_manual_pv, out_start_date, out_end_date, 'MANUAL PORTFOLIO - OUT SAMPLE')
        print('* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * ')


    def testPolicy(self, symbol="AAPL", sd=dt.datetime(2010, 1, 1), ed=dt.datetime(2011, 12, 13), sv=1000000):
        # create trades dataframe
        symbol_list = [symbol]
        df_trades = get_data(symbol_list, pd.date_range(sd, ed), addSPY=False)
        df_trades.dropna(axis=0, how='any', inplace=True)
        df_trades.index.rename('Date', inplace=True)
        df_trades.ix[:, 0] = 0

        sd = (df_trades.index[0])
        ed = (df_trades.index[-1])

        # create prices dataframe
        df_prices = get_data(symbol_list, pd.date_range(sd, ed), addSPY=False)
        df_prices.dropna(axis=0, how='any', inplace=True)
        df_prices.index.rename('Date', inplace=True)

        # set trading position to 0
        position = 0

        # generate indicators
        df_sma, df_momentum, df_cmf = ind.generate_indicators(symbol=symbol, sd=sd, ed=ed)

        # add indicators to prices dataframe
        df_prices['sma'] = df_sma
        df_prices['momentum'] = df_momentum
        df_prices['cmf'] = df_cmf

        # create manual trades dataframe
        for row, day in enumerate(df_prices.index):
            if df_prices.isnull().at[day, 'cmf']:
                pass

            else:
                if day != sd:
                    prev_day = df_prices.index[row-1]
                    doub_prev = df_prices.index[row-2]
                #
                # doub_prev_sma = df_prices.at[doub_prev, 'sma']
                # prev_sma = df_prices.at[prev_day, 'sma']
                prev_cmf = df_prices.at[prev_day, 'cmf']
                cur_cmf = df_prices.at[day, 'cmf']
                prev_momentum = df_prices.at[prev_day, 'momentum']
                cur_momentum = df_prices.at[day, 'momentum']
                cur_sma_ratio = df_prices.at[day, 'sma']

                cmf_slope = (cur_cmf-prev_cmf)/2
                mom_slope = (cur_momentum-prev_momentum)/2

                #yields 1.45x
                if cur_cmf < -.55:
                    if cur_momentum < -.1 and cur_sma_ratio < -.05:
                        if position == 0:
                            trade = 1000
                            df_trades.ix[day, 0] = trade
                            position = 1000

                        elif position == -1000:
                            trade = 2000
                            df_trades.ix[day, 0] = trade
                            position = 1000

                        elif position == 1000:
                            trade = 0
                            position = 1000
                            pass
                            # do nothing

                elif cur_cmf > .55:
                    if cur_momentum > .1 and cur_sma_ratio > .05:
                        if position == 0:
                            trade = -1000
                            df_trades.ix[day, 0] = trade
                            position = -1000

                        elif position == -1000:
                            trade = 0
                            position = -1000
                            pass
                            # do nothing

                        elif position == 1000:
                            trade = -2000
                            df_trades.ix[day, 0] = trade
                            position = -1000

        return df_trades




