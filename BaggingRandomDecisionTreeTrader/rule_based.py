# -*- coding: utf-8 -*-
"""
Created on Sat Apr  1 15:45:07 2017

@author: QChen325
"""
import datetime as dt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.switch_backend('agg')
from indicators import get_indicators,normalize_indicator
from marketsim import compute_portvals,compute_portfolio_stats

#function to prepare normalized indicators and Y labels over in sample and out of sample period
def normalize_train_test(symbols=["AAPL"],train_dates=pd.date_range("2008-01-01","2009-12-31"),
                         test_dates=pd.date_range("2010-01-01","2011-12-31"),sma_window=20,
                         momentum_window=7,MFI_window=14,expected_up=1,expected_down=1,holddays=21):
    
    price,sma,price_sma_ratio,bollinger_value,bb_upper,bb_lower,mfi,momentum=get_indicators(symbols,train_dates,sma_window,MFI_window,momentum_window)
    

    norm_mfi,nmfim,nmfisd=normalize_indicator(mfi[symbols])
    norm_bbp,nbbpm,nbbpsd=normalize_indicator(bollinger_value[symbols])
    norm_psr,npsrm,npsrsd=normalize_indicator(price_sma_ratio[symbols])
    norm_spymfi,nspymfim,nspymfisd=normalize_indicator(mfi["SPY"])    
    norm_momentum,nmomentumm,nmomentumsd=normalize_indicator(momentum[symbols])
    #calculate 21 day return
    period_return=price.copy()
    period_return.ix[:-holddays,:]=price.ix[holddays:,:].values/price.ix[:-holddays,:]-1
    period_return.ix[-holddays:,:]=0
    
    #calculate median changes in either direction
    pos=period_return[period_return>0]
    neg=period_return[period_return<0]
    
    median_pos_period_resturn=pos[symbols].median()
    median_neg_period_resturn=neg[symbols].median()
    #translate Y labels from 21 day return
    labelY=pd.DataFrame(data=0,index=price.index,columns=price.columns)
    labelY[period_return>=median_pos_period_resturn*expected_up]=1
    labelY[period_return<=median_neg_period_resturn*expected_down]=-1
    
    del labelY["SPY"]
    
    trainXY=np.column_stack((norm_momentum,norm_bbp,norm_psr,norm_mfi,norm_spymfi,labelY))
    
    trainXY=pd.DataFrame(trainXY,index=labelY.index)
    trainXY=trainXY.dropna()
    trainDate=trainXY.index
    trainXY=np.array(trainXY)
    trainX=trainXY[:,:-1]
    trainY=trainXY[:,-1]
    

    
    testprice,testsma,testprice_sma_ratio,testbollinger_value,testbb_upper,testbb_lower,testmfi,testmomentum=get_indicators(symbols,test_dates,sma_window,MFI_window)
    
    norm_testmfi=(testmfi[symbols]-nmfim[symbols])/nmfisd[symbols]
    norm_testbbp=(testbollinger_value[symbols]-nbbpm[symbols])/nbbpsd[symbols]
    norm_testpsr=(testprice_sma_ratio[symbols]-npsrm[symbols])/npsrsd[symbols]
    norm_testspymfi=(testmfi["SPY"]-nspymfim)/nspymfisd
    norm_testmomentum=(testmomentum[symbols]-nmomentumm)/nmomentumsd

    #calculate 21 day return
    testperiod_return=testprice.copy()
    testperiod_return.ix[:-holddays,:]=testprice.ix[holddays:,:].values/testprice.ix[:-holddays,:]-1
    testperiod_return.ix[-holddays:,:]=0
    
    #translate Y labels from 21 day return
    testlabelY=pd.DataFrame(data=0,index=testprice.index,columns=testprice.columns)
    testlabelY[testperiod_return>=median_pos_period_resturn*expected_up]=1
    testlabelY[testperiod_return<=median_neg_period_resturn*expected_down]=-1
    del testlabelY["SPY"]
    
    
    testXY=np.column_stack((norm_testmomentum,norm_testbbp,norm_testpsr,norm_testmfi,norm_testspymfi,testlabelY))
    testXY=pd.DataFrame(testXY,index=testlabelY.index)
    testXY=testXY.dropna()
    testDate=testXY.index
    testXY=np.array(testXY)    

    testX=testXY[:,:-1]
    testY=testXY[:,-1]

    
    return trainX,trainY,trainDate,testX,testY,testDate
    
