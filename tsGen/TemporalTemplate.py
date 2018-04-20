# -*- coding: utf-8 -*-
"""
Created on Fri Apr 20 11:16:32 2018

@author: roozbeh
"""
#%%
import numpy as np
from numpy import timedelta64
import pandas as pd

class TemporalTemplate:
    
    def __init__(self, recipe):
        self.recipe = recipe
        #Format one: start, end, delta
        if('start' in recipe and 'end' in recipe and 'delta' in recipe and not 'length' in recipe):
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
        elif('start' in recipe and not 'end' in recipe and 'delta' in recipe and 'length' in recipe):
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
            if('end-exclusive' in recipe and recipe['end-exclusive'] == True):
                ticks.remove(self.end)
            self.ticks = np.array(ticks)
        #Format three: end, length, delta
        elif(not 'start' in recipe and 'end' in recipe and 'delta' in recipe and 'length' in recipe):
            self.end = pd.to_datetime(recipe['end'])
            self.length = int(recipe['length'])
            self.delta = self.__parse_delta__(recipe)
        #Format four: start, end, length
        elif('start' in recipe and 'end' in recipe and not 'delta' in recipe and 'length' in recipe):
            self.start = pd.to_datetime(recipe['start'])
            self.end = pd.to_datetime(recipe['end'])
            self.length = int(recipe['length'])

        else:
            raise ValueError("""The provided recipe does not follow any of the possible formats:
                                Format one: start, end, delta
                                Format two: start, length, delta
                                Format three: end, length, delta
                                Format four: start, end, length
                                Note: 
                                    start: formatted date-time as string
                                    end: formatted date-time as string 
                                    length: int
                                    delta: string. e.g '1 s', '2 m', '3 h' , '4 D'
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
            ret = timedelta64(i,st)
        except TypeError:    
            raise ValueError('delta is in wrong format. The first part must be an integer. examples: "1 s", "2 m", "3 h", "4 D"')
        return ret