# -*- coding: utf-8 -*-
"""
Created on Fri Apr 20 11:29:25 2018

@author: roozbeh
"""
#import sys, os
#current_dir = os.path.realpath(os.path.curdir)
#lib_dir = os.path.join(current_dir, "tsGen","TemporalTemplate.py")
#sys.path.append(lib_dir)

from tsGen import TemporalTemplate
#%%
import warnings
import unittest
import pandas as pd

 
class TestRecipeSpecs(unittest.TestCase):
    def test_recipe_without_start_end(self):
        recipe_without_start_end = { 
            'length': 100
        }        
        with self.assertRaises(ValueError):
            TemporalTemplate(recipe_without_start_end)
            
    def test_recipe_start_end_without_length_delta(self):
        recipe_start_end_without_length_delta = { 
            'start': '2018-01-01',
            'end': '2018-01-01'
        }        
        with self.assertRaises(ValueError):
            TemporalTemplate(recipe_start_end_without_length_delta)

    def test_recipe_start_length_without_end_delta(self):
        recipe_start_length_without_end_delta = { 
            'start': '2018-01-01',
            'length': 100
        }        
        with self.assertRaises(ValueError):
            TemporalTemplate(recipe_start_length_without_end_delta)  
            
    def test_recipe_end_length_without_start_delta(self):
        recipe_end_length_without_start_delta = { 
            'end': '2018-01-01',
            'length': 100
        }        
        with self.assertRaises(ValueError):
            TemporalTemplate(recipe_end_length_without_start_delta) 
            
    def test_recipe_start_delta_without_end_length(self):
        recipe_start_delta_without_end_length = { 
            'start': '2018-01-01',
            'delta': '1 h'
        }        
        with self.assertRaises(ValueError):
            TemporalTemplate(recipe_start_delta_without_end_length)  
            
    def test_recipe_end_delta_without_start_length(self):
        recipe_end_delta_without_start_length = { 
            'end': '2018-01-01',
            'delta': '1 h'
        }        
        with self.assertRaises(ValueError):
            TemporalTemplate(recipe_end_delta_without_start_length) 
            
    def test_recipe_without_length(self):
        recipe_without_length = { 
            'start': '2018-01-01',
        }        
        with self.assertRaises(ValueError):
            TemporalTemplate(recipe_without_length)
            
    def test_recipe_without_length2(self):
        recipe_without_length2 = { 
            'end': '2018-01-01',
        }        
        with self.assertRaises(ValueError):
            TemporalTemplate(recipe_without_length2)
            
    def test_wrong_delta_format(self):
        recipe_without_delta = { 
            'start': '2018-01-01',
            'end': '2018-01-02',
        }        
        with self.assertRaises(ValueError):
            TemporalTemplate(self.merge(recipe_without_delta,{'delta': '1'}))
            
        with self.assertRaises(ValueError):
            TemporalTemplate(self.merge(recipe_without_delta,{'delta': 's'}))
            
        with self.assertRaises(ValueError):            
            TemporalTemplate(self.merge(recipe_without_delta,{'delta': '1s'}))
            
        with self.assertRaises(ValueError):
            TemporalTemplate(self.merge(recipe_without_delta,{'delta': '1 d'}))
            
        t1 = TemporalTemplate(self.merge(recipe_without_delta,{'delta': '1 h'})) 
        self.assertEqual(len(t1.ticks),25,'There must be 25 ticks.')
        
            
    def test_recipe_with_all_fours(self):
        recipe_without_length2 = { 
            'start': '2018-01-01',
            'end': '2018-01-02',
            'delta': '1 h',
            'length': 100
        }        
        with self.assertRaises(ValueError):
            TemporalTemplate(recipe_without_length2)
            

    def test_recipe_start_end_delta_exlusives(self):
        recipe_start_end_without_length_delta = { 
            'start': '2018-01-01',
            'end': '2018-01-02',
            'delta': '1 h'
        }        
        t1 = TemporalTemplate(recipe_start_end_without_length_delta)
        self.assertEqual(len(t1.ticks),25,'There must be 25 ticks if no exlusion provided.')
        self.assertEqual(t1.length,25,'There must be 25 ticks if no exlusion provided.')
        self.assertEqual(t1.length,len(t1.ticks),'The length property must be equal to the length of ticks.')
        self.assertEqual(t1.ticks[0],t1.start,'The first tick must be equal to start if no exlusion provided.')
        self.assertEqual(t1.ticks[-1],t1.end,'The last tick must be equal to start if no exlusion provided.')
        self.assertEqual(t1.start,pd.to_datetime(recipe_start_end_without_length_delta['start']),'The end must be equal 2018-01-01 00:00:00.')
        self.assertEqual(t1.end,pd.to_datetime(recipe_start_end_without_length_delta['end']),'The end must be equal 2018-01-02 00:00:00.')        
        
        t1 = TemporalTemplate(self.merge(recipe_start_end_without_length_delta,{'start-exclusive':False}))        
        self.assertEqual(len(t1.ticks),25,'There must be 25 ticks if start-exclusive is False.')
        self.assertEqual(t1.length,len(t1.ticks),'The length property must be equal to the length of ticks.')
        self.assertEqual(t1.ticks[0],t1.start,'The first tick must be equal to start if start-exclusive is False.')
        self.assertEqual(t1.ticks[-1],t1.end,'The last tick must be equal to end if start-exclusive is False.')
        self.assertEqual(t1.start,pd.to_datetime(recipe_start_end_without_length_delta['start']),'The end must be equal 2018-01-01 00:00:00.')
        self.assertEqual(t1.end,pd.to_datetime(recipe_start_end_without_length_delta['end']),'The end must be equal 2018-01-02 00:00:00.') 
        
        t1 = TemporalTemplate(self.merge(recipe_start_end_without_length_delta,{'start-exclusive':True}))        
        self.assertEqual(len(t1.ticks),24,'There must be 24 ticks if start-exclusive is True.')
        self.assertEqual(t1.length,len(t1.ticks),'The length property must be equal to the length of ticks.')
        self.assertNotEqual(t1.ticks[0],t1.start,'The first tick must not be equal to start if start-exclusive is True.')
        self.assertEqual(t1.ticks[-1],t1.end,'The last tick must be equal to end even if start-exclusive is True.')
        self.assertEqual(t1.start,pd.to_datetime(recipe_start_end_without_length_delta['start']),'The end must be equal 2018-01-01 00:00:00.')
        self.assertEqual(t1.end,pd.to_datetime(recipe_start_end_without_length_delta['end']),'The end must be equal 2018-01-02 00:00:00.') 
        
        t1 = TemporalTemplate(self.merge(recipe_start_end_without_length_delta,{'end-exclusive':False}))        
        self.assertEqual(len(t1.ticks),25,'There must be 25 ticks if end-exclusive is False.')
        self.assertEqual(t1.length,len(t1.ticks),'The length property must be equal to the length of ticks.')
        self.assertEqual(t1.ticks[0],t1.start,'The first tick must be equal to start if end-exclusive is False.')
        self.assertEqual(t1.ticks[-1],t1.end,'The last tick must be equal to end if end-exclusive is False.')
        self.assertEqual(t1.start,pd.to_datetime(recipe_start_end_without_length_delta['start']),'The end must be equal 2018-01-01 00:00:00.')
        self.assertEqual(t1.end,pd.to_datetime(recipe_start_end_without_length_delta['end']),'The end must be equal 2018-01-02 00:00:00.') 
        
        t1 = TemporalTemplate(self.merge(recipe_start_end_without_length_delta,{'end-exclusive':True}))        
        self.assertEqual(len(t1.ticks),24,'There must be 24 ticks if end-exclusive is True.')
        self.assertEqual(t1.length,len(t1.ticks),'The length property must be equal to the length of ticks.')
        self.assertEqual(t1.ticks[0],t1.start,'The first tick must be equal to start even if end-exclusive is True.')
        self.assertNotEqual(t1.ticks[-1],t1.end,'The last tick not must be equal to end if end-exclusive is True.') 
        self.assertEqual(t1.start,pd.to_datetime(recipe_start_end_without_length_delta['start']),'The end must be equal 2018-01-01 00:00:00.')
        self.assertEqual(t1.end,pd.to_datetime(recipe_start_end_without_length_delta['end']),'The end must be equal 2018-01-02 00:00:00.') 
        
        t1 = TemporalTemplate(self.merge(recipe_start_end_without_length_delta,{'end-exclusive':True,'start-exclusive':True}))        
        self.assertEqual(len(t1.ticks),23,'There must be 23 ticks if both start-exclusive and end-exclusive are True.')
        self.assertEqual(t1.length,len(t1.ticks),'The length property must be equal to the length of ticks.')
        self.assertNotEqual(t1.ticks[0],t1.start,'The first tick must not be equal to start even if both start-exclusive and end-exclusive are True.')
        self.assertNotEqual(t1.ticks[-1],t1.end,'The last tick must not be equal to end if both start-exclusive and end-exclusive are True.') 
        self.assertEqual(t1.start,pd.to_datetime(recipe_start_end_without_length_delta['start']),'The end must be equal 2018-01-01 00:00:00.')
        self.assertEqual(t1.end,pd.to_datetime(recipe_start_end_without_length_delta['end']),'The end must be equal 2018-01-02 00:00:00.') 
        
        #
        # The delta and start/end are not dividable        
        #
        recipe_start_end_without_length_delta = { 
            'start': '2018-01-01',
            'end': '2018-01-02 00:01',
            'delta': '1 h'
        }        
        t1 = TemporalTemplate(recipe_start_end_without_length_delta)
        self.assertEqual(len(t1.ticks),26,'There must be 26 ticks if no exlusion provided.')
        self.assertEqual(t1.length,26,'There must be 26 ticks if no exlusion provided.')
        self.assertEqual(t1.length,len(t1.ticks),'The length property must be equal to the length of ticks.')
        self.assertEqual(t1.ticks[0],t1.start,'The first tick must be equal to start if no exlusion provided.')
        self.assertEqual(t1.ticks[-1],t1.end,'The last tick must be equal to start if no exlusion provided.')
        self.assertEqual(t1.start,pd.to_datetime(recipe_start_end_without_length_delta['start']),'The end must be equal 2018-01-01 00:00:00.')
        self.assertEqual(t1.end,pd.to_datetime(recipe_start_end_without_length_delta['end']),'The end must be equal 2018-01-02 00:00:00.') 
        
        t1 = TemporalTemplate(self.merge(recipe_start_end_without_length_delta,{'start-exclusive':False}))        
        self.assertEqual(len(t1.ticks),26,'There must be 26 ticks if start-exclusive is False.')
        self.assertEqual(t1.length,len(t1.ticks),'The length property must be equal to the length of ticks.')
        self.assertEqual(t1.ticks[0],t1.start,'The first tick must be equal to start if start-exclusive is False.')
        self.assertEqual(t1.ticks[-1],t1.end,'The last tick must be equal to end if start-exclusive is False.')
        self.assertEqual(t1.start,pd.to_datetime(recipe_start_end_without_length_delta['start']),'The end must be equal 2018-01-01 00:00:00.')
        self.assertEqual(t1.end,pd.to_datetime(recipe_start_end_without_length_delta['end']),'The end must be equal 2018-01-02 00:00:00.') 
        
        t1 = TemporalTemplate(self.merge(recipe_start_end_without_length_delta,{'start-exclusive':True}))        
        self.assertEqual(len(t1.ticks),25,'There must be 25 ticks if start-exclusive is True.')
        self.assertEqual(t1.length,len(t1.ticks),'The length property must be equal to the length of ticks.')
        self.assertNotEqual(t1.ticks[0],t1.start,'The first tick must not be equal to start if start-exclusive is True.')
        self.assertEqual(t1.ticks[-1],t1.end,'The last tick must be equal to end even if start-exclusive is True.')
        self.assertEqual(t1.start,pd.to_datetime(recipe_start_end_without_length_delta['start']),'The end must be equal 2018-01-01 00:00:00.')
        self.assertEqual(t1.end,pd.to_datetime(recipe_start_end_without_length_delta['end']),'The end must be equal 2018-01-02 00:00:00.') 
        
        t1 = TemporalTemplate(self.merge(recipe_start_end_without_length_delta,{'end-exclusive':False}))        
        self.assertEqual(len(t1.ticks),26,'There must be 26 ticks if end-exclusive is False.')
        self.assertEqual(t1.length,len(t1.ticks),'The length property must be equal to the length of ticks.')
        self.assertEqual(t1.ticks[0],t1.start,'The first tick must be equal to start if end-exclusive is False.')
        self.assertEqual(t1.ticks[-1],t1.end,'The last tick must be equal to end if end-exclusive is False.')
        self.assertEqual(t1.start,pd.to_datetime(recipe_start_end_without_length_delta['start']),'The end must be equal 2018-01-01 00:00:00.')
        self.assertEqual(t1.end,pd.to_datetime(recipe_start_end_without_length_delta['end']),'The end must be equal 2018-01-02 00:00:00.') 
        
        t1 = TemporalTemplate(self.merge(recipe_start_end_without_length_delta,{'end-exclusive':True}))        
        self.assertEqual(len(t1.ticks),25,'There must be 25 ticks if end-exclusive is True.')
        self.assertEqual(t1.length,len(t1.ticks),'The length property must be equal to the length of ticks.')
        self.assertEqual(t1.ticks[0],t1.start,'The first tick must be equal to start even if end-exclusive is True.')
        self.assertNotEqual(t1.ticks[-1],t1.end,'The last tick must not be equal to end if end-exclusive is True.')   
        self.assertEqual(t1.start,pd.to_datetime(recipe_start_end_without_length_delta['start']),'The end must be equal 2018-01-01 00:00:00.')
        self.assertEqual(t1.end,pd.to_datetime(recipe_start_end_without_length_delta['end']),'The end must be equal 2018-01-02 00:00:00.') 
        
        t1 = TemporalTemplate(self.merge(recipe_start_end_without_length_delta,{'end-exclusive':True,'start-exclusive':True}))        
        self.assertEqual(len(t1.ticks),24,'There must be 24 ticks if both start-exclusive and end-exclusive are True.')
        self.assertEqual(t1.length,len(t1.ticks),'The length property must be equal to the length of ticks.')
        self.assertNotEqual(t1.ticks[0],t1.start,'The first tick must not be equal to start even if both start-exclusive and end-exclusive are True.')
        self.assertNotEqual(t1.ticks[-1],t1.end,'The last tick must not be equal to end if both start-exclusive and end-exclusive are True.') 
        self.assertEqual(t1.start,pd.to_datetime(recipe_start_end_without_length_delta['start']),'The end must be equal 2018-01-01 00:00:00.')
        self.assertEqual(t1.end,pd.to_datetime(recipe_start_end_without_length_delta['end']),'The end must be equal 2018-01-02 00:00:00.') 
        
        #
        #
        #
        recipe_start_end_without_length_delta = { 
            'start': '2018-01-01',
            'end': '2018-01-01 23:59',
            'delta': '1 h'
        }        
        t1 = TemporalTemplate(recipe_start_end_without_length_delta)
        self.assertEqual(len(t1.ticks),25,'There must be 25 ticks if no exlusion provided.')
        self.assertEqual(t1.length,25,'There must be 25 ticks if no exlusion provided.')
        self.assertEqual(t1.length,len(t1.ticks),'The length property must be equal to the length of ticks.')
        self.assertEqual(t1.ticks[0],t1.start,'The first tick must be equal to start if no exlusion provided.')
        self.assertEqual(t1.ticks[-1],t1.end,'The last tick must be equal to start if no exlusion provided.')
        self.assertEqual(t1.start,pd.to_datetime(recipe_start_end_without_length_delta['start']),'The end must be equal 2018-01-01 00:00:00.')
        self.assertEqual(t1.end,pd.to_datetime(recipe_start_end_without_length_delta['end']),'The end must be equal 2018-01-02 00:00:00.') 
        
        t1 = TemporalTemplate(self.merge(recipe_start_end_without_length_delta,{'start-exclusive':False}))        
        self.assertEqual(len(t1.ticks),25,'There must be 25 ticks if start-exclusive is False.')
        self.assertEqual(t1.length,len(t1.ticks),'The length property must be equal to the length of ticks.')
        self.assertEqual(t1.ticks[0],t1.start,'The first tick must be equal to start if start-exclusive is False.')
        self.assertEqual(t1.ticks[-1],t1.end,'The last tick must be equal to end if start-exclusive is False.')
        self.assertEqual(t1.start,pd.to_datetime(recipe_start_end_without_length_delta['start']),'The end must be equal 2018-01-01 00:00:00.')
        self.assertEqual(t1.end,pd.to_datetime(recipe_start_end_without_length_delta['end']),'The end must be equal 2018-01-02 00:00:00.') 
        
        t1 = TemporalTemplate(self.merge(recipe_start_end_without_length_delta,{'start-exclusive':True}))        
        self.assertEqual(len(t1.ticks),24,'There must be 24 ticks if start-exclusive is True.')
        self.assertEqual(t1.length,len(t1.ticks),'The length property must be equal to the length of ticks.')
        self.assertNotEqual(t1.ticks[0],t1.start,'The first tick must not be equal to start if start-exclusive is True.')
        self.assertEqual(t1.ticks[-1],t1.end,'The last tick must be equal to end even if start-exclusive is True.')
        self.assertEqual(t1.start,pd.to_datetime(recipe_start_end_without_length_delta['start']),'The end must be equal 2018-01-01 00:00:00.')
        self.assertEqual(t1.end,pd.to_datetime(recipe_start_end_without_length_delta['end']),'The end must be equal 2018-01-02 00:00:00.') 
        
        t1 = TemporalTemplate(self.merge(recipe_start_end_without_length_delta,{'end-exclusive':False}))        
        self.assertEqual(len(t1.ticks),25,'There must be 25 ticks if end-exclusive is False.')
        self.assertEqual(t1.length,len(t1.ticks),'The length property must be equal to the length of ticks.')
        self.assertEqual(t1.ticks[0],t1.start,'The first tick must be equal to start if end-exclusive is False.')
        self.assertEqual(t1.ticks[-1],t1.end,'The last tick must be equal to end if end-exclusive is False.')
        self.assertEqual(t1.start,pd.to_datetime(recipe_start_end_without_length_delta['start']),'The end must be equal 2018-01-01 00:00:00.')
        self.assertEqual(t1.end,pd.to_datetime(recipe_start_end_without_length_delta['end']),'The end must be equal 2018-01-02 00:00:00.') 
        
        t1 = TemporalTemplate(self.merge(recipe_start_end_without_length_delta,{'end-exclusive':True}))        
        self.assertEqual(len(t1.ticks),24,'There must be 24 ticks if end-exclusive is True.')
        self.assertEqual(t1.length,len(t1.ticks),'The length property must be equal to the length of ticks.')
        self.assertEqual(t1.ticks[0],t1.start,'The first tick must be equal to start even if end-exclusive is True.')
        self.assertNotEqual(t1.ticks[-1],t1.end,'The last tick must not be equal to end if end-exclusive is True.')   
        self.assertEqual(t1.start,pd.to_datetime(recipe_start_end_without_length_delta['start']),'The end must be equal 2018-01-01 00:00:00.')
        self.assertEqual(t1.end,pd.to_datetime(recipe_start_end_without_length_delta['end']),'The end must be equal 2018-01-02 00:00:00.') 
        
        t1 = TemporalTemplate(self.merge(recipe_start_end_without_length_delta,{'end-exclusive':True,'start-exclusive':True}))        
        self.assertEqual(len(t1.ticks),23,'There must be 23 ticks if both start-exclusive and end-exclusive are True.')
        self.assertEqual(t1.length,len(t1.ticks),'The length property must be equal to the length of ticks.')
        self.assertNotEqual(t1.ticks[0],t1.start,'The first tick must not be equal to start even if both start-exclusive and end-exclusive are True.')
        self.assertNotEqual(t1.ticks[-1],t1.end,'The last tick must not be equal to end if both start-exclusive and end-exclusive are True.') 
        self.assertEqual(t1.start,pd.to_datetime(recipe_start_end_without_length_delta['start']),'The end must be equal 2018-01-01 00:00:00.')
        self.assertEqual(t1.end,pd.to_datetime(recipe_start_end_without_length_delta['end']),'The end must be equal 2018-01-02 00:00:00.') 
        
    def test_recipe_start_length_delta_exlusives(self):
        recipe_start_length_delta_exlusives = { 
            'start': '2018-01-01',
            'length': 25,
            'delta': '1 h'
        }        
        t1 = TemporalTemplate(recipe_start_length_delta_exlusives)
        self.assertEqual(len(t1.ticks),25,'There must be 25 ticks if no exlusion provided.')
        self.assertEqual(t1.length,25,'There must be 25 ticks if no exlusion provided.')
        self.assertEqual(t1.length,len(t1.ticks),'The length property must be equal to the length of ticks.')
        self.assertEqual(t1.ticks[0],t1.start,'The first tick must be equal to start if no exlusion provided.')
        self.assertEqual(t1.ticks[-1],t1.end,'The last tick must be equal to start if no exlusion provided.')
        self.assertEqual(t1.start,pd.to_datetime(recipe_start_length_delta_exlusives['start']),'The end must be equal 2018-01-01 00:00:00.')
        self.assertEqual(t1.end,pd.to_datetime('2018-01-02'),'The end must be equal 2018-01-02 00:00:00.')
        
        
        t1 = TemporalTemplate(self.merge(recipe_start_length_delta_exlusives,{'start-exclusive':False}))        
        self.assertEqual(len(t1.ticks),25,'There must be 25 ticks if start-exclusive is False.')
        self.assertEqual(t1.length,len(t1.ticks),'The length property must be equal to the length of ticks.')
        self.assertEqual(t1.ticks[0],t1.start,'The first tick must be equal to start if start-exclusive is False.')
        self.assertEqual(t1.ticks[-1],t1.end,'The last tick must be equal to end if start-exclusive is False.')
        self.assertEqual(t1.start,pd.to_datetime(recipe_start_length_delta_exlusives['start']),'The end must be equal 2018-01-01 00:00:00.')
        self.assertEqual(t1.end,pd.to_datetime('2018-01-02'),'The end must be equal 2018-01-02 00:00:00.')
        
        t1 = TemporalTemplate(self.merge(recipe_start_length_delta_exlusives,{'start-exclusive':True}))        
        self.assertEqual(len(t1.ticks),25,'There must be 25 ticks if start-exclusive is True.')
        self.assertEqual(t1.length,len(t1.ticks),'The length property must be equal to the length of ticks.')
        self.assertNotEqual(t1.ticks[0],t1.start,'The first tick must not be equal to start if start-exclusive is True.')
        self.assertEqual(t1.ticks[-1],t1.end,'The last tick must be equal to end even if start-exclusive is True.')
        self.assertEqual(t1.start,pd.to_datetime(recipe_start_length_delta_exlusives['start']),'The end must be equal 2018-01-01 00:00:00.')
        self.assertEqual(t1.end,pd.to_datetime('2018-01-02 01:00'),'The end must be equal 2018-01-02 01:00:00.')
        
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            t1 = TemporalTemplate(self.merge(recipe_start_length_delta_exlusives,{'end-exclusive':False}))        
            self.assertEqual(len(t1.ticks),25,'There must be 25 ticks if end-exclusive is False.')
            self.assertEqual(t1.length,len(t1.ticks),'The length property must be equal to the length of ticks.')
            self.assertEqual(t1.ticks[0],t1.start,'The first tick must be equal to start if end-exclusive is False.')
            self.assertEqual(t1.ticks[-1],t1.end,'The last tick must be equal to end if end-exclusive is False.')
            self.assertEqual(t1.start,pd.to_datetime(recipe_start_length_delta_exlusives['start']),'The end must be equal 2018-01-01 00:00:00.')
            self.assertEqual(t1.end,pd.to_datetime('2018-01-02'),'The end must be equal 2018-01-02 00:00:00.')
            self.assertEqual(w[-1].category,SyntaxWarning )
            
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            t1 = TemporalTemplate(self.merge(recipe_start_length_delta_exlusives,{'end-exclusive':True}))        
            self.assertEqual(len(t1.ticks),25,'There must be 254 ticks if end-exclusive is True.')
            self.assertEqual(t1.length,len(t1.ticks),'The length property must be equal to the length of ticks.')
            self.assertEqual(t1.ticks[0],t1.start,'The first tick must be equal to start even if end-exclusive is True.')
            self.assertEqual(t1.ticks[-1],t1.end,'The last tick must be equal to end even if end-exclusive is True but end is not in recipe.') 
            self.assertEqual(t1.start,pd.to_datetime(recipe_start_length_delta_exlusives['start']),'The end must be equal 2018-01-01 00:00:00.')
            self.assertEqual(t1.end,pd.to_datetime('2018-01-02'),'The end must be equal 2018-01-02 00:00:00.')
            self.assertEqual(w[-1].category,SyntaxWarning )
        
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            t1 = TemporalTemplate(self.merge(recipe_start_length_delta_exlusives,{'end-exclusive':True,'start-exclusive':True}))        
            self.assertEqual(len(t1.ticks),25,'There must be 25 ticks if both start-exclusive and end-exclusive are True.')
            self.assertEqual(t1.length,len(t1.ticks),'The length property must be equal to the length of ticks.')
            self.assertNotEqual(t1.ticks[0],t1.start,'The first tick must not be equal to start even if both start-exclusive and end-exclusive are True.')
            self.assertEqual(t1.ticks[-1],t1.end,'The last tick must be equal to end even if end-exclusive is True but end is not in recipe.')
            self.assertEqual(t1.start,pd.to_datetime(recipe_start_length_delta_exlusives['start']),'The end must be equal 2018-01-01 00:00:00.')
            self.assertEqual(t1.end,pd.to_datetime('2018-01-02 01:00'),'The end must be equal 2018-01-02 01:00:00.')
            self.assertEqual(w[-1].category,SyntaxWarning )
        
    def test_recipe_end_length_delta_exlusives(self):
        recipe_end_length_delta_exlusives = { 
            'end': '2018-01-02',
            'length': 25,
            'delta': '1 h'
        }        
        t1 = TemporalTemplate(recipe_end_length_delta_exlusives)
        self.assertEqual(len(t1.ticks),25,'There must be 25 ticks if no exlusion provided.')
        self.assertEqual(t1.length,25,'There must be 25 ticks if no exlusion provided.')
        self.assertEqual(t1.length,len(t1.ticks),'The length property must be equal to the length of ticks.')
        self.assertEqual(t1.ticks[0],t1.start,'The first tick must be equal to start if no exlusion provided.')
        self.assertEqual(t1.ticks[-1],t1.end,'The last tick must be equal to start if no exlusion provided.')
        self.assertEqual(t1.start,pd.to_datetime('2018-01-01'),'The start must be equal 2018-01-01 00:00:00.')
        self.assertEqual(t1.end,pd.to_datetime(recipe_end_length_delta_exlusives['end']),'The end must be equal 2018-01-02 00:00:00.') 
        
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            t1 = TemporalTemplate(self.merge(recipe_end_length_delta_exlusives,{'start-exclusive':False}))        
            self.assertEqual(len(t1.ticks),25,'There must be 25 ticks if start-exclusive is False.')
            self.assertEqual(t1.length,len(t1.ticks),'The length property must be equal to the length of ticks.')
            self.assertEqual(t1.ticks[0],t1.start,'The first tick must be equal to start if start-exclusive is False.')
            self.assertEqual(t1.ticks[-1],t1.end,'The last tick must be equal to end if start-exclusive is False.')
            self.assertEqual(t1.start,pd.to_datetime('2018-01-01'),'The start must be equal 2018-01-01 00:00:00.')
            self.assertEqual(t1.end,pd.to_datetime(recipe_end_length_delta_exlusives['end']),'The end must be equal 2018-01-02 00:00:00.') 
            self.assertEqual(w[-1].category,SyntaxWarning )
        
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            t1 = TemporalTemplate(self.merge(recipe_end_length_delta_exlusives,{'start-exclusive':True}))        
            self.assertEqual(len(t1.ticks),25,'There must be 25 ticks if start-exclusive is True.')
            self.assertEqual(t1.length,len(t1.ticks),'The length property must be equal to the length of ticks.')
            self.assertEqual(t1.ticks[0],t1.start,'The first tick must be equal to start even if start-exclusive is True.')
            self.assertEqual(t1.ticks[-1],t1.end,'The last tick must be equal to end even if start-exclusive is True.')
            self.assertEqual(t1.start,pd.to_datetime('2018-01-01'),'The start must be equal 2018-01-01 00:00:00.')
            self.assertEqual(t1.end,pd.to_datetime(recipe_end_length_delta_exlusives['end']),'The end must be equal 2018-01-02 00:00:00.') 
            self.assertEqual(w[-1].category,SyntaxWarning )
        
        t1 = TemporalTemplate(self.merge(recipe_end_length_delta_exlusives,{'end-exclusive':False}))        
        self.assertEqual(len(t1.ticks),25,'There must be 25 ticks if end-exclusive is False.')
        self.assertEqual(t1.length,len(t1.ticks),'The length property must be equal to the length of ticks.')
        self.assertEqual(t1.ticks[0],t1.start,'The first tick must be equal to start if end-exclusive is False.')
        self.assertEqual(t1.ticks[-1],t1.end,'The last tick must be equal to end if end-exclusive is False.')
        self.assertEqual(t1.start,pd.to_datetime('2018-01-01'),'The start must be equal 2018-01-01 00:00:00.')
        self.assertEqual(t1.end,pd.to_datetime(recipe_end_length_delta_exlusives['end']),'The end must be equal 2018-01-02 00:00:00.') 
        
        t1 = TemporalTemplate(self.merge(recipe_end_length_delta_exlusives,{'end-exclusive':True}))        
        self.assertEqual(len(t1.ticks),25,'There must be 25 ticks if end-exclusive is True.')
        self.assertEqual(t1.length,len(t1.ticks),'The length property must be equal to the length of ticks.')
        self.assertEqual(t1.ticks[0],t1.start,'The first tick must be equal to start even if end-exclusive is True.')
        self.assertNotEqual(t1.ticks[-1],t1.end,'The last tick not must be equal to end if end-exclusive is True.')
        self.assertEqual(t1.start,pd.to_datetime('2017-12-31 23:00:00'),'The start must be equal 2017-12-31 23:00:00.')
        self.assertEqual(t1.end,pd.to_datetime(recipe_end_length_delta_exlusives['end']),'The end must be equal 2018-01-02 00:00:00.') 
        
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            t1 = TemporalTemplate(self.merge(recipe_end_length_delta_exlusives,{'end-exclusive':True,'start-exclusive':True}))        
            self.assertEqual(len(t1.ticks),25,'There must be 25 ticks if both start-exclusive and end-exclusive are True.')
            self.assertEqual(t1.length,len(t1.ticks),'The length property must be equal to the length of ticks.')
            self.assertEqual(t1.ticks[0],t1.start,'The first tick must be equal to start even even if both start-exclusive and end-exclusive are True.')
            self.assertNotEqual(t1.ticks[-1],t1.end,'The last tick must not be equal to end if both start-exclusive and end-exclusive are True.')
            self.assertEqual(t1.start,pd.to_datetime('2017-12-31 23:00:00'),'The start must be equal 2017-12-31 23:00:00.')
            self.assertEqual(t1.end,pd.to_datetime(recipe_end_length_delta_exlusives['end']),'The end must be equal 2018-01-02 00:00:00.') 
            self.assertEqual(w[-1].category,SyntaxWarning )
        
    def test_recipe_start_end_length_exlusives(self):
        recipe_start_end_length_exlusives = { 
            'start': '2018-01-01',
            'end': '2018-01-02',
            'length': 25
        }        
        
        t1 = TemporalTemplate(recipe_start_end_length_exlusives)        
        self.assertEqual(len(t1.ticks),25,'There must be 25 ticks if no exlusion provided.')
        self.assertEqual(t1.length,25,'There must be 25 ticks if no exlusion provided.')
        self.assertEqual(t1.length,len(t1.ticks),'The length property must be equal to the length of ticks.')
        self.assertEqual(t1.ticks[0],t1.start,'The first tick must be equal to start if no exlusion provided.')
        self.assertEqual(t1.ticks[-1],t1.end,'The last tick must be equal to start if no exlusion provided.')
        self.assertEqual(t1.start,pd.to_datetime(recipe_start_end_length_exlusives['start']),'The end must be equal 2018-01-01 00:00:00.')
        self.assertEqual(t1.end,pd.to_datetime(recipe_start_end_length_exlusives['end']),'The end must be equal 2018-01-02 00:00:00.')        
        
        t1 = TemporalTemplate(self.merge(recipe_start_end_length_exlusives,{'start-exclusive':False}))        
        self.assertEqual(len(t1.ticks),25,'There must be 25 ticks if start-exclusive is False.')
        self.assertEqual(t1.length,len(t1.ticks),'The length property must be equal to the length of ticks.')
        self.assertEqual(t1.ticks[0],t1.start,'The first tick must be equal to start if start-exclusive is False.')
        self.assertEqual(t1.ticks[-1],t1.end,'The last tick must be equal to end if start-exclusive is False.')
        self.assertEqual(t1.start,pd.to_datetime(recipe_start_end_length_exlusives['start']),'The end must be equal 2018-01-01 00:00:00.')
        self.assertEqual(t1.end,pd.to_datetime(recipe_start_end_length_exlusives['end']),'The end must be equal 2018-01-02 00:00:00.') 
        
        t1 = TemporalTemplate(self.merge(recipe_start_end_length_exlusives,{'start-exclusive':True}))        
        self.assertEqual(len(t1.ticks),25,'There must be 25 ticks if start-exclusive is True.')
        self.assertEqual(t1.length,len(t1.ticks),'The length property must be equal to the length of ticks.')
        self.assertNotEqual(t1.ticks[0],t1.start,'The first tick must not be equal to start if start-exclusive is True.')
        self.assertEqual(t1.ticks[-1],t1.end,'The last tick must be equal to end even if start-exclusive is True.')
        self.assertEqual(t1.start,pd.to_datetime(recipe_start_end_length_exlusives['start']),'The end must be equal 2018-01-01 00:00:00.')
        self.assertEqual(t1.end,pd.to_datetime(recipe_start_end_length_exlusives['end']),'The end must be equal 2018-01-02 00:00:00.') 
        
        t1 = TemporalTemplate(self.merge(recipe_start_end_length_exlusives,{'end-exclusive':False}))        
        self.assertEqual(len(t1.ticks),25,'There must be 25 ticks if end-exclusive is False.')
        self.assertEqual(t1.length,len(t1.ticks),'The length property must be equal to the length of ticks.')
        self.assertEqual(t1.ticks[0],t1.start,'The first tick must be equal to start if end-exclusive is False.')
        self.assertEqual(t1.ticks[-1],t1.end,'The last tick must be equal to end if end-exclusive is False.')
        self.assertEqual(t1.start,pd.to_datetime(recipe_start_end_length_exlusives['start']),'The end must be equal 2018-01-01 00:00:00.')
        self.assertEqual(t1.end,pd.to_datetime(recipe_start_end_length_exlusives['end']),'The end must be equal 2018-01-02 00:00:00.') 
        
        t1 = TemporalTemplate(self.merge(recipe_start_end_length_exlusives,{'end-exclusive':True}))         
        self.assertEqual(len(t1.ticks),25,'There must be 25 ticks if end-exclusive is True.')
        self.assertEqual(t1.length,len(t1.ticks),'The length property must be equal to the length of ticks.')
        self.assertEqual(t1.ticks[0],t1.start,'The first tick must be equal to start even if end-exclusive is True.')
        self.assertNotEqual(t1.ticks[-1],t1.end,'The last tick not must be equal to end if end-exclusive is True.') 
        self.assertEqual(t1.start,pd.to_datetime(recipe_start_end_length_exlusives['start']),'The end must be equal 2018-01-01 00:00:00.')
        self.assertEqual(t1.end,pd.to_datetime(recipe_start_end_length_exlusives['end']),'The end must be equal 2018-01-02 00:00:00.') 
        
        t1 = TemporalTemplate(self.merge(recipe_start_end_length_exlusives,{'end-exclusive':True,'start-exclusive':True}))         
        self.assertEqual(len(t1.ticks),25,'There must be 25 ticks if both start-exclusive and end-exclusive are True.')
        self.assertEqual(t1.length,len(t1.ticks),'The length property must be equal to the length of ticks.')
        self.assertNotEqual(t1.ticks[0],t1.start,'The first tick must not be equal to start even if both start-exclusive and end-exclusive are True.')
        self.assertNotEqual(t1.ticks[-1],t1.end,'The last tick must not be equal to end if both start-exclusive and end-exclusive are True.') 
        self.assertEqual(t1.start,pd.to_datetime(recipe_start_end_length_exlusives['start']),'The end must be equal 2018-01-01 00:00:00.')
        self.assertEqual(t1.end,pd.to_datetime(recipe_start_end_length_exlusives['end']),'The end must be equal 2018-01-02 00:00:00.') 
    
    def test_non_strictly_increasing_points(self):
        non_strictly_increasing_points = { 
            'start': '2018-01-01',
            'res': 'h',
            
        }        
        with self.assertRaises(ValueError):
            TemporalTemplate(self.merge(non_strictly_increasing_points,{'points': [1,2,3,2,6] }))   
            
        with self.assertRaises(ValueError):
            TemporalTemplate(self.merge(non_strictly_increasing_points,{'points': [1,2,3,-3,6] }))
            
        with self.assertRaises(ValueError):
            TemporalTemplate(self.merge(non_strictly_increasing_points,{'points': [1,2,3,3,6] }))

    def test_recipe_start_point_res_exlusives(self):
        recipe_start_point_res_exlusives = { 
            'start': '2018-01-01',
            'points': [int(i) for i in range(1,25)],
            'res': 'h'
        }                
        t1 = TemporalTemplate(recipe_start_point_res_exlusives)            
        self.assertEqual(len(t1.ticks),25,'There must be 25 ticks if no exlusion provided.')
        self.assertEqual(t1.length,25,'There must be 25 ticks if no exlusion provided.')
        self.assertEqual(t1.length,len(t1.ticks),'The length property must be equal to the length of ticks.')
        self.assertEqual(t1.ticks[0],t1.start,'The first tick must be equal to start if no exlusion provided.')
        self.assertEqual(t1.ticks[-1],t1.end,'The last tick must be equal to start if no exlusion provided.')
        self.assertEqual(t1.start,pd.to_datetime(recipe_start_point_res_exlusives['start']),'The end must be equal 2018-01-01 00:00:00.')
        self.assertEqual(t1.end,pd.to_datetime('2018-01-02'),'The end must be equal 2018-01-02 00:00:00.')        
        
        t1 = TemporalTemplate(self.merge(recipe_start_point_res_exlusives,{'start-exclusive':False}))        
        self.assertEqual(len(t1.ticks),25,'There must be 25 ticks if start-exclusive is False.')
        self.assertEqual(t1.length,len(t1.ticks),'The length property must be equal to the length of ticks.')
        self.assertEqual(t1.ticks[0],t1.start,'The first tick must be equal to start if start-exclusive is False.')
        self.assertEqual(t1.ticks[-1],t1.end,'The last tick must be equal to end if start-exclusive is False.')
        self.assertEqual(t1.start,pd.to_datetime(recipe_start_point_res_exlusives['start']),'The end must be equal 2018-01-01 00:00:00.')
        self.assertEqual(t1.end,pd.to_datetime('2018-01-02'),'The end must be equal 2018-01-02 00:00:00.') 
        
        t1 = TemporalTemplate(self.merge(recipe_start_point_res_exlusives,{'start-exclusive':True}))        
        self.assertEqual(len(t1.ticks),24,'There must be 24 ticks if start-exclusive is True.')
        self.assertEqual(t1.length,len(t1.ticks),'The length property must be equal to the length of ticks.')
        self.assertNotEqual(t1.ticks[0],t1.start,'The first tick must not be equal to start if start-exclusive is True.')
        self.assertEqual(t1.ticks[-1],t1.end,'The last tick must be equal to end even if start-exclusive is True.')
        self.assertEqual(t1.start,pd.to_datetime(recipe_start_point_res_exlusives['start']),'The end must be equal 2018-01-01 00:00:00.')
        self.assertEqual(t1.end,pd.to_datetime('2018-01-02'),'The end must be equal 2018-01-02 00:00:00.') 
        
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            t1 = TemporalTemplate(self.merge(recipe_start_point_res_exlusives,{'end-exclusive':False}))        
            self.assertEqual(len(t1.ticks),25,'There must be 25 ticks if end-exclusive is False.')
            self.assertEqual(t1.length,len(t1.ticks),'The length property must be equal to the length of ticks.')
            self.assertEqual(t1.ticks[0],t1.start,'The first tick must be equal to start if end-exclusive is False.')
            self.assertEqual(t1.ticks[-1],t1.end,'The last tick must be equal to end if end-exclusive is False.')
            self.assertEqual(t1.start,pd.to_datetime(recipe_start_point_res_exlusives['start']),'The end must be equal 2018-01-01 00:00:00.')
            self.assertEqual(t1.end,pd.to_datetime('2018-01-02'),'The end must be equal 2018-01-02 00:00:00.') 
            self.assertEqual(w[-1].category,SyntaxWarning )
        
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            t1 = TemporalTemplate(self.merge(recipe_start_point_res_exlusives,{'end-exclusive':True}))         
            self.assertEqual(len(t1.ticks),25,'There must be 25 ticks if end-exclusive is True.')
            self.assertEqual(t1.length,len(t1.ticks),'The length property must be equal to the length of ticks.')
            self.assertEqual(t1.ticks[0],t1.start,'The first tick must be equal to start even if end-exclusive is True.')
            self.assertEqual(t1.ticks[-1],t1.end,'The last tick must be equal to end even if end-exclusive is True when the end is not set.') 
            self.assertEqual(t1.start,pd.to_datetime(recipe_start_point_res_exlusives['start']),'The end must be equal 2018-01-01 00:00:00.')
            self.assertEqual(t1.end,pd.to_datetime('2018-01-02'),'The end must be equal 2018-01-02 00:00:00.') 
            self.assertEqual(w[-1].category,SyntaxWarning )
        
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            t1 = TemporalTemplate(self.merge(recipe_start_point_res_exlusives,{'end-exclusive':True,'start-exclusive':True}))         
            self.assertEqual(len(t1.ticks),24,'There must be 24 ticks if both start-exclusive and end-exclusive are True.')
            self.assertEqual(t1.length,len(t1.ticks),'The length property must be equal to the length of ticks.')
            self.assertNotEqual(t1.ticks[0],t1.start,'The first tick must not be equal to start even if both start-exclusive and end-exclusive are True.')
            self.assertEqual(t1.ticks[-1],t1.end,'The last tick must be equal to end even if end-exclusive is True when the end is not set.') 
            self.assertEqual(t1.start,pd.to_datetime(recipe_start_point_res_exlusives['start']),'The end must be equal 2018-01-01 00:00:00.')
            self.assertEqual(t1.end,pd.to_datetime('2018-01-02'),'The end must be equal 2018-01-02 00:00:00.') 
            self.assertEqual(w[-1].category,SyntaxWarning )
    
    def test_non_positive_or_zero_points_delta(self):
        non_positive_or_zero_points_delta = { 
            'start': '2018-01-01',
            'res': 'h',            
        }        
        with self.assertRaises(ValueError):
            TemporalTemplate(self.merge(non_positive_or_zero_points_delta,{'points_delta': [1,1,1,0,1,1] }))   
            
        with self.assertRaises(ValueError):
            TemporalTemplate(self.merge(non_positive_or_zero_points_delta,{'points_delta': [1,1,1,-1,1,1] }))
              
    def test_recipe_start_point_delta_res_exlusives(self):
        recipe_start_point_res_exlusives = { 
            'start': '2018-01-01',
            'points_delta': [1 for i in range(1,25)],
            'res': 'h'
        }                
        t1 = TemporalTemplate(recipe_start_point_res_exlusives)            
        self.assertEqual(len(t1.ticks),25,'There must be 25 ticks if no exlusion provided.')
        self.assertEqual(t1.length,25,'There must be 25 ticks if no exlusion provided.')
        self.assertEqual(t1.length,len(t1.ticks),'The length property must be equal to the length of ticks.')
        self.assertEqual(t1.ticks[0],t1.start,'The first tick must be equal to start if no exlusion provided.')
        self.assertEqual(t1.ticks[-1],t1.end,'The last tick must be equal to start if no exlusion provided.')
        self.assertEqual(t1.start,pd.to_datetime(recipe_start_point_res_exlusives['start']),'The end must be equal 2018-01-01 00:00:00.')
        self.assertEqual(t1.end,pd.to_datetime('2018-01-02'),'The end must be equal 2018-01-02 00:00:00.')        
        
        t1 = TemporalTemplate(self.merge(recipe_start_point_res_exlusives,{'start-exclusive':False}))        
        self.assertEqual(len(t1.ticks),25,'There must be 25 ticks if start-exclusive is False.')
        self.assertEqual(t1.length,len(t1.ticks),'The length property must be equal to the length of ticks.')
        self.assertEqual(t1.ticks[0],t1.start,'The first tick must be equal to start if start-exclusive is False.')
        self.assertEqual(t1.ticks[-1],t1.end,'The last tick must be equal to end if start-exclusive is False.')
        self.assertEqual(t1.start,pd.to_datetime(recipe_start_point_res_exlusives['start']),'The end must be equal 2018-01-01 00:00:00.')
        self.assertEqual(t1.end,pd.to_datetime('2018-01-02'),'The end must be equal 2018-01-02 00:00:00.') 
        
        t1 = TemporalTemplate(self.merge(recipe_start_point_res_exlusives,{'start-exclusive':True}))        
        self.assertEqual(len(t1.ticks),24,'There must be 24 ticks if start-exclusive is True.')
        self.assertEqual(t1.length,len(t1.ticks),'The length property must be equal to the length of ticks.')
        self.assertNotEqual(t1.ticks[0],t1.start,'The first tick must not be equal to start if start-exclusive is True.')
        self.assertEqual(t1.ticks[-1],t1.end,'The last tick must be equal to end even if start-exclusive is True.')
        self.assertEqual(t1.start,pd.to_datetime(recipe_start_point_res_exlusives['start']),'The end must be equal 2018-01-01 00:00:00.')
        self.assertEqual(t1.end,pd.to_datetime('2018-01-02'),'The end must be equal 2018-01-02 00:00:00.') 
        
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            t1 = TemporalTemplate(self.merge(recipe_start_point_res_exlusives,{'end-exclusive':False}))        
            self.assertEqual(len(t1.ticks),25,'There must be 25 ticks if end-exclusive is False.')
            self.assertEqual(t1.length,len(t1.ticks),'The length property must be equal to the length of ticks.')
            self.assertEqual(t1.ticks[0],t1.start,'The first tick must be equal to start if end-exclusive is False.')
            self.assertEqual(t1.ticks[-1],t1.end,'The last tick must be equal to end if end-exclusive is False.')
            self.assertEqual(t1.start,pd.to_datetime(recipe_start_point_res_exlusives['start']),'The end must be equal 2018-01-01 00:00:00.')
            self.assertEqual(t1.end,pd.to_datetime('2018-01-02'),'The end must be equal 2018-01-02 00:00:00.') 
            self.assertEqual(w[-1].category,SyntaxWarning )
        
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            t1 = TemporalTemplate(self.merge(recipe_start_point_res_exlusives,{'end-exclusive':True}))         
            self.assertEqual(len(t1.ticks),25,'There must be 25 ticks if end-exclusive is True.')
            self.assertEqual(t1.length,len(t1.ticks),'The length property must be equal to the length of ticks.')
            self.assertEqual(t1.ticks[0],t1.start,'The first tick must be equal to start even if end-exclusive is True.')
            self.assertEqual(t1.ticks[-1],t1.end,'The last tick must be equal to end even if end-exclusive is True when the end is not set.') 
            self.assertEqual(t1.start,pd.to_datetime(recipe_start_point_res_exlusives['start']),'The end must be equal 2018-01-01 00:00:00.')
            self.assertEqual(t1.end,pd.to_datetime('2018-01-02'),'The end must be equal 2018-01-02 00:00:00.') 
            self.assertEqual(w[-1].category,SyntaxWarning )
        
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            t1 = TemporalTemplate(self.merge(recipe_start_point_res_exlusives,{'end-exclusive':True,'start-exclusive':True}))         
            self.assertEqual(len(t1.ticks),24,'There must be 24 ticks if both start-exclusive and end-exclusive are True.')
            self.assertEqual(t1.length,len(t1.ticks),'The length property must be equal to the length of ticks.')
            self.assertNotEqual(t1.ticks[0],t1.start,'The first tick must not be equal to start even if both start-exclusive and end-exclusive are True.')
            self.assertEqual(t1.ticks[-1],t1.end,'The last tick must be equal to end even if end-exclusive is True when the end is not set.') 
            self.assertEqual(t1.start,pd.to_datetime(recipe_start_point_res_exlusives['start']),'The end must be equal 2018-01-01 00:00:00.')
            self.assertEqual(t1.end,pd.to_datetime('2018-01-02'),'The end must be equal 2018-01-02 00:00:00.') 
            self.assertEqual(w[-1].category,SyntaxWarning )
            
    def merge(self,x,y):
        z = x.copy()
        z.update(y)
        return z
    
            
if __name__ == '__main__':
    unittest.main()            