#turn manual rule strategy to a signal list
def rule_strategy(trainX):
    

    
    norm_momentum=trainX[:,0]
    norm_bbp=trainX[:,1]
    norm_psr=trainX[:,2]
    norm_mfi=trainX[:,3]
    norm_spymfi=trainX[:,4]
    
    orders=trainX[:,0].copy()
    orders[:]=0
    orders[((norm_momentum<0)& (norm_bbp<0)&(norm_bbp>-1.8)&(norm_psr<0)&(norm_mfi<0)&(norm_mfi>-0.9)&(norm_spymfi<1.5))| ((norm_momentum>0)& (norm_bbp>1.8)&(norm_mfi>0.9)&(norm_spymfi<1.5)&(norm_psr>0))]=-1
    orders[((norm_momentum>0)& (norm_bbp>0)& (norm_bbp<1.8)&(norm_psr>0)&(norm_mfi>0)&(norm_mfi<1.8)&(norm_spymfi>-1.5))|((norm_momentum<0)& (norm_bbp<-1.4)&(norm_mfi<-0.9)&(norm_spymfi>-1.5)&(norm_psr<0))]=1
    
    return orders
#make order files for both in sample and out of sample period                         
def rule_based(symbols=["AAPL"],train_dates=pd.date_range("2008-01-01","2009-12-31"),
                         test_dates=pd.date_range("2010-01-01","2011-12-31"),sma_window=20,
                         momentum_window=7,MFI_window=14,plot=False,
                         holddays=21,sharelimit=200):
    #normalized indicators of in sample and out of sample periods                         
    trainX,trainY,trainDate,testX,testY,testDate=normalize_train_test(symbols,train_dates,
                         test_dates,sma_window,momentum_window,MFI_window,holddays=holddays)

    pred_orders=rule_strategy(trainX)
    
    #make scatter plot for two indicators with rule strategy
    if plot:
        twoindict1=trainX[pred_orders==1,:]
        twoindictN1=trainX[pred_orders==-1,:]
        twoindict0=trainX[pred_orders==0,:]
        
        plt.scatter(twoindict1[:,0],twoindict1[:,3],color="g",label="Long",alpha=0.5)
        plt.scatter(twoindictN1[:,0],twoindictN1[:,3],color="r",label="Short",alpha=0.5)
        plt.scatter(twoindict0[:,0],twoindict0[:,3],color="black",label="Nothing",alpha=0.2)
        plt.xlabel("Normalized momentum")
        plt.ylabel("Normalized MFI")
        plt.xlim([-1.5,1.5])
        plt.ylim([-1.5,1.5])
        plt.legend(loc="upper left")
        plt.title("Fig.9 Normalized momentum and Normalized MFI\nin sample by rule based strategy")
        plt.savefig("Fig9.png")
        plt.close()
    
    orders=pd.DataFrame(data=pred_orders,index=trainDate,columns=symbols)
    
    orders_list=translate_order(orders,symbols,holdlimit=holddays,sharelimit=sharelimit)
        
    ordersdf = pd.DataFrame(orders_list,columns=["Date","Symbol","Order","Shares"])
    ordersdf.to_csv("./orders_rule.csv",index=False)
    
    test_pred_orders=rule_strategy(testX)
    testorders=pd.DataFrame(data=test_pred_orders,index=testDate,columns=symbols)
    
    testorders_list=translate_order(testorders,symbols,holdlimit=holddays,sharelimit=sharelimit)
        
    testordersdf = pd.DataFrame(testorders_list,columns=["Date","Symbol","Order","Shares"])
    testordersdf.to_csv("./orders_rule_test.csv",index=False)
    
    
#helper function to translate signal list to true orders by 21 day holding limit
def translate_order(orders,symbols,holdlimit=21,sharelimit=200):
    holddays=0
    holding=0
    orders_list=[]
    
    for date in orders.index:
        for symbol in symbols:
            if holding==0 and orders.ix[date,symbol]==0:
                continue
            elif holding==0 and orders.ix[date,symbol]==1:
                orders_list.append([date.date(),symbol,"BUY",sharelimit])
                holding=sharelimit
                holddays=0
            elif holding==0 and orders.ix[date,symbol]==-1:
                orders_list.append([date.date(),symbol,"SELL",sharelimit])
                holding=-sharelimit
                holddays=0
            elif holding==sharelimit and holddays<holdlimit:
                holddays+=1
    
            elif holding==sharelimit and holddays==holdlimit:
                orders_list.append([date.date(),symbol,"SELL",sharelimit])
                #orders_list.append([date.date(),symbol,"SELL",200])
                holding=0
                holddays=0
                
            elif holding==-sharelimit and holddays<holdlimit:
                holddays+=1

            elif holding==-sharelimit and holddays==holdlimit:
                #orders_list.append([date.date(),symbol,"BUY",200])
                orders_list.append([date.date(),symbol,"BUY",sharelimit])
                holding=0
                holddays=0
    return orders_list

