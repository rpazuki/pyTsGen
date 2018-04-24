# -*- coding: utf-8 -*-
"""
Created on Sun Apr 22 17:35:02 2018

@author: roozbeh
"""
#%%
import numpy as np
from scipy.stats import norm
from numpy.fft import ihfft

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
    
    def __call__(self,params):
        if(self.samplers is None):
            pass
        else:
            r = 0.0
            for s in self.samplers:
                r += s(params)
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
            
    def __parse_delta__(self,d):
        try:
            (i,st) = d['delta'].split(' ')                
        except ValueError:
            raise ValueError('delta is in wrong format. examples: "1 s", "2 m", "3 h", "4 D"')
        
        try:
            i = int(i)            
        except ValueError:
            raise ValueError('delta is in wrong format. The first part must be an integer. examples: "1 s", "2 m", "3 h", "4 D"')
        try:
            ret = np.timedelta64(i,st)
        except TypeError:    
            raise ValueError('delta is in wrong format. The first part must be an integer. examples: "1 s", "2 m", "3 h", "4 D"')
        return ret
            
            
class Const(Sampler):
    
    def __init__(self,value):
        Sampler.__init__(self)
        self.value = value
        
    def __call__(self,params):
        return self.value

class Step(Sampler):
    
    def __init__(self,steps,probs=None):
        Sampler.__init__(self)
        self.steps = steps
        self.probs = probs
        
    def __call__(self,params):
        return np.random.choice(self.steps,size=1,p=self.probs).item()


class Function(Sampler):
    
    def __init__(self,func):
        Sampler.__init__(self)
        if(not callable(func)):
            raise ValueError('func argument is not callable')
            
        self.func = func
        
    def __call__(self,params):        
        return self.func(params)

class Periodic(Sampler):
    
    def __init__(self,period='1 h',func=lambda x: np.sin(2*np.pi*x)):
        Sampler.__init__(self)
        if(not callable(func)):
            raise ValueError('func argument is not callable')
            
        self.func = func
        self.period = Sampler.__parse_delta__(self,dict(delta=period))
        
    def __call__(self,params):
        time_elapsed = params['tick'] - params['start']
        incompelete_segment = time_elapsed/self.period - int(time_elapsed/self.period)
        return self.func(incompelete_segment)

class PDF(Sampler):
    
    def __init__(self,pdf):
        Sampler.__init__(self)
        self.pdf = pdf
        
    def __call__(self,params):
        return self.pdf.rvs(1).item()            
    
    
class AutoReg(Sampler):
    def __init__(self,coeffs,init,noise=1.0,const=0.0):        
        """
        Generate an autorehression time series plus added normal noise.
        coeffs: the phi vector for model degree n. [ph_1, ph_2, ph_3, ..., ph_n]
        init: n initial values for model degree n. [X_1, X_2, X_3, ..., X_n]
        """
        Sampler.__init__(self)        
        if(len(coeffs) != len(init)):
            raise ValueError('Coefficient length must be equal to initial values length.')
            
        self.coeffs = np.array(coeffs,dtype=float)
        self.init = np.array(init,dtype=float)
        self.degree = len(coeffs)
        self.noise = noise
        self.norm = norm(0.0,noise)
        self.const = const
        
    def __call__(self,params):
        history = params['history']
        if(len(history) <= self.degree):
           history_vec = np.concatenate((self.init,history))              
        else:
           history_vec = history        
        x_n_plus_1 = self.const + np.dot(self.coeffs,history_vec[-self.degree:]) + \
                                  self.norm.rvs(1).item() 
        return x_n_plus_1
    
    
class MovingAvg(Sampler):
    def __init__(self,coeffs,noise=1.0,mean=0.0):        
        """
        Generate a moving average time series plus added normal noise.
        coeffs: the theta vector for model degree n. [theta_1, theta_2, theta_3, ..., theta_n]
        """
        Sampler.__init__(self)        
           
        self.coeffs = np.array(coeffs,dtype=float)
        self.mean = mean
        self.norm = norm(0.0,noise)
        self.init = np.array( [self.norm.rvs(1).item() for i in self.coeffs] ,dtype=float)
        
        
    def __call__(self,params):                  
        epsion_n_plus_1 = self.norm.rvs(1).item()
        x_n_plus_1 = self.mean + np.dot(self.coeffs,self.init) +  epsion_n_plus_1
        
        self.init = np.roll(self.init,-1)# shift all the element to left, so the first element moves to last
        self.init[-1] = epsion_n_plus_1# replace the last element (which is the first one from previous shift) with the new one
        return x_n_plus_1    
    
