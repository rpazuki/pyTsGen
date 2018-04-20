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
import unittest

 
class TestRecipeSpecs(unittest.TestCase):
    def test_recipe_without_start_end(self):
        recipe_without_start_end = { 
            'length': 100
        }        
        with self.assertRaises(ValueError):
            TemporalTemplate(recipe_without_start_end)
            
            
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
            
if __name__ == '__main__':
    unittest.main()            
