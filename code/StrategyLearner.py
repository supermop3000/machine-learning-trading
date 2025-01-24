""""""  		  	   		     		  		  		    	 		 		   		 		  
"""  		  	   		     		  		  		    	 		 		   		 		  
Template for implementing StrategyLearner  (c) 2016 Tucker Balch  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
Copyright 2018, Georgia Institute of Technology (Georgia Tech)  		  	   		     		  		  		    	 		 		   		 		  
Atlanta, Georgia 30332  		  	   		     		  		  		    	 		 		   		 		  
All Rights Reserved  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
Template code for CS 4646/7646  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
Georgia Tech asserts copyright ownership of this template and all derivative  		  	   		     		  		  		    	 		 		   		 		  
works, including solutions to the projects assigned in this course. Students  		  	   		     		  		  		    	 		 		   		 		  
and other users of this template code are advised not to share it with others  		  	   		     		  		  		    	 		 		   		 		  
or to make it available on publicly viewable websites including repositories  		  	   		     		  		  		    	 		 		   		 		  
such as github and gitlab.  This copyright statement should not be removed  		  	   		     		  		  		    	 		 		   		 		  
or edited.  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
We do grant permission to share solutions privately with non-students such  		  	   		     		  		  		    	 		 		   		 		  
as potential employers. However, sharing with other current or future  		  	   		     		  		  		    	 		 		   		 		  
students of CS 7646 is prohibited and subject to being investigated as a  		  	   		     		  		  		    	 		 		   		 		  
GT honor code violation.  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
-----do not edit anything above this line---  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
Student Name: Chad Cortvriendt (replace with your name)  		  	   		     		  		  		    	 		 		   		 		  
GT User ID: ccortvriendt3 (replace with your User ID)  		  	   		     		  		  		    	 		 		   		 		  
GT ID: 903562623 (replace with your GT ID)  		  	   		     		  		  		    	 		 		   		 		  
"""  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
import datetime as dt  		  	   		     		  		  		    	 		 		   		 		  
import random
import indicators as ind
import numpy as np
import QLearner as ql
import pandas as pd  		  	   		     		  		  		    	 		 		   		 		  
import util as ut
from util import get_data, plot_data
  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
