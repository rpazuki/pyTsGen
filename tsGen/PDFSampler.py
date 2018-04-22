# -*- coding: utf-8 -*-
"""
Created on Sun Apr 22 20:13:49 2018

@author: roozbeh
"""

#%%
import numpy as np
class PDFSampler(Sampler):
    
    def __init__(self,pdf):
        Sampler.__init__(self)
        self.pdf = pdf
        
    def __call__(self,idx,tick):
        return self.pdf.rvs(1).item()