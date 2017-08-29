

import numpy as np
import random as rand

class QLearner(object):

    def __init__(self, \
        num_states=100, \
        num_actions = 4, \
        alpha = 0.2, \
        gamma = 0.9, \
        rar = 0.5, \
        radr = 0.99, \
        dyna = 0, \
        verbose = False):

        self.verbose = verbose
        self.num_actions = num_actions
        self.num_states=num_states
        self.s = 0
        self.a = 0
        self.Q=None
        self.alpha=alpha
        self.gamma=gamma
        self.rar=rar
        self.radr=radr
        self.dyna=dyna
        self.num_query=0
        
        #self.dyna_a=[]
        if dyna>0:
            #self.Tc=np.ones([num_states,num_actions,num_states])/10000.0
            #self.R=np.zeros([num_states,num_actions])
            self.dyna_sasr=[]

    def author(self):
        return 'Qingguo'
        
    def querysetstate(self, s):
        """
        @summary: Update the state without updating the Q-table
        @param s: The new state
        @returns: The selected action
        """
        self.s = s
        if self.Q is None:
            action = rand.randint(0, self.num_actions-1)
            #self.Q=np.random.uniform(-1,1,size=[self.num_states,self.num_actions])
            self.Q=np.zeros([self.num_states,self.num_actions])
        else:
            action=self.Q.argmax(axis=1)[s]
        self.a=action
        if self.verbose: print "s =", s,"a =",action
        return action

    def query(self,s_prime,r):
        """
        @summary: Update the Q table and return an action
        @param s_prime: The new state
        @param r: The ne state
        @returns: The selected action
        
        """
        if self.dyna==0:
            if rand.uniform(0.0, 1.0) <= self.rar:
                
                action = rand.randint(0, self.num_actions-1)
            else:
                action=self.Q.argmax(axis=1)[s_prime]
            self.rar=self.rar*self.radr
            self.Q[self.s,self.a]=(1-self.alpha)*self.Q[self.s,self.a]+self.alpha*(r+self.gamma*self.Q[s_prime,action])
            self.s=s_prime
            self.a=action
            
            if self.verbose: print "s =", s_prime,"a =",action,"r =",r
            
            return action
        else:

            if self.num_query < self.num_actions*self.num_states*10:
                self.num_query += 1
                if rand.uniform(0.0, 1.0) <= self.rar:
                    action = rand.randint(0, self.num_actions-1)
                else:
                    action=self.Q.argmax(axis=1)[s_prime]
                self.rar=self.rar*self.radr
                self.Q[self.s,self.a]=(1-self.alpha)*self.Q[self.s,self.a]+self.alpha*(r+self.gamma*self.Q[s_prime,action])

                self.dyna_sasr.append([self.s,self.a,s_prime,r])

                    
                self.s=s_prime
                self.a=action
                
                if self.verbose: print "s =", s_prime,"a =",action,"r =",r
                
                return action
           
            else:
 
                for i in range(self.dyna):
                    #print i
                    s,a,s_p,ri=rand.choice(self.dyna_sasr)

                    self.Q[s,a]=(1-self.alpha)*self.Q[s,a]+self.alpha*(ri+self.gamma*self.Q[s_p,:].max())
                #print self.Q
                if rand.uniform(0.0, 1.0) <= self.rar:
                    
                    action = rand.randint(0, self.num_actions-1)
                else:
                    action=self.Q.argmax(axis=1)[s_prime]
                self.rar=self.rar*self.radr
                self.Q[self.s,self.a]=(1-self.alpha)*self.Q[self.s,self.a]+self.alpha*(r+self.gamma*self.Q[s_prime,action])
                self.s=s_prime
                self.a=action
                
                if self.verbose: print "s =", s_prime,"a =",action,"r =",r
                
                return action                    
            


if __name__=="__main__":
    print "Remember Q from Star Trek? Well, this isn't him"
