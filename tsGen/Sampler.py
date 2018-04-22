# -*- coding: utf-8 -*-
"""
Created on Sun Apr 22 17:35:02 2018

@author: roozbeh
"""
#%%

class Sampler:
    samplers = None
    def __init__(self, *samplers):
        
        if(len(samplers) == 0):
            self.samplers = None
        else:
            self.samplers = []
            for s in samplers:
                self.samplers.append(s)
            #print(self.samplers)
    
    def __call__(self,idx,x,tick):
        if(self.samplers is None):
            pass
        else:
            r = 0.0
            for s in self.samplers:
                r += s(idx,x,tick)
            return r    
    
    def __add__(self,other):
        if(isinstance(other,Sampler)):
            if(self.samplers is None and other.samplers is None):
                return  Sampler(*[self,other])           
            elif(self.samplers is None):
                return  Sampler(self,*other.samplers)
            elif(other.samplers is None):
                return  Sampler(other,*self.samplers)
            else:                
                ss = self.samplers[:]
                for s in other.samplers:
                    ss.append(s)
                    
                return  Sampler(*ss)
        else:
            raise ValueError('The provided type cannot be added to Sampler.')