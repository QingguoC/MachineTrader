# -*- coding: utf-8 -*-
"""
Created on Fri Apr 14 09:28:25 2017

@author: GuoFang
"""

import pandas as pd
import datetime as dt
import util as ut
import StrategyLearner as sl
from marketsim import compute_portvals
import matplotlib.pyplot as plt
def test_code(verb = True):
    st=dt.datetime.now()
    # instantiate the strategy learner
    learner = sl.StrategyLearner(verbose = verb)

    # set parameters for training the learner
    #sym = "ML4T-220"
    #sym = "IBM"
    #sym="UNH"
    #sym="AAPL"
    sym="GOOG"
    #sym="SINE_FAST_NOISE"
    #sym="DIS"
    #sym="MSFT"
    #sym="AMZN"
    stdate =dt.datetime(2008,1,1)
    enddate =dt.datetime(2009,12,31) # just a few days for "shake out"

    # train the learner
    learner.addEvidence(symbol = sym, sd = stdate, \
        ed = enddate, sv = 100000) 
    et=dt.datetime.now()
    print (et-st).seconds,"seconds to train"
    # set parameters for testing
    #sym = "IBM"
    stdate =dt.datetime(2008,1,1)
    enddate =dt.datetime(2009,12,31)

    # get some data for reference
    syms=[sym]
    dates = pd.date_range(stdate, enddate)
    prices_all = ut.get_data(syms, dates)  # automatically adds SPY
    prices = prices_all[syms]  # only portfolio symbols
    if verb: print prices

    # test the learner
    df_trades = learner.testPolicy(symbol = sym, sd = stdate, \
        ed = enddate, sv = 100000)
    simulate(sym,df_trades,stdate,enddate,prices)
    
        # set parameters for testing
    #sym = "IBM"
    stdate =dt.datetime(2010,1,1)
    enddate =dt.datetime(2011,12,31)

    # get some data for reference
    syms=[sym]
    dates = pd.date_range(stdate, enddate)
    prices_all = ut.get_data(syms, dates)  # automatically adds SPY
    prices = prices_all[syms]  # only portfolio symbols
    if verb: print prices

    # test the learner
    df_trades = learner.testPolicy(symbol = sym, sd = stdate, \
        ed = enddate, sv = 100000)
    simulate(sym,df_trades,stdate,enddate,prices)

def simulate(sym,df_trades,sd,ed,prices):
    trade_list=[]
    
    for date in df_trades.index:
        t=df_trades.ix[date,sym]
        
        if t>0:
            trade_list.append([date.date(),sym,"BUY",t])
        elif t<0:
            trade_list.append([date.date(),sym,"SELL",-t])
    ordersdf = pd.DataFrame(trade_list,columns=["Date","Symbol","Order","Shares"])
    ordersdf.to_csv("./orders.csv",index=False)        
    
    oportval=compute_portvals("./orders.csv", start_val =100000,start_date=sd,end_date=ed)
    portval=oportval/oportval.ix[0]
    nprices=prices/prices.ix[0]
    ax=portval.plot()
    nprices.plot(ax=ax)
    plt.show()
    print portval.ix[-1,:]/portval.ix[0,:].values-1
def test_code2(verb = True):
    #st=dt.datetime.now()
    # instantiate the strategy learner
    

    # set parameters for training the learner
    #sym = "ML4T-220"
    #sym = "IBM"
    #sym="UNH"
    sym="AAPL"
    #sym="GOOG"
    #sym="SINE_FAST_NOISE"
    #sym="DIS"

    stdate =dt.datetime(2006,1,1)
    for i in range(10):
        learner = sl.StrategyLearner(verbose = verb)
        enddate=stdate+dt.timedelta(300)
        learner.addEvidence(symbol = sym, sd = stdate, \
        ed = enddate, sv = 100000) 
        stdate=stdate+dt.timedelta(301)
        enddate=stdate+dt.timedelta(30)
        syms=[sym]
        dates = pd.date_range(stdate, enddate)
        prices_all = ut.get_data(syms, dates)  # automatically adds SPY
        prices = prices_all[syms]
        df_trades = learner.testPolicy(symbol = sym, sd = stdate, \
        ed = enddate, sv = 100000)
        simulate(sym,df_trades,stdate,enddate,prices) 
        stdate=enddate-dt.timedelta(250)
    
    

if __name__=="__main__":
    
    test_code(verb = False)
