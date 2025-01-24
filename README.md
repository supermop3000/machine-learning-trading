File Descriptions
ManualStrategy.py - This file creates a ManualStrategy object. The testPolicy method returns a trades dataframe based on a manual trading strategy for a given stock sybmol, start date, end date, and starting amount of money. The main method of this file takes in dataframes representing the following: benchmark trades for in sample data, manual trades for in sample data, benchmark trades for out sample data, and manual trades for out sample data. The trades dataframes are then passed to market_sim's compute_portvals to get porfolio value dataframes for each.  The main method then calls marketsimcode's plot_graph method to create charts required for the report. The main method also outputs portfolio value stats for the benchmark in sample, bechmark out sample, manual in sample, and manual out sample portfolios.

marketsimcode.py - This file receives a trades dataframe in it's compute_portvals function as well as starting amount of money, commission, impact, start date, and end date values. The function returns the portfolio value dataframe given the trades/orders provided in the dataframe. This file also contains a plot_graph method which is called by ManualStrategy's main method to generate charts for the report.

indicators.py - This file generates technical indicators and charts for a stock symbol between a start and end date. The file has a generate indicators function which is called by the StrategyLearner.py add evidence method. The generate indicators function creates indicator dataframes for Simple Moving Average, Bollinger Percent, Momentum, Chaikin Money Flow, and Exponential Moving Average.

experiment1.py - This file executes all the code required for experiment one. The primary method is the complete_experiment method which creates a Manual Strategy and Strategy Learner (QLearner) object based on the data details, dates, and rules given in the assignment. This method then trains the Strategy Learner using the Strategy Learner's add evidence method. Bechmark strategy, manual strategy, and learner strategy trade dataframes are calculated and then portfolio value dataframes are created for each using the marketsimcode compute_portvals method. In sample portfolio pertformance for the benchmark strategy, manual strategy, and learner strategy is then created by the plot_graph function.

experiment2.py - This executes all the code required for experiment two. The primary method is the complete_experiment method which creates and trains 3 different QLearners each one using a different impact value. Trades dataframes and portfolio value dataframes are created for each of the three learners and then a line graph and a bar graph is created for the report using the plot_graph and plot_bar_graph methods. Portfolio stats for each of the 3 learners is also printed in the console.

testproject.py - This file is responsible for running the program and calling all necessary files/functions. This file creates the benchmark in sample trades dataframe, benchmark out sample trades dataframe, manual strategy in sample trades dataframe, and the manual strategy out sample trades dataframe by calling the corresponding functions. This file then generates graphs for the report by calling ManualStrategy's main method. This file then runs the experiments for the report by calling complete_experiment methods in the experiment1.py and experiment2.py files.

StrategyLearner.py - This file creates a StrategyLearner object and contains all the code to wrap stock data and indicator to work with the Q-Learner. The constructor takes verbose flag (for print statements), impact, and commission values as arguments and then creates a QLearner object. The add_evidence method takes a stock symbol, start date, end date, and starting value of money as arguments. This method then gets a prices dataframe for the given stock within the given date range and generates trade indicators using that prices dataframe by calling indicators.py's method generate_indicators. This returns dataframes for simple moving average, momentum, and Chaikin money flow. These dataframes are discretized and used to define states. The QLearner is trained using these indicators as states until convergence. The testpolicy function of this file uses the trained QLearner and discretized bins from the add_evidence method to output a trades dataframe. 

QLearner.py - This file implements a QLearner that hallucinates experiences to come up with an optimal Q-Table policy. In this assignment the QLearner creates an optimal trading policy given indicator values as states.

How to Run the Code:
1. Ensure that all files below are contained in the same directory
		ManualStrategy.py
		marketsimcode.py
		indicators.py
		experiment1.py
		experiment2.py
		testproject.py
		StrategyLearner.py
		QLearner.py
2. Open your terminal console and in terminal navigate to the folder containing the files mentioned above.
3. Type in the following command in terminal: PYTHONPATH=../:. python testproject.py
4. This will call the main function in testproject.py which will then call all the necessary functions for the assignment. Several portfolio statistics are printed in the terminal window and the graphs are saved in the root directory where the project files live.
