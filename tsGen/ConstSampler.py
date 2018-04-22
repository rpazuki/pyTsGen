# -*- coding: utf-8 -*-
"""
Created on Sun Apr 22 17:38:01 2018

@author: roozbeh
"""
#%%
class ConstSampler(Sampler):
    
    def __init__(self,value):
        Sampler.__init__(self)
        self.value = value
        
    def __call__(self,idx,tick):
        return self.value