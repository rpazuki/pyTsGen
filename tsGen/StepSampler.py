# -*- coding: utf-8 -*-
"""
Created on Sun Apr 22 19:42:05 2018

@author: roozbeh
"""

#%%
import numpy as np
class StepSampler(Sampler):
    
    def __init__(self,steps,probs=None):
        Sampler.__init__(self)
        self.steps = steps
        self.probs = probs
        
    def __call__(self,idx,x,tick):
        return np.random.choice(self.steps,size=1,p=self.probs).item()