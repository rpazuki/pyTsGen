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
        if(not isinstance(temporal,TemporalTemplate)):
            raise ValueError('The temporal argument must be of type TemporalTemplate')
            
        if(not isinstance(sampler,Sampler) and not isinstance(sampler,CategoriesSampler)):
            raise ValueError('The sampler argument must be of type Sampler or CategoriesSampler')
        self.temporal = temporal
        self.sampler = sampler
        
    def create(self):        
        if(isinstance(self.sampler,Sampler)):
            data = np.zeros((self.temporal.length,),dtype=float)
            total_delta = self.temporal[-1] - self.temporal[0]
            current_delta = np.timedelta64(0,'h')
            for idx,tick in enumerate(self.temporal[:-1]):                
                data[idx] = self.sampler(idx,current_delta/total_delta,tick)
                current_delta += self.temporal[idx+1] - tick
                
            data[-1] = self.sampler(self.temporal.length-1,1.0,self.temporal[-1])                    
                
            return pd.Series(data,index=self.temporal.ticks)
        elif(isinstance(self.sampler,CategoriesSampler)):
            data = np.zeros((self.temporal.length,),dtype=object)
            
            for idx,tick in enumerate(self.temporal):
                data[idx] = self.sampler(idx,tick)
                
            return pd.Series(data,index=self.temporal.ticks)
        