#function to calculate portfolio for benchmark
def benchmark_portforlio(symbol,date="2008-01-02",shares=200,start_val = 100000,
                         start_date="2008-01-01",end_date="2009-12-31",filename="benchmark_orders"):
    benchmark_order=pd.DataFrame([[date,symbol,"BUY",shares]],columns=["Date","Symbol","Order","Shares"])
    benchmark_order.to_csv("./{}.csv".format(filename),index=False)
    portvals=compute_portvals("./{}.csv".format(filename), start_val,start_date=start_date,end_date=end_date)
    return portvals
#simulate portfolio based on order files and make plots   
def simulate_orders(symbols,orders_files = ["./orders_rule.csv"], start_val = 100000,
                    labels=["Manual rule based","benchmark"],strategy=["Manual rule based"],
                    start_date="2008-01-01",end_date="2009-12-31",benchmark=True,
                    benchmark_date="2008-01-02",bm_filename="benchmark_orders",two_strategy=False,
                    legend_loc="lower right",title="title",
                    entry_line=0,savefig="Fig.png"):
    
    origin_portvals=compute_portvals(orders_files[0] , start_val,start_date=start_date,end_date=end_date)
    #normalize portvals    
    portvals=origin_portvals/origin_portvals.ix[0]    
    start_date = dt.date.strftime(portvals.index[0],"%Y-%m-%d")
    end_date = dt.date.strftime(portvals.index[-1],"%Y-%m-%d")
    
    
    print "Date Range: {} to {}".format(start_date, end_date)

    cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = compute_portfolio_stats(portvals)
    print "Cumulative Return of {}: {}".format(strategy[0],cum_ret.values[0])
    print "Standard Deviation of daily return of {}: {}".format(strategy[0],std_daily_ret.values[0])
    print "Average Daily Return of {}: {}".format(strategy[0],avg_daily_ret.values[0])
    
    ax1=portvals.plot(title=title)
    
    ax1.set_ylabel("Normalized Price")
    ax1.set_xlabel("Date")
    if benchmark:
        origin_benchmark_portvals=benchmark_portforlio(symbol=symbols[0],date=benchmark_date,start_date=start_date,end_date=end_date,filename=bm_filename)
        benchmark_portvals=origin_benchmark_portvals/origin_benchmark_portvals.ix[0]
        cum_ret_BM, avg_daily_ret_BM, std_daily_ret_BM, sharpe_ratio_BM = compute_portfolio_stats(benchmark_portvals)
    
        print "Cumulative Return of Benchmark : {}".format(cum_ret_BM.values[0])
        print "Standard Deviation of daily return of Benchmark : {}".format(std_daily_ret_BM.values[0])
        print "Average Daily Return of Benchmark : {}".format(avg_daily_ret_BM.values[0])
        benchmark_portvals.plot(ax=ax1,color="black")
    if two_strategy:
        origin_portvals2=compute_portvals(orders_files[1] , start_val,start_date=start_date,end_date=end_date)
        #normalize portvals    
        portvals2=origin_portvals2/origin_portvals2.ix[0]
        cum_ret2, avg_daily_ret2, std_daily_ret2, sharpe_ratio2 = compute_portfolio_stats(portvals2)
        print "Cumulative Return of {}: {}".format(strategy[1],cum_ret2.values[0])
        print "Standard Deviation of daily return of  {}: {}".format(strategy[1],std_daily_ret2.values[0])
        print "Average Daily Return of {}: {}".format(strategy[1],avg_daily_ret2.values[0])

        portvals2.plot(ax=ax1,color="g")
    if entry_line>=0:
        ymin, ymax = ax1.get_ylim()
        orders=pd.read_csv(orders_files[entry_line])
        for i in range(0,len(orders),2):
            if orders.ix[i,"Order"]=="SELL":
                ax1.axvline(pd.to_datetime(orders.ix[i,"Date"]),ymin=0,ymax=ymax,color="r")
            else:
                ax1.axvline(pd.to_datetime(orders.ix[i,"Date"]),ymin=0,ymax=ymax,color="g")             
        
    plt.legend(loc=legend_loc,prop={'size':8},labels=labels)
    plt.savefig(savefig)
    plt.close()


if __name__ == "__main__":
    #part 3
    print "*************** Manual Rule based Part ****************"
    rule_based(symbols=["AAPL"],plot=False)
    simulate_orders(symbols=["AAPL"],entry_line=0,title="Fig.7 Manual rule based strategy vs benchmark\nduring in sample period",savefig="Fig7.png")
    
    print 
    print "Fig 7 was saved."

    
    
    
                 
    
