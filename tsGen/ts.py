# -*- coding: utf-8 -*-
"""
Created on Tue Apr 24 22:52:21 2018

@author: roozbeh
"""
#%%
import itertools
import numpy as np
import pandas as pd

from .temporal import TemporalTemplate
from .catsamplers import CategoriesSampler
from .samplers import Sampler
from .factory import Factory

class realisation:
    def __init__(self,
                 temporalsFunc,
                 samplersFunc):
        self.temporalsFunc = temporalsFunc
        self.samplersFunc = samplersFunc
        
    def __enter__(self):
        self.factory = Factory(self.temporalsFunc(),
                               self.samplersFunc())
        
        return self.factory.create()
    
    def __exit__(self, *args):
        return
    
class ensemble:
    def __init__(self,
                 temporalsFunc,
                 samplersFunc,
                 labelFunc,
                 params):
        self.temporalsFunc = temporalsFunc
        self.samplersFunc = samplersFunc
        self.labelFunc = labelFunc
        self.params = params
        
    def __enter__(self):
        params = self.params.items()
        paramNames =  [l[0] for l in params]
        result = pd.DataFrame(columns=['id','value','target'])
        for idx,p in enumerate(itertools.product(*[l[1] for l in params])):
           param_comb = dict(zip(paramNames,p))
           f = Factory(self.temporalsFunc(**param_comb),
                       self.samplersFunc(**param_comb))            
           series = f.create()
           s = series.to_frame(name='value')
           s['id'] = str(idx+1)
           s['target'] = self.labelFunc(series,**param_comb)
           result = pd.concat([result,s])
        return result
    
    def __exit__(self, *args):
        return    
    