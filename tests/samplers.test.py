# -*- coding: utf-8 -*-
"""
Created on Sun Apr 22 18:06:38 2018

@author: roozbeh
"""


from tsGen import *
#%%
import unittest
import numpy as np

class Test1(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(Test1, self).__init__(*args, **kwargs)
        recipe_1 = { 
            'start': '2018-01-01',
            'end': '2018-01-02',
            'delta': '1 h'
         }
        self.ts = TemporalTemplate(recipe_1)
        
    def test_ConstSampler(self):
        const_3_5 = ConstSampler(3.5)
        f1 = Factory(self.ts,const_3_5)
        for i in f1.create():
            self.assertEqual(i,const_3_5.value,'All the values must be equal to the constant.')
            
        
    def test_ConstSampler_sum(self):
        const_3_5 = ConstSampler(3.5)
                    
        const_4_5 = ConstSampler(4.0)
        #Test Add two
        f1 = Factory(self.ts,const_3_5 + const_4_5)
        for i in f1.create():
            self.assertEqual(i,const_3_5.value + const_4_5.value,'All the values must be equal to the constant.')
            
        f2 = Factory(self.ts,const_3_5 + const_4_5 + const_3_5)
        for i in f2.create():
            self.assertEqual(i,2*const_3_5.value + const_4_5.value,'All the values must be equal to the constant.')
           
    def test_CategoriesSampler(self):
        cat = CategoriesSampler(['a','b','c'])
        f2 = Factory(self.ts,cat)
        items = np.unique(f2.create().values)        
        self.assertListEqual(items.tolist(),['a','b','c'],'All the categories must come from the same result.')
        
    def test_CategoriesSampler_by_probs(self):
        np.random.seed(seed=42)
        cat = CategoriesSampler(['a','b','c'],probs=[.2,0.4,0.4])
        f2 = Factory(self.ts,cat)
        items = np.unique(f2.create().values)            
        self.assertListEqual(items.tolist(),['a','b','c'],'All the categories must come from the same result.')
        
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
        steps = StepSampler([1.0,2.0,3.0,4.0])
        
        f = Factory(ts1,const_3_5 + (const_4_5 + const_4_5 + steps))
        #print(f.create())
        
        cat = CategoriesSampler(['a','b','c'])
        f2 = Factory(ts1,cat)
        print(f2.create())
        
if __name__ == '__main__':
    unittest.main()         