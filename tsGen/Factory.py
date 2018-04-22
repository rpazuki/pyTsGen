# -*- coding: utf-8 -*-
"""
Created on Sun Apr 22 17:41:54 2018

@author: roozbeh
"""
#%%
import numpy as np
import pandas as pd

class Factory:
    def __init__(self,temporal,sampler):
        self.temporal = temporal
        self.sampler = sampler
        
    def create(self):
        data = np.zeros((self.temporal.length,),dtype=float)
        
        for idx,tick in enumerate(self.temporal):
            data[idx] = self.sampler(idx,tick)
            
        return pd.Series(data,index=self.temporal.ticks)
            