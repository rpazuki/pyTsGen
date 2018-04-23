# -*- coding: utf-8 -*-
"""
Created on Sun Apr 22 19:10:08 2018

@author: roozbeh
"""
#%%
import numpy as np

class CategoriesSampler:
    categories = None
    def __init__(self, categories,probs=None):        
        self.categories = categories
        self.probs = probs
    
    def __call__(self,idx,tick):
        return np.random.choice(self.categories,size=1,p=self.probs).item()
    
    def __add__(self,other):
        if(isinstance(other,Sampler)):
            pass
        else:
            raise ValueError('The provided type cannot be added to Sampler.')