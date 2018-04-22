# -*- coding: utf-8 -*-
"""
Created on Fri Apr 20 11:16:32 2018

@author: roozbeh
"""
#%%
import warnings
from collections import Sequence  
import numpy as np
from numpy import timedelta64
import pandas as pd

class TemporalTemplate:
    
    def __init__(self, recipe, ticks=None):
        if(ticks is None and recipe is None):
            raise ValueError('recipe or ticks is not provided.')
        elif(recipe is not None):
            self.__default_const__(recipe)
        else:       
            if(isinstance(ticks,np.ndarray)):
                self.ticks = np.sort(np.unique(ticks))
            elif(isinstance(ticks,Sequence )):
                self.ticks = np.sort(np.unique(np.array(ticks)))
            else:
                raise ValueError('tick must be a sequence or ndarray.')
            self.start = self.ticks[0]
            self.end = self.ticks[-1]
            self.length = len(self.ticks)
        
        
    def __default_const__(self,recipe):
        self.recipe = recipe
        #Format one: start, end, delta
        if('start' in recipe and 'end' in recipe and 'delta' in recipe and not 'length' in recipe \
           and not 'points' in recipe and not 'res' in recipe and not 'points_delta' in recipe):
            self.start = pd.to_datetime(recipe['start'])
            self.end = pd.to_datetime(recipe['end'])
            delta = self.__parse_delta__(recipe)
            if('start-exclusive' in recipe and recipe['start-exclusive'] == True):
                ticks = []
            else:
                ticks = [self.start]
                
            current_date = self.start+ delta
            while current_date < self.end:                
                ticks.append(current_date)
                current_date = current_date + delta
                
            if('end-exclusive' in recipe and recipe['end-exclusive'] == True):
                if(ticks[-1] == self.end):
                    ticks.remove(self.end)
            else:
                if(ticks[-1] != self.end):
                    ticks.append(self.end)
                    
            self.ticks = np.array(ticks)
            self.length = len(ticks)

        #Format two: start, length, delta
        elif('start' in recipe and not 'end' in recipe and 'delta' in recipe and 'length' in recipe\
           and not 'points' in recipe and not 'res' in recipe and not 'points_delta' in recipe):
            self.start = pd.to_datetime(recipe['start'])
            self.length = int(recipe['length'])
            delta = self.__parse_delta__(recipe)
            
            if('start-exclusive' in recipe and recipe['start-exclusive'] == True):
                ticks = []
                l = self.length
            else:
                ticks = [self.start]
                l = self.length -1
                
            current_date = self.start+ delta
            for idx in range(l):                
                ticks.append(current_date)
                current_date = current_date + delta
            
            self.end = ticks[-1]
            if('end-exclusive' in recipe):
                warnings.warn('end-exclusive does not have any effect when end is not defined in recipe.',SyntaxWarning)
                
            self.ticks = np.array(ticks)
        #Format three: end, length, delta
        elif(not 'start' in recipe and 'end' in recipe and 'delta' in recipe and 'length' in recipe\
           and not 'points' in recipe and not 'res' in recipe and not 'points_delta' in recipe):
            self.end = pd.to_datetime(recipe['end'])
            self.length = int(recipe['length'])
            delta = self.__parse_delta__(recipe)
            
            if('end-exclusive' in recipe and recipe['end-exclusive'] == True):
                ticks = []
                l = self.length
            else:
                ticks = [self.end]
                l = self.length -1
            
            current_date = self.end - delta
            for idx in range(l):
                ticks.insert(0,current_date)
                current_date = current_date - delta
                
            self.start = ticks[0]
            if('start-exclusive' in recipe):
                warnings.warn('start-exclusive does not have any effect when start is not defined in recipe.',SyntaxWarning)
                
            self.ticks = np.array(ticks)
        #Format four: start, end, length
        elif('start' in recipe and 'end' in recipe and not 'delta' in recipe and 'length' in recipe\
           and not 'points' in recipe and not 'res' in recipe and not 'points_delta' in recipe):
            self.start = pd.to_datetime(recipe['start'])
            self.end = pd.to_datetime(recipe['end'])
            self.length = int(recipe['length'])
            
            
            if((not 'start-exclusive' in recipe or recipe['start-exclusive'] == False) and \
               (not 'end-exclusive' in recipe or recipe['end-exclusive'] == False)):
                l = self.length -1 
            elif((not 'start-exclusive' in recipe or recipe['start-exclusive'] == False) or \
                 (not 'end-exclusive' in recipe or recipe['end-exclusive'] == False)):
                l = self.length            
            else:
                l = self.length +1
            
            delta = (self.end - self.start)/l
            
            if('start-exclusive' in recipe and recipe['start-exclusive'] == True):
                ticks = []
            else:
                ticks = [self.start]
                
            current_date = self.start+ delta
            while  self.end - current_date > timedelta64(1,'ms'):                
                ticks.append(current_date)
                current_date = current_date + delta
                
            if(not 'end-exclusive' in recipe or recipe['end-exclusive'] == False):
                ticks.append(self.end)
                    
            self.ticks = np.array(ticks)
            
        #Format five: start, points, res
        elif('start' in recipe and not 'end' in recipe and not 'delta' in recipe and not 'length' in recipe\
           and 'points' in recipe and 'res' in recipe and not 'points_delta' in recipe):
            
            self.start = pd.to_datetime(recipe['start'])
            
            if('start-exclusive' in recipe and recipe['start-exclusive'] == True):
                ticks = []            
            else:
                ticks = [self.start]

            resolution = recipe['res']
            current_date = self.start
            previous_p = 0
            for p in recipe['points']:                         
                delta_p = p - previous_p
                if(delta_p <= 0):
                    raise ValueError('points sequence must be an strictly increasing function ')
                    
                previous_p = p
                current_date += np.timedelta64(delta_p,resolution)
                ticks.append(current_date)
                
            self.end = ticks[-1]
            if('end-exclusive' in recipe):
                warnings.warn('end-exclusive does not have any effect when end is not defined in recipe.',SyntaxWarning)
                
            self.length = len(ticks)
            self.ticks = np.array(ticks)    
            
        #Format six: end, points_delta, res
        elif('start' in recipe and not 'end' in recipe and not 'delta' in recipe and not 'length' in recipe\
           and not 'points' in recipe and 'res' in recipe and 'points_delta' in recipe):
            self.start = pd.to_datetime(recipe['start'])
            
            if('start-exclusive' in recipe and recipe['start-exclusive'] == True):
                ticks = []            
            else:
                ticks = [self.start]

            resolution = recipe['res']
            current_date = self.start
            for p in recipe['points_delta']:      
                if(p <= 0):
                    raise ValueError('points_delta sequence must be positve/non-zero.')                   
                current_date += np.timedelta64(p,resolution)
                ticks.append(current_date)
                
            self.end = ticks[-1]
            if('end-exclusive' in recipe):
                warnings.warn('end-exclusive does not have any effect when end is not defined in recipe.',SyntaxWarning)
                
            self.length = len(ticks)
            self.ticks = np.array(ticks)    
            
        else:
            raise ValueError("""The provided recipe does not follow any of the possible formats:
                                Format one: start, end, delta
                                Format two: start, length, delta
                                Format three: end, length, delta
                                Format four: start, end, length
                                Format five: start, points, res
                                Format six: start, points_delta, res
                                Note: 
                                    start: formatted date-time as string
                                    end: formatted date-time as string 
                                    length: int
                                    delta: string. e.g '1 s', '2 m', '3 h' , '4 D'
                                    points:  an iteratable of int. It must be an strictly increasing function 
                                    points_delta: an iteratable of int. All its elements must be positive.
                                    res: an string for the resolution of points in time. similar to delta time part.                                    
                             """)
    def __getitem__(self, key):
        return self.ticks[key]
    
    def __setitem__(self, key,value):
        self.ticks[key] = value
        
    def __iter__(self):
        return iter(self.ticks)
    def __len__(self):
        return self.length
    
    def __add__(self, other):
        """
          if the second argument is another TemporalTemplate, then merge them together, while it remove duplicate ticks.
          if the second argument is a string of delta (e.g. '1 s'), then it adds the delta to all the ticks.
          if the second argument is a TemporalJitter object, add a random delta (negative values subtracts) to the ticks where the random value is sampled from the TemporalJitter.
        """
        if(isinstance(other,TemporalTemplate)):
            joined_ticks = np.concatenate((self.ticks,other.ticks))
            return TemporalTemplate(recipe=None, ticks=joined_ticks)
        elif(isinstance(other,str)):
            delta = self.__parse_delta__(dict(delta=other))            
            ticks = np.array([ t + delta for t in self.ticks ])
            return TemporalTemplate(recipe=None, ticks=ticks)           
        elif(isinstance(other,TemporalJitter)):
            Jit = iter(other)
            ticks = np.array([ t + next(Jit) for t in self.ticks ])
            return TemporalTemplate(recipe=None, ticks=ticks)           
        else:
            raise ValueError('The provided type cannot be added to TemporalTemplate.')
        
    def __radd__(self, other):
        return self.__add__(other)
    
    def __sub__(self, other):
        """
          if the second argument is a string of delta (e.g. '1 s'), then it subtract the delta from all the ticks.
          if the second argument is a TemporalJitter object, subtract a random delta (negative values adds) from the ticks where the random value is sampled from the TemporalJitter.
        """
        if(isinstance(other,TemporalTemplate)):
            raise ValueError('Subtracting two TemporalTemplates is not defined.')
        elif(isinstance(other,str)):
            delta = self.__parse_delta__(dict(delta=other))
            ticks = np.array([ t - delta for t in self.ticks ])
            return TemporalTemplate(recipe=None, ticks=ticks) 
        elif(isinstance(other,TemporalJitter)):
            Jit = iter(other)
            ticks = np.array([ t - next(Jit) for t in self.ticks ])
            return TemporalTemplate(recipe=None, ticks=ticks) 
        else:
            raise ValueError('The provided type cannot be subtracted from TemporalTemplate.')
            
    
    def __mul__(self, other):
        """
          if the second argument is a int (n), then creates n equal-distance new ticks between each consecutive one.
          if the second argument is a TemporalJitter object, then creates n random equal-distance new ticks between each consecutive one from the ticks where the random value is sampled from the TemporalJitter.
          the negative values does not have any effect.
        """
        if(isinstance(other,TemporalTemplate)):
            raise ValueError('Subtracting two TemporalTemplates is not defined.')
        elif(isinstance(other,int)):
            if(other <= 1):
                return TemporalTemplate(recipe=None, ticks=np.copy(self.ticks)) 
            else:
                ticks = []
                splits = other
                for idx,t in enumerate(self.ticks[:-1]):
                    ticks.append(t)                    
                    next_t = self.ticks[idx+1]
                    delta = (next_t - t)/splits 
                    for j in range(1,splits):                        
                        ticks.append(t + delta*j)
                ticks.append(self.ticks[-1])         
                return TemporalTemplate(recipe=None, ticks=np.array(ticks)) 
        elif(isinstance(other,TemporalJitter)):
            jitter = other
            ticks = []
            for idx,t in enumerate(self.ticks[:-1]):
                ticks.append(t)                    
                next_t = self.ticks[idx+1]
                splits = jitter.nextInt()
                if(splits <= 0):
                    continue                
                delta = (next_t - t)/splits 
                for j in range(1,splits):                        
                    ticks.append(t + delta*j)
            ticks.append(self.ticks[-1])         
            
            return TemporalTemplate(recipe=None, ticks=np.array(ticks)) 
        else:
            raise ValueError('The provided type cannot be subtracted from TemporalTemplate.')
            
    def __rmul__(self,other):
        return self.__mul__(other)
    
    
    def __rshift__(self, other):
        """
          if the second argument is an int or float (greater or equal to 1.0), all the point are expanded by the provided ratio. The starting point is fixed.
        """
        if(isinstance(other,float) or isinstance(other,int)):
            if(other <1):
                raise ValueError('ratio must be greater than 1.0 to expand TemporalTemplate object.')
            else:
                return self.zoom(other)
        else:
            raise ValueError('The provided type cannot be used for expanding the TemporalTemplate object.')
            
    def __lshift__(self, other):
        """
          if the second argument is an int or float (in (0.0, 1.0])), all the point are shrinked by the provided ratio. The starting point is fixed.
        """
        if(isinstance(other,float) or isinstance(other,int)):
            if(other >1 or other <= 0):
                raise ValueError('ratio must be in (0,1.0] to shrink TemporalTemplate object.')
            else:
                return self.zoom(other)
        else:
            raise ValueError('The provided type cannot be used for shrinking the TemporalTemplate object.')
    def zoom(self,ratio):
        if(isinstance(ratio,float) or isinstance(ratio,int)):
            if(ratio <=0):
                raise ValueError('Negative or zero ratio cannot be used for zooming the TemporalTemplate object.')
            elif(ratio ==1):
                return TemporalTemplate(recipe=None, ticks=np.copy(self.ticks)) 
            else:#ratio != 1
                ticks = [self.ticks[0]]
                for idx,t in enumerate(self.ticks[:-1]):
                    next_t = self.ticks[idx+1]
                    delta = next_t - t
                    ticks.append(ticks[-1] + delta*ratio)
                return TemporalTemplate(recipe=None, ticks=np.array(ticks)) 
        else:
           raise ValueError('The provided type cannot be used for zooming the TemporalTemplate object.')
           
    def drop(self,n):
        """
          drops n elements from start
        """
        if(isinstance(n,int)):
            if(n < 0):
                raise ValueError('Negative values cannot be used for droping ticks.')
            elif(n >= self.length):
                raise ValueError('%d is larger than or equal to the length: %d. for droping ticks' % (n,self.length))           
            else:
                ticks = np.array( [self.ticks[i] for i in range(n,self.length)])
                return TemporalTemplate(recipe=None, ticks=ticks)
        else:
           raise ValueError('The provided type cannot be used for droping ticks.')
           
    def drop_r(self,n):
        """
          drops n elements from end
        """
        if(isinstance(n,int)):
            if(n < 0):
                raise ValueError('Negative values cannot be used for left droping ticks.')
            elif(n >= self.length):
                raise ValueError('%d is larger than or equal to the length: %d. for left droping ticks' % (n,self.length))           
            else:
                ticks = np.array( [self.ticks[i] for i in range(0,self.length-n)])
                return TemporalTemplate(recipe=None, ticks=ticks)
        else:
           raise ValueError('The provided type cannot be used for left droping ticks.')
    def __floordiv__(self, n):
        """
         if the second argument is an int, random number of elements are removed from within ticks (not start and end).
         Negative and zero values raise ValueError exception
         Values larger thane length-2 raise ValueError exception
        """
        if(isinstance(n,int)):
            if(n < 0):
                raise ValueError('Negative values cannot be used for removing random ticks.')
            elif(n > self.length -2):
                raise ValueError('%d is larger than the length - 2: (%d -2).' % (n,self.length))
            elif(n == 0):
                return TemporalTemplate(recipe=None, ticks=np.array(self.ticks))
            else:
                indecies =  np.random.choice(range(1,self.length-1),size=n,replace=False)
                ticks = np.copy(self.ticks)
                return TemporalTemplate(recipe=None, ticks=np.delete(ticks,indecies))
        else:
           raise ValueError('The provided type cannot be used for removing random ticks.')
        
    def __str__(self):
        return '\n'.join([ str(i) for i in self.ticks])
    
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
   