# -*- coding: utf-8 -*-
"""
Created on Sat Apr  8 23:20:38 2017

@author: GuoFang
"""

from rule_based import rule_based
from ML_based import ML_based

if __name__ == "__main__":
    #make plots for part 5 to plot three plots of two normalized indicators 
    rule_based(symbols=["AAPL"],plot=True)
    ML_based(expected_up=0.8,expected_down=0.8,symbols=["AAPL"],bags=200,leaf_size=5,plot=True)
    
    print 
    print "Fig 9 to 11 were saved."