In this project, I have 11 .py files shown below.

BagLearner.pyBestPossibleStrategy.pycomparative_analysis.pyindicators.pymarketsim.pyML_based.pyRTLearner.pyrule_based.pytweak_parameter_ML.pyutil.py
visualization_data.py

Run indicators.py to obtain five indicators and helper data, and then normalize indictors and generate 5 charts fig1 to fig 5 for Part 1 of the report.

Run BestPossibleStrategy.py to create order file for best possible strategy, get summary report of performance of best possible strategy and benchmark, and make a chart fig6 to simulate the normalized portfolios of both for part 2 of the report.

Run rule_based.py to conduct manual rule strategy, create order files for the strategy over both in sample and out of sample periods, and generate fig 7 to simulate normalized portfolios over in sample period in part 3 of the report.

Run ML_based.py to conduct ML strategy, create order files for the strategy over both in sample and out of sample periods, and generate fig 8 to simulate normalized portfolios over in sample period in part 4, and generate fig 12 to simulate normalized portfolios over out of sample period for benchmark, rule based and ML based strategies in part 6 of the report.

Run tweak_parameter_ML.py to tweak parameters for YBuy/YSell, numbers of bags and leaf_size to find best performance over in sample period. It may take more than 10 minutes.

Run visualization_data.py to create fig 9 to 11 to show normalized Slope and normalized MFI labeled by rule strategy, before and after ML in part 5. 

Run comparative_analysis.py to create final performance table of CR and Sharpe ratio from benchmark, rule trader and ML trader over in sample and out sample. Since it has 20 iterations, it may take 4 minutes.

RTLearner and BagLearner were modified to classification learners.

marketsim is used to simulate portfolio from order files
util is used to get price and volume data from historical price files of stocks
