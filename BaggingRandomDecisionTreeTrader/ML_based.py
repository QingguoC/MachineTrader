# -*- coding: utf-8 -*-
"""
Created on Sat Apr  1 23:17:48 2017

@author: QChen325
"""

import pandas as pd
import matplotlib.pyplot as plt
plt.switch_backend('agg')
from rule_based import translate_order,simulate_orders,normalize_train_test,rule_based
import RTLearner as rt
import BagLearner as bl


#function to run ML strategy and create order file
def ML_based(symbols=["AAPL"],train_dates=pd.date_range("2008-01-01","2009-12-31"),
                         test_dates=pd.date_range("2010-01-01","2011-12-31"),sma_window=20,momentum_window=7,MFI_window=14,
                         expected_up=1,expected_down=1,holddays=21,sharelimit=200,plot=True,bags=200,leaf_size=5):
    #normalized indicators of in sample and out of sample periods
    trainX,trainY,trainDate,testX,testY,testDate=normalize_train_test(symbols,train_dates,test_dates,sma_window,
                         momentum_window,MFI_window,expected_up,expected_down,holddays)
    
    #make scatter plot for two indicators with data for ML
    if plot:
        twoindict1=trainX[trainY==1,:]
        twoindictN1=trainX[trainY==-1,:]
        twoindict0=trainX[trainY==0,:]
        
        plt.scatter(twoindict1[:,0],twoindict1[:,3],color="g",label="Long",alpha=0.5)
        plt.scatter(twoindictN1[:,0],twoindictN1[:,3],color="r",label="Short",alpha=0.5)
        plt.scatter(twoindict0[:,0],twoindict0[:,3],color="black",label="Nothing",alpha=0.2)
        plt.xlabel("Normalized momentum")
        plt.ylabel("Normalized MFI")
        plt.legend(loc="upper left")
        plt.xlim([-1.5,1.5])
        plt.ylim([-1.5,1.5])    
        plt.title("Fig.10 Normalized momentum and Normalized MFI\nbefore ML training")
        plt.savefig("Fig10.png")
        plt.close()
    #build Bagging random forest
    bagLearner=bl.BagLearner(learner=rt.RTLearner,bags=bags,kwargs={"leaf_size":leaf_size})
    bagLearner.addEvidence(trainX,trainY)
    
    #get signal list
    pred_orders=bagLearner.query(trainX)
    

    orders=pd.DataFrame(data=pred_orders,index=trainDate,columns=symbols)
    
    #make scatter plot for two indicators based on ML
    if plot:
        ttwoindict1=trainX[pred_orders==1,:]
        ttwoindictN1=trainX[pred_orders==-1,:]
        ttwoindict0=trainX[pred_orders==0,:]
        
        plt.scatter(ttwoindict1[:,0],ttwoindict1[:,3],color="g",label="Long",alpha=0.5)
        plt.scatter(ttwoindictN1[:,0],ttwoindictN1[:,3],color="r",label="Short",alpha=0.5)
        plt.scatter(ttwoindict0[:,0],ttwoindict0[:,3],color="black",label="Nothing",alpha=0.2)
        plt.xlabel("Normalized momentum")
        plt.ylabel("Normalized MFI")
        plt.xlim([-1.5,1.5])
        plt.ylim([-1.5,1.5]) 
        plt.legend(loc="upper left")
        plt.title("Fig.11 Normalized momentum and Normalized MFI\nafter ML training")
        plt.savefig("Fig11.png")
        plt.close()
    
    #translate signal list to order file for in sample period
    orders_list=translate_order(orders,symbols,holdlimit=holddays,sharelimit=sharelimit)
    ordersdf = pd.DataFrame(orders_list,columns=["Date","Symbol","Order","Shares"])
    ordersdf.to_csv("./orders_ml.csv",index=False)
    
    #get signal list
    testpred_orders=bagLearner.query(testX)
    #translate signal list to order file for out of sample period

    testorders=pd.DataFrame(data=testpred_orders,index=testDate,columns=symbols)    
    testorders_list=translate_order(testorders,symbols,holdlimit=holddays,sharelimit=sharelimit)
    testordersdf = pd.DataFrame(testorders_list,columns=["Date","Symbol","Order","Shares"])
    testordersdf.to_csv("./orders_ml_test.csv",index=False)
                       

    
    
    
if __name__ == "__main__":

    rule_based(symbols=["AAPL"],plot=False)    
    #part 4
    print
    print "*************** ML based Part ****************"   
    
    ML_based(expected_up=0.7,expected_down=0.7,symbols=["AAPL"],bags=200,leaf_size=5,plot=False)
    
    simulate_orders(symbols=["AAPL"],orders_files = ["./orders_rule.csv","./orders_ml.csv"], start_val = 100000,
                    labels=["Manual rule based","benchmark","ML based"],strategy=["Manual rule based","ML based"],
                    start_date="2008-01-01",end_date="2009-12-31",benchmark=True,
                    benchmark_date="2008-01-02",bm_filename="benchmark_orders",two_strategy=True,
                    legend_loc="upper left",title="Fig.8 Manual rule based vs benchmark vs ML based strategy\nduring in sample period",
                    entry_line=1,savefig="Fig8.png")

    #part 6    
    print
    print "*************** Part 6 Out sample period ****************"     

    simulate_orders(symbols=["AAPL"],orders_files = ["./orders_rule_test.csv","./orders_ml_test.csv"], start_val = 100000,
                labels=["Manual rule based","benchmark","ML based"],strategy=["Manual rule based","ML based"],
                start_date="2010-01-01",end_date="2011-12-31",benchmark=True,
                benchmark_date="2010-01-04",bm_filename="benchmark_orders_test",two_strategy=True,
                legend_loc="upper left",title="Fig.12 Manual rule based vs benchmark vs ML based strategy\nduring out of sample period",
                entry_line=-1,savefig="Fig12.png")
                
                
    print 
    print "Fig 8 and Fig 12 were saved."
    
