# -*- coding: utf-8 -*-
"""
Created on Fri Apr 20 11:16:32 2018

@author: roozbeh
"""
#%%
import pandas as pd

class TemporalTemplate:
    
    def __init__(self, recipe):
        self.recipe = recipe
        #Format one: start, end, delta
        if('start' in recipe and 'end' in recipe and 'delta' in recipe and not 'length' in recipe):
            self.start = pd.to_datetime(recipe['start'])
            self.end = pd.to_datetime(recipe['end'])
            self.delta = recipe['delta']

        #Format two: start, length, delta
        elif('start' in recipe and not 'end' in recipe and 'delta' in recipe and 'length' in recipe):
            self.start = pd.to_datetime(recipe['start'])
            self.length = recipe['length']
            self.delta = recipe['delta']
        #Format three: end, length, delta
        elif(not 'start' in recipe and 'end' in recipe and 'delta' in recipe and 'length' in recipe):
            self.end = pd.to_datetime(recipe['end'])
            self.length = recipe['length']
            self.delta = recipe['delta']
        #Format four: start, end, length
        elif('start' in recipe and 'end' in recipe and not 'delta' in recipe and 'length' in recipe):
            self.start = pd.to_datetime(recipe['start'])
            self.end = pd.to_datetime(recipe['end'])
            self.length = recipe['length']

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
                                    delta: string. e.g '1 s', '2 min', '3 d'
                             """)
        
       
        