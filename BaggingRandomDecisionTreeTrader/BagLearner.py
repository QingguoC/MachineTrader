# -*- coding: utf-8 -*-
"""
Created on Sun Jan 29 15:00:20 2017

"""

"""
 Implement BagLearner  
"""

import numpy as np

class BagLearner(object):

    def __init__(self, learner , kwargs = {}, bags = 20, boost = False, verbose = False):
        
        self.verbose=verbose
        self.bags=bags
        self.boost=boost
        
        
        self.learners = []
        for i in range(self.bags):
            self.learners.append(learner(**kwargs))
    def addEvidence(self,dataX,dataY):
        """
        @summary: Add training data to learner
        @param dataX: X values of data to add
        @param dataY: the Y training values
        """
        
        bagsize=dataX.shape[0]
                
        if self.boost:
            weight=np.ones(bagsize)/float(bagsize)
            for bag in range(self.bags):
                
                selected=np.random.choice(bagsize,size=bagsize,p=weight)
                self.learners[bag].addEvidence(dataX[selected],dataY[selected])
                #self.forest.append(learners[bag].tree)
                predY=self.query(dataX)
                error=np.square(predY-dataY)
                error_rate=error/float(np.sum(error))
                if self.verbose==True:
                    print 'bag', bag
                    #print 'weight', weight
                    print 'error', np.sum(error)
                #weight=np.ones(bagsize)/float(bagsize)
                weight=weight/2+error_rate/2
        else:
            for learner in self.learners:
                selected=np.random.randint(0,bagsize,size=bagsize)
                learner.addEvidence(dataX[selected],dataY[selected])
                
            
        
        
    def query(self,points):
        if self.bags==1:
            return self.learners[0].query(points)
        res=[]
        for learner in self.learners:
            res_one=learner.query(points)
            res.append(res_one)
        res=np.array(res)
        count_res=[]
        for i in range(res.shape[1]):
            temp=res[:,i].tolist()
            #votes for classification
            count_res.append(max(temp,key=temp.count))
        return np.array(count_res)
                    
    
        
if __name__=="__main__":
    print "the secret clue is 'zzyzx'"
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 02 19:36:05 2017

@author: Administrator
"""

