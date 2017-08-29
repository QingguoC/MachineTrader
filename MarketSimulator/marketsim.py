"""Market simulator"""

import pandas as pd
import numpy as np
import datetime as dt
import os
from util import get_data, plot_data

def author():
    return 'Qingguo'
    
def compute_portvals(orders_file = "./orders/orders-3.csv", start_val = 1000000):
    
    lev_limit=1.5
    secret_date=dt.datetime.strptime("2011-06-15","%Y-%m-%d")
    orders=pd.read_csv(orders_file,parse_dates=True, index_col='Date',na_values=['nan'])
    orders.sort_index(inplace=True)
    start_date=orders.index[0]
    end_date=orders.index[-1]
    dates=pd.date_range(start_date,end_date)
    symbols=orders.Symbol.unique().tolist()
    prices=get_data(symbols=symbols,dates=dates)
    prices['CASH']=1
    if "SPY" not in symbols:
        prices.drop(['SPY'],1,inplace=True)
        
    orginprices=prices.copy()
    prices.fillna(method="ffill",inplace=True)
    prices.fillna(method="bfill",inplace=True)
    
    trades=pd.DataFrame(data=0,index=prices.index,columns=prices.columns)
    holdings=pd.DataFrame(data=0,index=trades.index,columns=trades.columns)
    prevData=holdings.ix[0]
    prevData['CASH']=start_val
    #prevDate=start_date    
    

    for date, price in prices.iterrows():
        holdings.ix[date]=prevData


        if date !=secret_date and date in orders.index:

            for index, onetrade in orders.loc[date:date].iterrows():
                
                symbol,order,share=onetrade
                if np.isnan(orginprices.ix[date,symbol]):
                    continue 
                if order == 'SELL':
                    share=-share
                forw_trade=trades.ix[date]
                forw_trade[symbol] = forw_trade[symbol]+share
                forw_trade['CASH'] = forw_trade['CASH']-share * prices.ix[date,symbol]
                forw_holding=prevData.copy()
                forw_holding[symbol]=prevData[symbol]+share
                forw_holding['CASH']=prevData['CASH']-share * prices.ix[date,symbol]
                forw_value=forw_holding*prices.ix[date]
                forw_lev=leverage(forw_value)
                
                curr_value=holdings.ix[date]*prices.ix[date]
                curr_lev=leverage(curr_value)
                if forw_lev<lev_limit or forw_lev < curr_lev:
                    trades.ix[date]=forw_trade
                    holdings.ix[date]=forw_holding
                    prevData=holdings.ix[date]

        

            
        prevData=holdings.ix[date]    
        
    values=holdings*prices    

    portvals = pd.DataFrame(values.sum(axis=1),columns=['portvals'])

#==============================================================================
#     print trades.head(20)
#     print holdings.head(20)
#     print values.head(20)
#     print prices.head(20)
#==============================================================================
#==============================================================================
#     values.to_csv("values.csv")
#     trades.to_csv("trades.csv")
#     prices.to_csv("prices.csv")
#     holdings.to_csv("holdings.csv")
#     portvals.to_csv("portvals.csv")
#     orders.to_csv("orders.csv")
#==============================================================================

    return portvals

def leverage(value):
    lev=sum(abs(value[:-1]))/(sum(value[:-1])+value[-1])
    return lev
    
def compute_portfolio_stats(portvals,
    rfr = 0.0, sf = 252.0):
    
    cr=portvals[-1]/portvals[0]-1
    dr=portvals.copy()
    dr[1:]=portvals[1:]/portvals[:-1].values-1
    dr[0]=0
    adr=dr[1:].mean()
    sddr=dr[1:].std()
    sr=np.sqrt(sf)*(adr-rfr)/sddr
    
    return cr, adr, sddr, sr
def test_code():
    # this is a helper function you can use to test your code
    # note that during autograding his function will not be called.
    # Define input parameters

    of = "./orders/orders-03.csv"
    sv = 1000000

    # Process orders
    portvals = compute_portvals(orders_file = of, start_val = sv)
    if isinstance(portvals, pd.DataFrame):
        portvals = portvals[portvals.columns[0]] # just get the first column
    else:
        print "warning, code did not return a DataFrame"
    
    # Get portfolio stats
    # Here we just fake the data. you should use your code from previous assignments.
    start_date = dt.date.strftime(portvals.index[0],"%Y-%m-%d")
    end_date = dt.date.strftime(portvals.index[-1],"%Y-%m-%d")
    cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = compute_portfolio_stats(portvals)
    SPY=get_data(symbols=["$SPX"],dates=pd.date_range(start=start_date,end=end_date))
    spy=SPY['$SPX']
    cum_ret_SPY, avg_daily_ret_SPY, std_daily_ret_SPY, sharpe_ratio_SPY = compute_portfolio_stats(spy)

    # Compare portfolio against $SPX
    print "Date Range: {} to {}".format(start_date, end_date)
    print
    print "Sharpe Ratio of Fund: {}".format(sharpe_ratio)
    print "Sharpe Ratio of SPX : {}".format(sharpe_ratio_SPY)
    print
    print "Cumulative Return of Fund: {}".format(cum_ret)
    print "Cumulative Return of SPX : {}".format(cum_ret_SPY)
    print
    print "Standard Deviation of Fund: {}".format(std_daily_ret)
    print "Standard Deviation of SPX : {}".format(std_daily_ret_SPY)
    print
    print "Average Daily Return of Fund: {}".format(avg_daily_ret)
    print "Average Daily Return of SPX : {}".format(avg_daily_ret_SPY)
    print
    print "Final Portfolio Value: {}".format(portvals[-1])

if __name__ == "__main__":
    test_code()
