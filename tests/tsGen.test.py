# -*- coding: utf-8 -*-
"""
Created on Fri Apr 20 11:14:57 2018

@author: roozbeh
"""

from tsGen import TemporalTemplate 
#%%
import unittest

 
class Test1(unittest.TestCase):
    
    def test_recipe_without_length2(self):
        recipe = { 
            'start': '2018-01-01',
            'end': '2018-01-02',
            'delta': '1 h'
         }        
        ts = TemporalTemplate(recipe)        
        self.assertEqual(len(ts.ticks),25, 'There must be 25 ticks for 24 hours period with delta 1 h.')
            
if __name__ == '__main__':
    unittest.main()            
