# -*- coding: utf-8 -*-
"""
Created on Fri Apr 20 11:14:57 2018

@author: roozbeh
"""

from tsGen import TemporalTemplate 
#%%
import unittest
import pandas as pd
import numpy as np
from scipy.stats import poisson
from scipy.stats import norm
 
class Test1(unittest.TestCase):
    
    def test_create_by_ticks(self):
        start = pd.to_datetime('2018-01-01')
        delta = np.timedelta64(1,'h')
        ticks = [ start + i*delta for i in range(25) ]
        ts = TemporalTemplate(recipe=None,ticks = ticks)
        self.assertEqual(len(ts.ticks),25, 'There must be 25 ticks for 24 hours period with delta 1 h.')
    def test_create_by_invalid_ticks(self):
        
        with self.assertRaises(ValueError):
            ts = TemporalTemplate(recipe=None,ticks = 2)
        
        with self.assertRaises(ValueError):
            ts = TemporalTemplate(recipe=None)
            
    def test_recipe_without_length2(self):
        recipe = { 
            'start': '2018-01-01',
            'end': '2018-01-02',
            'delta': '1 h'
         }        
        ts = TemporalTemplate(recipe)        
        self.assertEqual(len(ts.ticks),25, 'There must be 25 ticks for 24 hours period with delta 1 h.')
        
        
    def test_merge(self):
        recipe_1 = { 
            'start': '2018-01-01',
            'end': '2018-01-02',
            'delta': '1 h'
         }
        recipe_2 = { 
            'start': '2018-01-02',
            'end': '2018-01-03',
            'delta': '1 h'
         }        
        ts1 = TemporalTemplate(recipe_1)
        ts2 = TemporalTemplate(recipe_2)
        
        ts_all = merge(ts1,ts2)        
        self.assertEqual(ts_all.length,49,'The merged TemporalTemplate must have 49 ticks.')
        self.assertEqual(ts_all.start,pd.to_datetime(recipe_1['start']),'The start of the merged TemporalTemplate must be equal to the start of the first recipe.')
        self.assertEqual(ts_all.end,pd.to_datetime(recipe_2['end']),'The end of the merged TemporalTemplate must be equal to the end of the second recipe.')
                
        # half overlap
        recipe_1 = { 
            'start': '2018-01-01',
            'end': '2018-01-02',
            'delta': '1 h'
         }
        recipe_2 = { 
            'start': '2018-01-01 15:00',
            'end': '2018-01-02 15:00',
            'delta': '1 h'
         }        
        ts1 = TemporalTemplate(recipe_1)
        ts2 = TemporalTemplate(recipe_2)
        
        ts_all = merge(ts1,ts2)        
        self.assertEqual(ts_all.length,40,'The merged TemporalTemplate must have 40 ticks.')
        self.assertEqual(ts_all.start,pd.to_datetime(recipe_1['start']),'The start of the merged TemporalTemplate must be equal to the start of the first recipe.')
        self.assertEqual(ts_all.end,pd.to_datetime(recipe_2['end']),'The end of the merged TemporalTemplate must be equal to the end of the second recipe.')
                   
        # one inside the others
        recipe_1 = { 
            'start': '2018-01-01',
            'end': '2018-01-02',
            'delta': '1 h'
         }
        recipe_2 = { 
            'start': '2018-01-01 15:00',
            'end': '2018-01-01 20:00',
            'delta': '1 h'
         }        
        ts1 = TemporalTemplate(recipe_1)
        ts2 = TemporalTemplate(recipe_2)
        
        ts_all = merge(ts1,ts2)        
        self.assertEqual(ts_all.length,25,'The merged TemporalTemplate must have 25 ticks.')
        self.assertEqual(ts_all.start,pd.to_datetime(recipe_1['start']),'The start of the merged TemporalTemplate must be equal to the start of the first recipe.')
        self.assertEqual(ts_all.end,pd.to_datetime(recipe_1['end']),'The end of the merged TemporalTemplate must be equal to the end of the first recipe.')
        
        # No common elements
        recipe_1 = { 
            'start': '2018-01-01',
            'end': '2018-01-02',
            'delta': '1 h'
         }
        recipe_2 = { 
            'start': '2018-01-01 00:15',
            'end': '2018-01-02 00:15',
            'delta': '1 h'
         }        
        ts1 = TemporalTemplate(recipe_1)
        ts2 = TemporalTemplate(recipe_2)
        
        ts_all = merge(ts1,ts2)        
        self.assertEqual(ts_all.length,50,'The merged TemporalTemplate must have 50 ticks.')
        self.assertEqual(ts_all.start,pd.to_datetime(recipe_1['start']),'The start of the merged TemporalTemplate must be equal to the start of the first recipe.')
        self.assertEqual(ts_all.end,pd.to_datetime(recipe_2['end']),'The end of the merged TemporalTemplate must be equal to the end of the second recipe.')
        
        # No common elements and long distnace between
        recipe_1 = { 
            'start': '2018-01-01',
            'end': '2018-01-02',
            'delta': '1 h'
         }
        recipe_2 = { 
            'start': '2018-01-04 00:15',
            'end': '2018-01-05 00:15',
            'delta': '1 h'
         }        
        ts1 = TemporalTemplate(recipe_1)
        ts2 = TemporalTemplate(recipe_2)
        
        ts_all = merge(ts1,ts2)        
        self.assertEqual(ts_all.length,50,'The merged TemporalTemplate must have 50 ticks.')
        self.assertEqual(ts_all.start,pd.to_datetime(recipe_1['start']),'The start of the merged TemporalTemplate must be equal to the start of the first recipe.')
        self.assertEqual(ts_all.end,pd.to_datetime(recipe_2['end']),'The end of the merged TemporalTemplate must be equal to the end of the second recipe.')
        
    def test_plus_by_another_TemporalTemplate(self):
        recipe_1 = { 
            'start': '2018-01-01',
            'end': '2018-01-02',
            'delta': '1 h'
         }
        recipe_2 = { 
            'start': '2018-01-02',
            'end': '2018-01-03',
            'delta': '1 h'
         }        
        ts1 = TemporalTemplate(recipe_1)
        ts2 = TemporalTemplate(recipe_2)
        
        ts_all = ts1 + ts2
        self.assertEqual(ts_all.length,49,'The summed TemporalTemplate must have 49 ticks.')
        self.assertEqual(ts_all.start,pd.to_datetime(recipe_1['start']),'The start of the summed TemporalTemplate must be equal to the start of the first recipe.')
        self.assertEqual(ts_all.end,pd.to_datetime(recipe_2['end']),'The end of the summed TemporalTemplate must be equal to the end of the second recipe.')
                
        # half overlap
        recipe_1 = { 
            'start': '2018-01-01',
            'end': '2018-01-02',
            'delta': '1 h'
         }
        recipe_2 = { 
            'start': '2018-01-01 15:00',
            'end': '2018-01-02 15:00',
            'delta': '1 h'
         }        
        ts1 = TemporalTemplate(recipe_1)
        ts2 = TemporalTemplate(recipe_2)
        
        ts_all = ts1 + ts2     
        self.assertEqual(ts_all.length,40,'The summed TemporalTemplate must have 40 ticks.')
        self.assertEqual(ts_all.start,pd.to_datetime(recipe_1['start']),'The start of the summed TemporalTemplate must be equal to the start of the first recipe.')
        self.assertEqual(ts_all.end,pd.to_datetime(recipe_2['end']),'The end of the summed TemporalTemplate must be equal to the end of the second recipe.')
                   
        # one inside the others
        recipe_1 = { 
            'start': '2018-01-01',
            'end': '2018-01-02',
            'delta': '1 h'
         }
        recipe_2 = { 
            'start': '2018-01-01 15:00',
            'end': '2018-01-01 20:00',
            'delta': '1 h'
         }        
        ts1 = TemporalTemplate(recipe_1)
        ts2 = TemporalTemplate(recipe_2)
        
        ts_all = ts1 + ts2      
        self.assertEqual(ts_all.length,25,'The summed TemporalTemplate must have 25 ticks.')
        self.assertEqual(ts_all.start,pd.to_datetime(recipe_1['start']),'The start of the summed TemporalTemplate must be equal to the start of the first recipe.')
        self.assertEqual(ts_all.end,pd.to_datetime(recipe_1['end']),'The end of the summed TemporalTemplate must be equal to the end of the first recipe.')
        
        # No common elements
        recipe_1 = { 
            'start': '2018-01-01',
            'end': '2018-01-02',
            'delta': '1 h'
         }
        recipe_2 = { 
            'start': '2018-01-01 00:15',
            'end': '2018-01-02 00:15',
            'delta': '1 h'
         }        
        ts1 = TemporalTemplate(recipe_1)
        ts2 = TemporalTemplate(recipe_2)
        
        ts_all = ts1 + ts2   
        self.assertEqual(ts_all.length,50,'The summed TemporalTemplate must have 50 ticks.')
        self.assertEqual(ts_all.start,pd.to_datetime(recipe_1['start']),'The start of the summed TemporalTemplate must be equal to the start of the first recipe.')
        self.assertEqual(ts_all.end,pd.to_datetime(recipe_2['end']),'The end of the summed TemporalTemplate must be equal to the end of the second recipe.')
        
        # No common elements and long distnace between
        recipe_1 = { 
            'start': '2018-01-01',
            'end': '2018-01-02',
            'delta': '1 h'
         }
        recipe_2 = { 
            'start': '2018-01-04 00:15',
            'end': '2018-01-05 00:15',
            'delta': '1 h'
         }        
        ts1 = TemporalTemplate(recipe_1)
        ts2 = TemporalTemplate(recipe_2)
        
        ts_all = ts1 + ts2      
        self.assertEqual(ts_all.length,50,'The summed TemporalTemplate must have 50 ticks.')
        self.assertEqual(ts_all.start,pd.to_datetime(recipe_1['start']),'The start of the summed TemporalTemplate must be equal to the start of the first recipe.')
        self.assertEqual(ts_all.end,pd.to_datetime(recipe_2['end']),'The end of the summed TemporalTemplate must be equal to the end of the second recipe.')
        
    def test_plus_by_delta(self):
        recipe_1 = { 
            'start': '2018-01-01',
            'end': '2018-01-02',
            'delta': '1 h'
         }
                
        ts1 = TemporalTemplate(recipe_1)
        
        
        ts_all = ts1 + '1 h'
        
        self.assertEqual(ts_all.length,ts1.length,'The summed by delta must not change the length.')
        self.assertEqual(ts_all.start,pd.to_datetime(recipe_1['start']) + np.timedelta64(1,'h') ,'The start of the summed TemporalTemplate must be equal to the start of the first recipe plus the delta.')
        self.assertEqual(ts_all.end,pd.to_datetime(recipe_1['end']) + np.timedelta64(1,'h'),'The end of the summed TemporalTemplate must be equal to the end of the second recipe plus the delta.')
        
        ts_all = ts1 + '1 s'
        self.assertEqual(ts_all.length,ts1.length,'The summed by delta must not change the length.')
        self.assertEqual(ts_all.start,pd.to_datetime(recipe_1['start']) + np.timedelta64(1,'s') ,'The start of the summed TemporalTemplate must be equal to the start of the first recipe plus the delta.')
        self.assertEqual(ts_all.end,pd.to_datetime(recipe_1['end']) + np.timedelta64(1,'s'),'The end of the summed TemporalTemplate must be equal to the end of the second recipe plus the delta.')
        
        ts_all = ts1 + '1 D'
        self.assertEqual(ts_all.length,ts1.length,'The summed by delta must not change the length.')
        self.assertEqual(ts_all.start,pd.to_datetime(recipe_1['start']) + np.timedelta64(1,'D') ,'The start of the summed TemporalTemplate must be equal to the start of the first recipe plus the delta.')
        self.assertEqual(ts_all.end,pd.to_datetime(recipe_1['end']) + np.timedelta64(1,'D'),'The end of the summed TemporalTemplate must be equal to the end of the second recipe plus the delta.')
                   
        ts1 += '1 h' 
                
        self.assertEqual(ts1.start,pd.to_datetime(recipe_1['start']) + np.timedelta64(1,'h') ,'The start of the summed TemporalTemplate must be equal to the start of the first recipe plus the delta.')
        self.assertEqual(ts1.end,pd.to_datetime(recipe_1['end']) + np.timedelta64(1,'h'),'The end of the summed TemporalTemplate must be equal to the end of the second recipe plus the delta.')
        
    def test_plus_by_temporal_jitter(self):
        recipe_1 = { 
            'start': '2018-01-01',
            'end': '2018-01-02',
            'delta': '1 h'
         }
                
        ts1 = TemporalTemplate(recipe_1)
        np.random.seed(seed=42)
        
        mu = 0.6
        rv = poisson(mu)        
        j = TemporalJitter(pdf=rv,resolution='m')
        
        
        ts_all = ts1 + j
        self.assertEqual(ts_all.length,ts1.length,'The summed by delta must not change the length.')
        self.assertEqual(ts_all.ticks[1],pd.to_datetime('2018-01-01 01:02:00') ,'The jitter must move the second ticks by 2 minutes.')

        np.random.seed(seed=42)        
        rv = norm(0,10)        
        j = TemporalJitter(pdf=rv,resolution='m')

        ts_all = ts1 + j       
        self.assertEqual(ts_all.length,ts1.length,'The summed by delta must not change the length.')
        self.assertEqual(ts_all.ticks[0],pd.to_datetime('2018-01-01 00:04:00') ,'The jitter must move the first ticks by 4 minutes.')        
        self.assertEqual(ts_all.ticks[-1],pd.to_datetime('2018-01-01 23:55:00') ,'The jitter must move the last ticks by 5 minutes.')        
       

    def test_subtract_by_another_TemporalTemplate(self):
        recipe_1 = { 
            'start': '2018-01-01',
            'end': '2018-01-02',
            'delta': '1 h'
         }
        recipe_2 = { 
            'start': '2018-01-02',
            'end': '2018-01-03',
            'delta': '1 h'
         }        
        ts1 = TemporalTemplate(recipe_1)
        ts2 = TemporalTemplate(recipe_2)
        with self.assertRaises(ValueError):
           ts1 - ts2
        
    def test_subtract_by_delta(self):
        recipe_1 = { 
            'start': '2018-01-01',
            'end': '2018-01-02',
            'delta': '1 h'
         }
                
        ts1 = TemporalTemplate(recipe_1)
        
        
        ts_all = ts1 - '1 h'
        
        self.assertEqual(ts_all.length,ts1.length,'The subtracted by delta must not change the length.')
        self.assertEqual(ts_all.start,pd.to_datetime(recipe_1['start']) - np.timedelta64(1,'h') ,'The start of the subtracted TemporalTemplate must be equal to the start of the first recipe plus the delta.')
        self.assertEqual(ts_all.end,pd.to_datetime(recipe_1['end']) - np.timedelta64(1,'h'),'The end of the subtracted TemporalTemplate must be equal to the end of the second recipe plus the delta.')
        
        ts_all = ts1 - '1 s'
        self.assertEqual(ts_all.length,ts1.length,'The subtracted by delta must not change the length.')
        self.assertEqual(ts_all.start,pd.to_datetime(recipe_1['start']) - np.timedelta64(1,'s') ,'The start of the subtracted TemporalTemplate must be equal to the start of the first recipe plus the delta.')
        self.assertEqual(ts_all.end,pd.to_datetime(recipe_1['end']) - np.timedelta64(1,'s'),'The end of the subtracted TemporalTemplate must be equal to the end of the second recipe plus the delta.')
        
        ts_all = ts1 - '1 D'
        self.assertEqual(ts_all.length,ts1.length,'The subtracted by delta must not change the length.')
        self.assertEqual(ts_all.start,pd.to_datetime(recipe_1['start']) - np.timedelta64(1,'D') ,'The start of the subtracted TemporalTemplate must be equal to the start of the first recipe plus the delta.')
        self.assertEqual(ts_all.end,pd.to_datetime(recipe_1['end']) - np.timedelta64(1,'D'),'The end of the subtracted TemporalTemplate must be equal to the end of the second recipe plus the delta.')
                   
        ts1 -= '1 h' 
                
        self.assertEqual(ts1.start,pd.to_datetime(recipe_1['start']) - np.timedelta64(1,'h') ,'The start of the subtracted TemporalTemplate must be equal to the start of the first recipe plus the delta.')
        self.assertEqual(ts1.end,pd.to_datetime(recipe_1['end']) - np.timedelta64(1,'h'),'The end of the subtracted TemporalTemplate must be equal to the end of the second recipe plus the delta.')

            
if __name__ == '__main__':
    unittest.main()            
