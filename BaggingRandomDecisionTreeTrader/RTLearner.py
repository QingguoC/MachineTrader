# -*- coding: utf-8 -*-
"""
Created on Sun Jan 29 15:00:20 2017

"""

"""
 Implement RTLearner  
"""

import numpy as np

class RTLearner(object):

    def __init__(self, leaf_size = 5, verbose = False):
        self.leaf_size=leaf_size
        self.verbose=verbose
    
        
    def author(self):
        return 'qchen325'
        
    def addEvidence(self,dataX,dataY):
        """
        @summary: Add training data to learner
        @param dataX: X values of data to add
        @param dataY: the Y training values
        """
        self.tree=self.build_tree(dataX,dataY)
        
        
        
        
    def build_tree(self,dataX,dataY):
        if dataX.shape[0] <= self.leaf_size: 
            #votes for classification
            return np.array([-1,max(dataY.tolist(),key=dataY.tolist().count),np.nan,np.nan])
        if np.all(dataY[:]==dataY[0]): 
            return np.array([-1,dataY[0],np.nan,np.nan])
        index=np.random.randint(0,dataX.shape[1])
        random_two=np.random.choice(dataX.shape[0],2,replace=False)
        i=0
        while(dataX[random_two[0],index]==dataX[random_two[1],index] and i<10):
            index=np.random.randint(0,dataX.shape[1])
            random_two=np.random.choice(dataX.shape[0],2,replace=False)
            i=i+1
        if dataX[random_two[0],index]==dataX[random_two[1],index]:
            #votes for classification
            return np.array([-1,max(dataY.tolist(),key=dataY.tolist().count),np.nan,np.nan]) 
        
        split_value=np.mean(dataX[random_two,index])
        ldataX,ldataY,rdataX,rdataY = self.split_Data(dataX,dataY,index,split_value)
        
        ltree=self.build_tree(ldataX,ldataY)
        rtree=self.build_tree(rdataX,rdataY)
        if ltree.ndim==1:
            root=np.array([index,split_value,1,2])
        else:
            root=np.array([index,split_value,1,ltree.shape[0]+1])
        tree=np.vstack((root,ltree,rtree))
                                             
        return tree
    def split_Data(self,dataX,dataY,index,split_value):
        left=dataX[:,index]<=split_value
        right=dataX[:,index]>split_value
        ldataX=dataX[left,:]
        ldataY=dataY[left]
        rdataX=dataX[right,:]
        rdataY=dataY[right]
        return ldataX,ldataY,rdataX,rdataY
    def query(self,points):
        """
        @summary: Estimate a set of test points given the model we built.
        @param points: should be a numpy array with each row corresponding to a specific query.
        @returns the estimated values according to the saved model.
        """
        res=[]
        start=int(self.tree[0,0])
        tree_height=self.tree.shape[0]
        for point in points:
            index=start
            i=0
            while(i<tree_height):
                index=self.tree[i,0]
                if index==-1:
                    break
                else:
                    index=int(index)
                if point[index] <= self.tree[i,1]:
                    i = i + 1
                    
                else:
                    i = i + int(self.tree[i,3])
                
            if index==-1:
                res.append(self.tree[i,1])
            else:
                res.append(np.nan)
        return np.array(res)
if __name__=="__main__":
    print "the secret clue is 'zzyzx'"
