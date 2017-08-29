# -*- coding: utf-8 -*-
"""
Created on Fri Apr  7 23:06:35 2017

@author: GuoFang
"""
import pandas as pd
import numpy as np

from marketsim import compute_portvals
from ML_based import ML_based

#function to tweak YBuy/Ysell, number of bags and leaf size to find better performance over in sample
def findbestparameter():
    
    #find best Ybuy/Ysell
    print
    print "tweaking Ybuy/Ysell"
    pool= np.array(range(1,12))*0.1
    performance=[]
    for ratio_to_median in pool:
        crs=[]
        for i in range(20):
            ML_based(expected_up=ratio_to_median,expected_down=ratio_to_median,symbols=["AAPL"],plot=False,bags=50)
            portvals = compute_portvals(orders_file = "./orders_ml.csv", start_val = 100000)
            cr=portvals.ix[-1,:]/portvals.ix[0,:]-1
            crs.append(cr)
        performance.append([ratio_to_median,np.mean(crs),np.std(crs)])
        print ratio_to_median,"done"
    
    rmpfdf=pd.DataFrame(performance,columns=["ratio_to_median","mean of cr","std of cr"])
    print rmpfdf
    rmpfdf.to_csv("ratio_to_median_insample_performance.csv")
    
    #find best Bag numbers
    print
    print "tweaking Bag numbsers"
    performance=[]
    for bags in [50,100,200,400]:
        crs=[]
        for i in range(10):
            ML_based(expected_up=0.7,expected_down=0.7,symbols=["AAPL"],plot=False,bags=bags)
            portvals = compute_portvals(orders_file = "./orders_ml.csv", start_val = 100000)
            cr=portvals.ix[-1,:]/portvals.ix[0,:]-1
            crs.append(cr)
        performance.append([bags,np.mean(crs),np.std(crs)])
        print bags,"bags done"
    
    bgpfdf=pd.DataFrame(performance,columns=["Number of bags","mean of cr","std of cr"])
    print bgpfdf
    bgpfdf.to_csv("bags_insample_performance.csv")    
    
    #find best leaf_size
    print "tweaking leaf size"
    performance=[]
    for leaf_size in range(5,10):
        crs=[]
        for i in range(10):
            ML_based(expected_up=0.7,expected_down=0.7,symbols=["AAPL"],plot=False,bags=200,leaf_size=leaf_size)
            portvals = compute_portvals(orders_file = "./orders_ml.csv", start_val = 100000)
            cr=portvals.ix[-1,:]/portvals.ix[0,:]-1
            crs.append(cr)
        performance.append([leaf_size,np.mean(crs),np.std(crs)])
        print leaf_size,"leaf size done"
    
    bgpfdf=pd.DataFrame(performance,columns=["leaf_size","mean of cr","std of cr"])
    print bgpfdf
    bgpfdf.to_csv("leaf_size_insample_performance.csv")        


    
if __name__ == "__main__":
    
    findbestparameter()

