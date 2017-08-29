# -*- coding: utf-8 -*-
"""
Created on Sun Apr  2 15:09:12 2017

@author: QChen325
"""

import pandas as pd
from util import get_data
from rule_based import simulate_orders

def bestPossibleStrategy(symbols=["AAPL"],
                         dates=pd.date_range("2008-01-01","2009-12-31"),
                        sharelimit=200):
                             
    price=get_data(symbols,dates)
    order_list=[]
    curr_holding=0
    for i in range(len(price)-1):
        if price.ix[i,symbols[0]]==price.ix[i+1,symbols[0]]:
            continue
        #price will decrease
        elif price.ix[i,symbols[0]]>price.ix[i+1,symbols[0]]:
            if curr_holding == 0:
                curr_holding = -sharelimit
                order_list.append([price.index[i].date(),symbols[0],"SELL",sharelimit])
            elif curr_holding > 0:
                curr_holding = -sharelimit
                order_list.append([price.index[i].date(),symbols[0],"SELL",sharelimit])
                order_list.append([price.index[i].date(),symbols[0],"SELL",sharelimit])
            else:
                continue
        else:#price will increase
            if curr_holding == 0:
                curr_holding = sharelimit
                order_list.append([price.index[i].date(),symbols[0],"BUY",sharelimit])
            elif curr_holding > 0:
                continue
            else:
                curr_holding = sharelimit
                order_list.append([price.index[i].date(),symbols[0],"BUY",sharelimit])
                order_list.append([price.index[i].date(),symbols[0],"BUY",sharelimit])
    ordersdf = pd.DataFrame(order_list,columns=["Date","Symbol","Order","Shares"])
    ordersdf.to_csv("./orders_bestpossiblestrategy.csv",index=False)  

    
if __name__ == "__main__":
    #part 2
    bestPossibleStrategy()
    simulate_orders(symbols=["AAPL"],orders_files=["./orders_bestpossiblestrategy.csv"],
                    labels=["Best possible strategy","benchmark"],strategy=["Best possible strategy"],
                    legend_loc="upper left",
                    title="Fig.6 Best possible strategy vs Benchmark",entry_line=-1,savefig="Fig6.png")
                    
    print 
    print "Fig 6 was saved."
            
                                     
    