class StrategyLearner(object):  		  	   		     		  		  		    	 		 		   		 		  
    """  		  	   		     		  		  		    	 		 		   		 		  
    A strategy learner that can learn a trading policy using the same indicators used in ManualStrategy.  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
    :param verbose: If “verbose” is True, your code can print out information for debugging.  		  	   		     		  		  		    	 		 		   		 		  
        If verbose = False your code should not generate ANY output.  		  	   		     		  		  		    	 		 		   		 		  
    :type verbose: bool  		  	   		     		  		  		    	 		 		   		 		  
    :param impact: The market impact of each transaction, defaults to 0.0  		  	   		     		  		  		    	 		 		   		 		  
    :type impact: float  		  	   		     		  		  		    	 		 		   		 		  
    :param commission: The commission amount charged, defaults to 0.0  		  	   		     		  		  		    	 		 		   		 		  
    :type commission: float  		  	   		     		  		  		    	 		 		   		 		  
    """  		  	   		     		  		  		    	 		 		   		 		  
    # constructor  		  	   		     		  		  		    	 		 		   		 		  
    def __init__(self, verbose=False, impact=0.0, commission=0.0):  		  	   		     		  		  		    	 		 		   		 		  
        """  		  	   		     		  		  		    	 		 		   		 		  
        Constructor method  		  	   		     		  		  		    	 		 		   		 		  
        """  		  	   		     		  		  		    	 		 		   		 		  
        self.verbose = verbose  		  	   		     		  		  		    	 		 		   		 		  
        self.impact = impact  		  	   		     		  		  		    	 		 		   		 		  
        self.commission = commission
        self.bins_sma = []
        self.bins_momentum = []
        self.bins_cmf = []

        # instantiate learner
        self.learner = ql.QLearner(
            # num_states=100000,
            num_states=191920,
            num_actions=3,
            # alpha=0.2,
            alpha=0.4,
            gamma=.7,
            rar=0.98,
            radr=0.999,
            dyna=0,
            verbose=False,
        )

    def add_evidence(  		  	   		     		  		  		    	 		 		   		 		  
        self,  		  	   		     		  		  		    	 		 		   		 		  
        symbol="IBM",  		  	   		     		  		  		    	 		 		   		 		  
        sd=dt.datetime(2008, 1, 1),  		  	   		     		  		  		    	 		 		   		 		  
        ed=dt.datetime(2009, 1, 1),  		  	   		     		  		  		    	 		 		   		 		  
        sv=10000,  		  	   		     		  		  		    	 		 		   		 		  
    ):
        symbol_list = [symbol]

        # set converged bool to false
        converged = False

        # get prices dataframe
        df_prices = get_data(symbol_list, pd.date_range(sd, ed), addSPY=False)
        df_prices.dropna(axis=0, how='any', inplace=True)
        df_prices.index.rename('Date', inplace=True)

        # create trades dataframe
        df_trades = get_data(symbol_list, pd.date_range(sd, ed), addSPY=False)
        df_trades.dropna(axis=0, how='any', inplace=True)
        df_trades.index.rename('Date', inplace=True)
        df_trades.ix[:, 0] = 0

        # add your code to do learning here
        df_sma, df_momentum, df_cmf = ind.generate_indicators(symbol=symbol, sd=sd, ed=ed)
        pd.set_option("display.max_rows", None, "display.max_columns", None)

        # replace na with 0.0
        df_sma = df_sma.fillna(0)
        df_momentum = df_momentum.fillna(0)
        df_cmf = df_cmf.fillna(0)

        # discretize data
        df_disc_sma, self.bins_sma = pd.qcut(df_sma.ix[:, 0], q=20, retbins=True, labels=False, duplicates='drop')
        df_disc_momentum, self.bins_momentum = pd.qcut(df_momentum.ix[:, 0], q=20, retbins=True, labels=False, duplicates='drop')
        df_disc_cmf, self.bins_cmf = pd.qcut(df_cmf.ix[:, 0], q=20, retbins=True, labels=False, duplicates='drop')

        # check discretize
        # df_disc_check = df_prices.copy()
        # df_disc_check['sma'] = df_sma
        # df_disc_check['sma bin'] = df_disc_sma
        # df_disc_check['momentum'] = df_momentum
        # df_disc_check['momentum bin'] = df_disc_momentum
        # df_disc_check['cmf'] = df_cmf
        # df_disc_check['cmf bin'] = df_disc_cmf
        # print(df_disc_check)

        # definte states
        df_state = pd.DataFrame(df_disc_sma.map(str) + df_disc_momentum.map(str) + df_disc_cmf.map(str)).astype(int)

        epoch = 0
        position = 0
        min_epoch = 5

        prev_portval = 0
        prev_trades = df_trades.copy()

        while not converged:
            portval = 0
            x = df_state.ix[0, 0]
            action = self.learner.querysetstate(x)

            for y in range(len(df_sma)):

                if y == 0:
                    reward = 0

                else:
                    # if action is to do nothing
                    if action == 0:
                        # if we have a long position
                        if position == 1000:
                            reward = 1000 * (df_prices.ix[y, 0] - df_prices.ix[y-1, 0])

                        # if we have a short position
                        elif position == -1000:
                            reward = 1000 * (df_prices.ix[y-1, 0] - df_prices.ix[y, 0])

                        # if we have no position
                        elif position == 0:
                            reward = 0

                    # calculate reward for buy
                    elif action == 1:
                        impact_price = df_prices.ix[y-1, 0] * (1 + self.impact)
                        reward = 1000 * (df_prices.ix[y, 0] - impact_price) - self.commission

                    # calculate reward for sell
                    elif action == 2:
                        impact_price = df_prices.ix[y, 0] * (1 - self.impact)
                        reward = 1000 * (df_prices.ix[y-1, 0] - impact_price) - self.commission

                portval += reward
                action = self.learner.query(x, reward)

                # implement action
                if action == 0:
                    trade = 0

                elif action == 1:
                    if position == 0:
                        trade = 1000
                        df_trades.ix[y, 0] = trade
                        position = 1000

                    elif position == -1000:
                        trade = 2000
                        df_trades.ix[y, 0] = trade
                        position = 1000

                    elif position == 1000:
                        trade = 0
                        position = 1000
                        pass

                elif action == 2:
                    if position == 0:
                        trade = -1000
                        df_trades.ix[y, 0] = trade
                        position = -1000

                    elif position == -1000:
                        trade = 0
                        position = -1000
                        pass
                        # do nothing

                    elif position == 1000:
                        trade = -2000
                        df_trades.ix[y, 0] = trade
                        position = -1000

                df_trades.ix[y, 0] = trade
                x = df_state.ix[y, 0]

            # print('PORTVAL:' + str(portval))
            # print('PREV_PORTVAL: ' + str(prev_portval))

            epoch += 1
            # check if converged
            if epoch >= min_epoch and prev_portval == portval and pd.DataFrame.equals(df_trades,prev_trades):
                converged = True

            prev_portval = portval
            prev_trades = df_trades

        # policy = df_trades.copy()
        # policy['state'] = df_state
        #
        # print(policy)

        # return df_trades

    # this method should use the existing policy and test it against new data  		  	   		     		  		  		    	 		 		   		 		  
    def testPolicy(  		  	   		     		  		  		    	 		 		   		 		  
        self,  		  	   		     		  		  		    	 		 		   		 		  
        symbol="IBM",  		  	   		     		  		  		    	 		 		   		 		  
        sd=dt.datetime(2009, 1, 1),  		  	   		     		  		  		    	 		 		   		 		  
        ed=dt.datetime(2010, 1, 1),  		  	   		     		  		  		    	 		 		   		 		  
        sv=10000,  		  	   		     		  		  		    	 		 		   		 		  
    ):
        symbol_list = [symbol]

        # get prices dataframe
        df_prices = get_data(symbol_list, pd.date_range(sd, ed), addSPY=False)
        df_prices.dropna(axis=0, how='any', inplace=True)
        df_prices.index.rename('Date', inplace=True)

        # create trades dataframe
        df_trades = get_data(symbol_list, pd.date_range(sd, ed), addSPY=False)
        df_trades.dropna(axis=0, how='any', inplace=True)
        df_trades.index.rename('Date', inplace=True)
        df_trades.ix[:, 0] = 0

        # add your code to do learning here
        df_sma, df_momentum, df_cmf = ind.generate_indicators(symbol=symbol, sd=sd, ed=ed)
        pd.set_option("display.max_rows", None, "display.max_columns", None)

        # replace na with 0.0
        df_sma = df_sma.fillna(0)
        df_momentum = df_momentum.fillna(0)
        df_cmf = df_cmf.fillna(0)

        df_disc_sma = df_sma.copy()
        df_disc_momentum = df_momentum.copy()
        df_disc_cmf = df_cmf.copy()

        # discretize using saved bin ranges
        df_disc_sma[symbol] = np.digitize(df_sma, self.bins_sma, right=True)-1
        df_disc_momentum[symbol] = np.digitize(df_momentum, self.bins_momentum, right=True)-1
        df_disc_cmf[symbol] = np.digitize(df_cmf, self.bins_cmf, right=True)-1


        # convert data frame to series to concatenate strings to ints for state analysis
        df_disc_sma = df_disc_sma.squeeze()
        df_disc_momentum = df_disc_momentum.squeeze()
        df_disc_cmf = df_disc_cmf.squeeze()

        # replace out of bounds min and max values
        df_disc_sma.replace(20, 19, inplace=True)
        df_disc_momentum.replace(20, 19, inplace=True)
        df_disc_cmf.replace(20, 19, inplace=True)
        df_disc_sma.replace(-1, 0, inplace=True)
        df_disc_momentum.replace(-1, 0, inplace=True)
        df_disc_cmf.replace(-1, 0, inplace=True)

        # check discretize
        # df_disc_check = df_prices.copy()
        # df_disc_check['sma'] = df_sma
        # df_disc_check['sma bin'] = df_disc_sma
        # df_disc_check['momentum'] = df_momentum
        # df_disc_check['momentum bin'] = df_disc_momentum
        # df_disc_check['cmf'] = df_cmf
        # df_disc_check['cmf bin'] = df_disc_cmf
        # print(df_disc_check)

        # calculate state dataframe
        df_state = pd.DataFrame(df_disc_sma.map(str) + df_disc_momentum.map(str) + df_disc_cmf.map(str)).astype(int)

        # set position to 0
        position = 0

        # set initial x
        x = df_state.ix[0, 0]

        for y in range(len(df_sma)):
            action = self.learner.querysetstate(x)

            # implement action
            if action == 0:
                trade = 0

            elif action == 1:
                if position == 0:
                    trade = 1000
                    df_trades.ix[y, 0] = trade
                    position = 1000

                elif position == -1000:
                    trade = 2000
                    df_trades.ix[y, 0] = trade
                    position = 1000

                elif position == 1000:
                    trade = 0
                    position = 1000
                    pass

            elif action == 2:
                if position == 0:
                    trade = -1000
                    df_trades.ix[y, 0] = trade
                    position = -1000

                elif position == -1000:
                    trade = 0
                    position = -1000
                    pass
                    # do nothing

                elif position == 1000:
                    trade = -2000
                    df_trades.ix[y, 0] = trade
                    position = -1000

            df_trades.ix[y, 0] = trade
            x = df_state.ix[y, 0]

        return df_trades

    def author(self):
        return 'ccortvriendt3'
  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
if __name__ == "__main__":  		  	   		     		  		  		    	 		 		   		 		  
    print("One does not simply think up a strategy")  		  	   		     		  		  		    	 		 		   		 		  
