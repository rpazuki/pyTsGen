# -*- coding: utf-8 -*-
"""
Created on Sun Apr 22 21:39:02 2018

@author: roozbeh
"""

#%%

class FunctionSampler(Sampler):
    
    def __init__(self,func):
        Sampler.__init__(self)
        if(not callable(func)):
            raise ValueError('func argument is not callable')
            
        self.func = func
        
    def __call__(self,idx,x,tick):        
        return self.func(idx,x,tick)