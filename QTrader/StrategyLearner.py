
import datetime as dt
import QLearner as ql
import pandas as pd
import util as ut
import numpy as np
import random as rand

class StrategyLearner(object):

    # constructor
    def __init__(self, verbose = False):
        self.verbose = verbose
        self.holdlimit=200
    def author(self):
        return 'Qingguo'
        
    # this method should create a QLearner, and train it for trading
    def addEvidence(self, symbol = "IBM", \
        sd=dt.datetime(2008,1,1), \
        ed=dt.datetime(2009,1,1), \
        sv = 10000): 

        allprices,orgin_psr,orgin_bbp,orgin_mm,orgin_mfi,dr=self.get_indicators([symbol],pd.date_range(sd-dt.timedelta(40),ed))
        
        psr=orgin_psr.ix[sd:ed,symbol]
        bbp=orgin_bbp.ix[sd:ed,symbol]
        mfi=orgin_mfi.ix[sd:ed,symbol]
        mm=orgin_mm.ix[sd:ed,symbol]
        mfispy=orgin_mfi.ix[sd:ed,"SPY"]
        dr=dr.ix[sd:ed,symbol]
        prices=allprices.ix[sd:ed,symbol]
        
        dis_psr,psrbins=pd.qcut(psr,2,retbins=True,labels=False)
        dis_bbp,bbpbins=pd.qcut(bbp,10,retbins=True,labels=False)
        dis_mm,mmbins=pd.qcut(mm,2,retbins=True,labels=False)
        dis_mfi,mfibins=pd.qcut(mfi,4,retbins=True,labels=False)
        dis_mfispy,mfispybins=pd.qcut(mfispy,10,retbins=True,labels=False)
        
        psrbins[0]=-np.Inf
        psrbins[-1]=np.Inf
        bbpbins[0]=-np.Inf
        bbpbins[-1]=np.Inf
        mfibins[0]=-np.Inf
        mfibins[-1]=np.Inf
        mmbins[0]=-np.Inf
        mmbins[-1]=np.Inf
        mfispybins[0]=-np.Inf
        mfispybins[-1]=np.Inf
        
        
        self.psrbins=psrbins
        self.bbpbins=bbpbins
        self.mfibins=mfibins
        self.mmbins=mmbins
        self.mfispybins=mfispybins
        
        self.learner = ql.QLearner(num_states=1600,num_actions=3)
        # add your code to do learning here
        oldprofit=0
        for iteration in range(100):
            old_holding=0
            profits=0
            rewards=0
            for i in range(dr.shape[0]-1):
                
                if(i>0):
                    profits+=prices[i-1]*old_holding*self.holdlimit*dr[i]
                state=self.discretize(dis_psr[i],dis_bbp[i],dis_mm[i],dis_mfi[i],dis_mfispy[i])
                               
                if i==0:
                    action=self.learner.querysetstate(state)    
                else:
                    action=self.learner.query(state,rewards)
                holding,rewards=self.execute_action(old_holding,action,dr[i+1])

                old_holding=holding
            profits+=prices[-2]*old_holding*self.holdlimit*dr[-1] 
            if iteration > 10:
                if profits == oldprofit:
                    
                    break
            oldprofit=profits
            
            
   
    # this method should use the existing policy and test it against new data
    def testPolicy(self, symbol = "IBM", \
        sd=dt.datetime(2009,1,1), \
        ed=dt.datetime(2010,1,1), \
        sv = 10000):
        
        

        # here we build a fake set of trades
        # your code should return the same sort of data

        allprices,orgin_psr,orgin_bbp,orgin_mm,orgin_mfi,dr=self.get_indicators([symbol],pd.date_range(sd-dt.timedelta(40),ed))
        psr=orgin_psr.ix[sd:ed,symbol]
        bbp=orgin_bbp.ix[sd:ed,symbol]
        mfi=orgin_mfi.ix[sd:ed,symbol]
        mm=orgin_mm.ix[sd:ed,symbol]
        mfispy=orgin_mfi.ix[sd:ed,"SPY"]
        dr=dr.ix[sd:ed,symbol]
        prices=allprices.ix[sd:ed,symbol]

        dis_psr=pd.cut(psr,self.psrbins,labels=False)
        dis_bbp=pd.cut(bbp,self.bbpbins,labels=False)
        dis_mfi=pd.cut(mfi,self.mfibins,labels=False)
        dis_mm=pd.cut(mm,self.mmbins,labels=False)        
        dis_mfispy=pd.cut(mfispy,self.mfispybins,labels=False)
        trades=dr.copy()
        trades[:]=0
        
        old_holding=0
        profits=0
        for i in range(dr.shape[0]-1):
            
            if(i>0):
                profits+=prices[i-1]*old_holding*self.holdlimit*dr[i]
            state=self.discretize(dis_psr[i],dis_bbp[i],dis_mm[i],dis_mfi[i],dis_mfispy[i])
            
            action=self.learner.querysetstate(state)    

            holding,rewards=self.execute_action(old_holding,action,dr[i+1])
            trades[i]=(holding-old_holding)*self.holdlimit
            old_holding=holding
        profits+=prices[-2]*old_holding*self.holdlimit*dr[-1] 
        #print profits," profits"
        trades=pd.DataFrame(trades,columns=[symbol])   
        return trades

    def execute_action(self,holding,action,ret,randomrate=0):
         

        if rand.uniform(0.0, 1.0) <= randomrate: # going rogue
            action = rand.randint(0,2) # choose the random direction
        rewards=0
        if holding==-1: 
            if action <=1:
                rewards=-ret
            else:
                holding=1
                
                rewards=2*ret
        elif holding==0:
            if action==0:
                holding=-1
                rewards=-ret
            elif action==2:
                holding=1
                rewards=ret
        else:
            if action==0:
                holding=-1
               
                rewards=-2*ret
            else:
                rewards=ret
                
        return holding,rewards


    def discretize(self,x1,x2,x3,x4,x5):
        
        return x1+x2*2+x3*20+x4*40+x5*160
    def get_indicators(self,symbols,dates,sma_window=20,
                  MFI_window=14,momentum_window=10):
        #load data
        df=ut.get_data(symbols=symbols,dates=dates)
        #normalize price dataframe    
        norm_price=df/df.values[0]
        
        #price/sma and bbvalue
        
        sma=pd.rolling_mean(norm_price,window=sma_window)
        #sma=sma.fillna(method="bfill")
        sd=pd.rolling_std(norm_price,window=sma_window)
        #sd=sd.fillna(method="bfill")
        price_sma_ratio=norm_price/sma
        bollinger_value=(norm_price-sma)/(2*sd)
        
        
        ##money flow index
        high=ut.get_data(symbols=symbols,dates=dates,colname="High")
        low=ut.get_data(symbols=symbols,dates=dates,colname="Low")
        close=ut.get_data(symbols=symbols,dates=dates,colname="Close")
        volume=ut.get_data(symbols=symbols,dates=dates,colname="Volume")
        
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
        
        #daily_return
        dr=pd.DataFrame(data=0,index=df.index,columns=df.columns)
        dr.ix[1:,:]=df.ix[1:,:]/df.ix[:-1,:].values-1
        dr.ix[0:1,:]=np.nan        
        
        
        return df,price_sma_ratio,bollinger_value,momentum,mfi,dr
    
if __name__=="__main__":
    print "One does not simply think up a strategy"
