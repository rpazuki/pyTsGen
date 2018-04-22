# -*- coding: utf-8 -*-
"""
Created on Sun Apr 22 18:06:38 2018

@author: roozbeh
"""


from tsGen import *
#%%
import unittest

class Test1(unittest.TestCase):
    
    def test_create_by_ticks(self):
        recipe_1 = { 
            'start': '2018-01-01',
            'end': '2018-01-02',
            'delta': '1 h'
         }
        ts1 = TemporalTemplate(recipe_1)
        const_3_5 = ConstSampler(3.5)
        
        #f = Factory(ts1,const_3_5)
        #print(f.create())
        
        const_4_5 = ConstSampler(4.0)
        
        f = Factory(ts1,const_3_5 + const_4_5 + const_4_5)
        print(f.create())
        
if __name__ == '__main__':
    unittest.main()         