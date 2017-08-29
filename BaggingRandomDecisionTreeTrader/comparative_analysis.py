# -*- coding: utf-8 -*-
"""
Created on Sat Apr  8 20:35:28 2017

@author: GuoFang
"""

import pandas as pd
import numpy as np

from rule_based import rule_based,benchmark_portforlio
from marketsim import compute_portvals,compute_portfolio_stats
from ML_based import ML_based

def performance_comparative_analysis():
    #summary lists of cr
    crs_ML_insample=[]
    crs_Rule_insample=[]
    crs_benchmark_insample=[]
    crs_ML_outsample=[]
    crs_Rule_outsample=[]
    crs_benchmark_outsample=[]
    #summary lists of sharpe ratio
    srs_ML_insample=[]
    srs_Rule_insample=[]
    srs_benchmark_insample=[]
    srs_ML_outsample=[]
    srs_Rule_outsample=[]
    srs_benchmark_outsample=[]
    
    #average performance from 20 times runs
    for i in range(20):
        print "start iteration",i+1
        ML_based(expected_up=0.7,expected_down=0.7,symbols=["AAPL"],plot=False,bags=200,leaf_size=5)
        portvals = compute_portvals(orders_file = "./orders_ml.csv", start_val = 100000)
        cr, adr, sddr, sr=compute_portfolio_stats(portvals)
        crs_ML_insample.append(cr.values[0])
        srs_ML_insample.append(sr.values[0])
        
        
        
        portvals_test = compute_portvals(orders_file = "./orders_ml_test.csv", start_val = 100000,start_date="2010-01-01",end_date="2011-12-31")
        cr_test, adr_test, sddr_test, sr_test=compute_portfolio_stats(portvals_test)
        crs_ML_outsample.append(cr_test.values[0])
        srs_ML_outsample.append(sr_test.values[0])        

        
        rule_based(symbols=["AAPL"],plot=False)
        rule_portvals=compute_portvals(orders_file="./orders_rule.csv",start_val=100000)
        cr_rule, adr_rule, sddr_rule, sr_rule=compute_portfolio_stats(rule_portvals)
        crs_Rule_insample.append(cr_rule.values[0])
        srs_Rule_insample.append(sr_rule.values[0])        

        rule_test_portvals=compute_portvals(orders_file="./orders_rule_test.csv",start_val=100000,start_date="2010-01-01",end_date="2011-12-31")
        cr_rule_test, adr_rule_test, sddr_rule_test, sr_rule_test=compute_portfolio_stats(rule_test_portvals)
        crs_Rule_outsample.append(cr_rule_test.values[0])
        srs_Rule_outsample.append(sr_rule_test.values[0])         

        
        bm_portforlio=benchmark_portforlio(symbol="AAPL",date="2008-01-02",shares=200,start_val = 100000,
                         start_date="2008-01-01",end_date="2009-12-31",filename="benchmark_orders")
        cr_bm, adr_bm, sddr_bm, sr_bm=compute_portfolio_stats(bm_portforlio)
        crs_benchmark_insample.append(cr_bm.values[0])
        srs_benchmark_insample.append(sr_bm.values[0])   

        
        bm_test_portforlio=benchmark_portforlio(symbol="AAPL",date="2010-01-04",shares=200,start_val = 100000,
                         start_date="2010-01-01",end_date="2011-12-31",filename="benchmark_orders_test")
        cr_bm_test, adr_bm_test, sddr_bm_test, sr_bm_test=compute_portfolio_stats(bm_test_portforlio)
        crs_benchmark_outsample.append(cr_bm_test.values[0])
        srs_benchmark_outsample.append(sr_bm_test.values[0])           
    
        
    type=["Benchmark in sample","Rule_based in sample","ML in sample","Benchmark out of sample","Rule_based out of sample","ML out of sample"]
    mean_cr=[np.mean(crs_benchmark_insample),np.mean(crs_Rule_insample),np.mean(crs_ML_insample),np.mean(crs_benchmark_outsample),np.mean(crs_Rule_outsample),np.mean(crs_ML_outsample)]
    std_cr=[np.std(crs_benchmark_insample),np.std(crs_Rule_insample),np.std(crs_ML_insample),np.std(crs_benchmark_outsample),np.std(crs_Rule_outsample),np.std(crs_ML_outsample)]
    tms_cr=np.column_stack((type,mean_cr,std_cr))    
    pfdf_cr=pd.DataFrame(tms_cr,columns=["type","mean of Cumulative Return","std of Cumulative Return"])
    print 
    print "Performance Table by Cumulative Return"
    print
    print pfdf_cr
    pfdf_cr.to_csv("inandoutsample_performance_cr.csv")
    
    mean_sr=[np.mean(srs_benchmark_insample),np.mean(srs_Rule_insample),np.mean(srs_ML_insample),np.mean(srs_benchmark_outsample),np.mean(srs_Rule_outsample),np.mean(srs_ML_outsample)]
    std_sr=[np.std(srs_benchmark_insample),np.std(srs_Rule_insample),np.std(srs_ML_insample),np.std(srs_benchmark_outsample),np.std(srs_Rule_outsample),np.std(srs_ML_outsample)]
    tms_sr=np.column_stack((type,mean_sr,std_sr))    
    pfdf_sr=pd.DataFrame(tms_sr,columns=["type","mean of Sharpe ratio","std of Sharpe ratio"])
    print 
    print "Performance Table by Sharpe Ratio"
    print
    print pfdf_sr
    pfdf_sr.to_csv("inandoutsample_performance_sr.csv")
    
if __name__ == "__main__":
    
    #summarize average performance of ML reference to rule based and benchmark
    performance_comparative_analysis()