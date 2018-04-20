# -*- coding: utf-8 -*-
"""
Created on Fri Apr 20 11:16:32 2018

@author: roozbeh
"""
#%%
import warnings
import numpy as np
from numpy import timedelta64
import pandas as pd

class TemporalTemplate:
    
    def __init__(self, recipe):
        self.recipe = recipe
        #Format one: start, end, delta
        if('start' in recipe and 'end' in recipe and 'delta' in recipe and not 'length' in recipe \
           and not 'points' in recipe and not 'res' in recipe and not 'points_delta' in recipe):
            self.start = pd.to_datetime(recipe['start'])
            self.end = pd.to_datetime(recipe['end'])
            self.delta = self.__parse_delta__(recipe)
            if('start-exclusive' in recipe and recipe['start-exclusive'] == True):
                ticks = []
            else:
                ticks = [self.start]
                
            current_date = self.start+ self.delta
            while current_date < self.end:                
                ticks.append(current_date)
                current_date = current_date + self.delta
                
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
            self.delta = self.__parse_delta__(recipe)
            
            if('start-exclusive' in recipe and recipe['start-exclusive'] == True):
                ticks = []
                l = self.length
            else:
                ticks = [self.start]
                l = self.length -1
                
            current_date = self.start+ self.delta
            for idx in range(l):                
                ticks.append(current_date)
                current_date = current_date + self.delta
            
            self.end = ticks[-1]
            if('end-exclusive' in recipe):
                warnings.warn('end-exclusive does not have any effect when end is not defined in recipe.',SyntaxWarning)
                
            self.ticks = np.array(ticks)
        #Format three: end, length, delta
        elif(not 'start' in recipe and 'end' in recipe and 'delta' in recipe and 'length' in recipe\
           and not 'points' in recipe and not 'res' in recipe and not 'points_delta' in recipe):
            self.end = pd.to_datetime(recipe['end'])
            self.length = int(recipe['length'])
            self.delta = self.__parse_delta__(recipe)
            
            if('end-exclusive' in recipe and recipe['end-exclusive'] == True):
                ticks = []
                l = self.length
            else:
                ticks = [self.end]
                l = self.length -1
            
            current_date = self.end - self.delta
            for idx in range(l):
                ticks.insert(0,current_date)
                current_date = current_date - self.delta
                
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
            
            self.delta = (self.end - self.start)/l
            
            if('start-exclusive' in recipe and recipe['start-exclusive'] == True):
                ticks = []
            else:
                ticks = [self.start]
                
            current_date = self.start+ self.delta
            while  self.end - current_date > timedelta64(1,'ms'):                
                ticks.append(current_date)
                current_date = current_date + self.delta
                
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
                                Format six: end, points_delta, res
                                Note: 
                                    start: formatted date-time as string
                                    end: formatted date-time as string 
                                    length: int
                                    delta: string. e.g '1 s', '2 m', '3 h' , '4 D'
                                    points:  an iteratable of int. It must be an strictly increasing function 
                                    points_delta: an iteratable of int. All its elements must be positive.
                                    res: an string for the resolution of points in time. similar to delta time part.                                    
                             """)
        
       
    def __parse_delta__(self,recipe):
        try:
            (i,st) = recipe['delta'].split(' ')                
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