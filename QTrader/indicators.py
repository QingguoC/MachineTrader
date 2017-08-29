# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 12:10:19 2017

@author: QChen325
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.switch_backend('agg')
from util import get_data


def get_indicators(symbols,dates,sma_window=20,
                  MFI_window=14,momentum_window=7):
    #load data
    df=get_data(symbols=symbols,dates=dates)
    #normalize price dataframe    
    norm_price=df/df.values[0]
    
    #price/sma and bbvalue
    
    sma=pd.rolling_mean(norm_price,window=sma_window)
    #sma=sma.fillna(method="bfill")
    sd=pd.rolling_std(norm_price,window=sma_window)
    #sd=sd.fillna(method="bfill")
    price_sma_ratio=norm_price/sma
    bollinger_value=(norm_price-sma)/(2*sd)
    bb_upper=sma+2*sd
    bb_lower=sma-2*sd
    
    
    ##money flow index
    high=get_data(symbols=symbols,dates=dates,colname="High")
    low=get_data(symbols=symbols,dates=dates,colname="Low")
    close=get_data(symbols=symbols,dates=dates,colname="Close")
    volume=get_data(symbols=symbols,dates=dates,colname="Volume")
    
    typical_price=(high+low+close)/3
    money_flow=typical_price*volume
    
    dc_tprice=typical_price.copy()
    dc_tprice.values[1:,:]=typical_price.values[1:,:]-typical_price.values[:-1,:]
    dc_tprice.values[0,:]=0
    up_flow=money_flow[dc_tprice>0].fillna(0).cumsum()
    down_flow=money_flow[dc_tprice<0].fillna(0).cumsum()    

    gain_flow=pd.DataFrame(data=0,index=df.index,columns=df.columns)
    gain_flow.values[MFI_window:,:]=up_flow.values[MFI_window:,:]-up_flow.values[:-MFI_window,:]
    loss_flow=pd.DataFrame(data=0,index=df.index,columns=df.columns)
    loss_flow.values[MFI_window:,:]=down_flow.values[MFI_window:,:]-down_flow.values[:-MFI_window,:]
    
    ms=gain_flow/loss_flow
    mfi=100-(100.0/(1+ms))
    mfi[mfi==np.Inf]=100
    
    #momentum
    momentum=pd.DataFrame(data=0,index=df.index,columns=df.columns)
    momentum.ix[momentum_window:,:]=df.ix[momentum_window:,:]/df.ix[:-momentum_window,:].values-1
    momentum.ix[0:momentum_window,:]=np.nan
    
    
    return norm_price,sma,price_sma_ratio,bollinger_value,bb_upper,bb_lower,mfi,momentum

#helper function to normalize indicators
def normalize_indicator(indicator):
    mean=indicator.mean()
    sd=indicator.std()
    scaled=(indicator-mean)/sd
    return scaled,mean,sd

#plot normalized price_sma ratio    
def plot_price_sma(price,sma,price_sma_ratio):
    ax1=price.plot(label="Normalized Price",title="Fig.1 Normalized Price/SMA ratio and historical price",alpha=0.5)
    sma.plot(ax=ax1,label="SMA",alpha=0.5)
    ax1.set_ylabel("Normalized Price")
    plt.legend(loc="lower left",prop={'size':7})
    ax2=ax1.twinx()
    price_sma_ratio.plot(ax=ax2,color='r',label="Normalized Price/SMA ratio",alpha=0.6)
    ax2.set_ylabel("Normalized Price/SMA ratio",color="r")
    plt.legend(loc="lower right",prop={'size':7})
    plt.savefig("Fig1.png")
    plt.close()

#plot normalized bollinger band    
def plot_price_bb(price,bb_upper,bb_lower,bollinger_value):  
    
    ax1=price.plot(label="Normalized Price",title="Fig.2 Normalized Bollinger band value and historical price",alpha=0.5)
    bb_upper.plot(ax=ax1,label="Normalized bollinger upper band",color="g",alpha=0.5)
    bb_lower.plot(ax=ax1,label="Normalized bollinger lower band",color="g",alpha=0.5)
    ax1.set_ylabel("Normalized Price")
    plt.legend(loc="lower left",prop={'size':7})
    ax2=ax1.twinx()
    bollinger_value.plot(ax=ax2,color='r',label="Normalized BB value",alpha=0.6)

    ax2.set_ylabel("Normalized BB value",color="r")
    plt.legend(loc="lower right",prop={'size':7})
    plt.savefig("Fig2.png")
    plt.close()
    
#plot normalized MFI    
def plot_mfi(price,mfi):

    ax1=price.plot(label="Normalized Price",title="Fig.3 Normalized MFI and historical price",alpha=0.5)
    ax1.set_ylabel("Normalized Price")
    plt.legend(loc="lower left",prop={"size":7})
    
    ax2=ax1.twinx()
    mfi.plot(ax=ax2,color='r',label="Normalized MFI",alpha=0.6)

    ax2.set_ylabel("Normalized MFI",color="r")
    plt.legend(loc="lower right",prop={"size":7})
    plt.savefig("Fig3.png") 
    plt.close()

#plot normalized SPY_MFI    
def plot_spy_mfi(price,mfi):

    ax1=price.plot(label="Normalized Price",title="Fig.4 Normalized SPY MFI and historical price",alpha=0.5)
    ax1.set_ylabel("Normalized Price")
    plt.legend(loc="lower left",prop={"size":7})
    
    ax2=ax1.twinx()
    mfi.plot(ax=ax2,color='r',label="Normalized SPY MFI",alpha=0.6)

    ax2.set_ylabel("Normalized SPY MFI",color="r")
    plt.legend(loc="lower right",prop={"size":7})
    plt.savefig("Fig4.png") 
    plt.close()  
    

#plot normalized momentum
def plot_momentum(price,momentum):
    ax1=price.plot(label="Normalized Price",title="Fig.5 Normalized Momentum and historical price",alpha=0.5)
    ax1.set_ylabel("Normalized Price")
    plt.legend(loc="lower left",prop={'size':7})
    ax2=ax1.twinx()

    momentum.plot(ax=ax2,color="r",label="Normalized momentum",alpha=0.6)
    ax2.set_ylabel("Normalized momentum",color="r")
    plt.legend(loc="lower right",prop={'size':7})
    plt.savefig("Fig5.png") 
    plt.close() 
#helper function to calculate all normalized indictors used in the study and plot them
def to_plot(symbol="AAPL",dates=pd.date_range("2008-1-1","2009-12-31")):

    price,sma,price_sma_ratio,bollinger_value,bb_upper,bb_lower,mfi,momentum=get_indicators([symbol],dates=dates)
    
    norm_price_sma_ratio,mean_price_sma_ratio,sd_price_sma_ratio= normalize_indicator(price_sma_ratio[symbol])   
    plot_price_sma(price[symbol],sma[symbol],norm_price_sma_ratio)

    norm_bbp,mean_bbp,sd_bbp= normalize_indicator(bollinger_value[symbol])
    plot_price_bb(price[symbol],bb_upper[symbol],bb_lower[symbol],norm_bbp)
    
    norm_mfi,mean_mfi,sd_mfi= normalize_indicator(mfi)
    plot_mfi(price[symbol],norm_mfi[symbol])
    plot_spy_mfi(price[symbol],norm_mfi["SPY"])
    
    norm_momentum,mean_momentum,sd_momentum= normalize_indicator(momentum[symbol])
    plot_momentum(price[symbol],norm_momentum)
    
    
if __name__ == "__main__":
    to_plot()
    print
    print "Five figures 1 to 5 were saved."
