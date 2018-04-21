# -*- coding: utf-8 -*-
"""
Created on Sat Apr 21 09:57:05 2018

@author: roozbeh
"""
#%%
import numpy as np

class TemporalJitter:
    
    def __init__(self,pdf,resolution='s'):
        self.pdf = pdf
        self.res = resolution
    def __iter__(self):
        return self
    
    def throw(self, type=None, value=None, traceback=None):
        raise StopIteration
        
    def __next__(self):
        return np.timedelta64(self.nextInt(),self.res) 
    
    def next(self):
        return self.__next__()
    
    def nextInt(self):
        rv = self.pdf.rvs(1).item()
        return int(rv)
    
    def close(self):
        """Raise GeneratorExit inside generator.
        """
        try:
            self.throw(GeneratorExit)
        except (GeneratorExit, StopIteration):
            pass
        else:
            raise RuntimeError("generator ignored GeneratorExit")