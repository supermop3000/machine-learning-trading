# Machine Learning Trading Project: Q-Learning

## ManualStrategy.py
This file creates a `ManualStrategy` object. The `testPolicy` method returns a trades DataFrame based on a manual trading strategy for a given stock symbol, start date, end date, and starting amount of money. 

### Main Method:
- Takes in DataFrames representing:
  - Benchmark trades for in-sample data.
  - Manual trades for in-sample data.
  - Benchmark trades for out-sample data.
  - Manual trades for out-sample data.
- Uses `marketsimcode`'s `compute_portvals` to get portfolio value DataFrames for each.
- Calls `marketsimcode`'s `plot_graph` method to generate charts for the report.
- Outputs portfolio value stats for:
  - Benchmark in-sample.
  - Benchmark out-sample.
  - Manual in-sample.
  - Manual out-sample portfolios.

---

## marketsimcode.py
This file calculates portfolio values based on trades.

### Functions:
- **`compute_portvals`**:
  - Inputs: trades DataFrame, starting money, commission, impact, start date, and end date.
  - Returns: Portfolio value DataFrame.
- **`plot_graph`**:
  - Generates charts for reports (called by `ManualStrategy`).

---

## indicators.py
This file generates technical indicators and charts for a stock symbol within a given date range.

### Function:
- **`generate_indicators`**:
  - Creates indicator DataFrames for:
    - Simple Moving Average.
    - Bollinger Percent.
    - Momentum.
    - Chaikin Money Flow.
    - Exponential Moving Average.
  - Used by `StrategyLearner.py`'s `add_evidence` method.

---

## experiment1.py
Executes all code required for Experiment 1.

### Main Function:
- **`complete_experiment`**:
  - Creates `ManualStrategy` and `StrategyLearner` (QLearner) objects.
  - Trains the `StrategyLearner` using the `add_evidence` method.
  - Generates trades DataFrames for:
    - Benchmark strategy.
    - Manual strategy.
    - Learner strategy.
  - Uses `marketsimcode`'s `compute_portvals` to create portfolio value DataFrames.
  - Generates in-sample performance graphs using `plot_graph`.

---

## experiment2.py
Executes all code required for Experiment 2.

### Main Function:
- **`complete_experiment`**:
  - Trains three different QLearners, each using a different impact value.
  - Generates trades and portfolio value DataFrames for each learner.
  - Creates:
    - Line graphs.
    - Bar graphs (using `plot_bar_graph`).
  - Prints portfolio stats for all three learners.

---

## testproject.py
Runs the program and orchestrates all necessary files and functions.

### Workflow:
1. Creates:
   - Benchmark in-sample trades DataFrame.
   - Benchmark out-sample trades DataFrame.
   - Manual strategy in-sample trades DataFrame.
   - Manual strategy out-sample trades DataFrame.
2. Generates graphs for the report using `ManualStrategy`'s main method.
3. Runs experiments by calling `complete_experiment` methods in `experiment1.py` and `experiment2.py`.

---

## StrategyLearner.py
Defines the `StrategyLearner` class and integrates stock data and indicators with the Q-Learner.

### Constructor:
- Takes:
  - `verbose` (flag for print statements).
  - `impact` (impact of trades).
  - `commission` (trading fees).
- Creates a `QLearner` object.

### Methods:
- **`add_evidence`**:
  - Inputs: stock symbol, start date, end date, and starting money.
  - Generates trade indicators using `indicators.py`'s `generate_indicators`.
  - Discretizes indicator DataFrames to define states.
  - Trains the QLearner until convergence.
- **`testPolicy`**:
  - Uses the trained QLearner to output a trades DataFrame.

---

## QLearner.py
Implements the Q-Learner algorithm to determine an optimal trading policy.

### Features:
- Uses indicator values as states.
- Hallucinates experiences to optimize the Q-Table policy.
- Outputs the optimal trading strategy for a given state.

---

## How to Run the Code

### Steps:
1. Ensure all the following files are in the same directory:
   - `ManualStrategy.py`
   - `marketsimcode.py`
   - `indicators.py`
   - `experiment1.py`
   - `experiment2.py`
   - `testproject.py`
   - `StrategyLearner.py`
   - `QLearner.py`

2. Open a terminal and navigate to the folder containing the above files.
3. Run the following command:
   ```bash
   PYTHONPATH=../:. python testproject.py
   ```
4. Output:
   - Portfolio statistics are printed in the terminal.
   - Graphs are saved in the project root directory.

---

