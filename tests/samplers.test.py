# -*- coding: utf-8 -*-
"""
Created on Sun Apr 22 18:06:38 2018

@author: roozbeh
"""


from tsGen import *
#%%
import unittest
import numpy as np
from scipy.stats import poisson
from scipy.stats import norm
import math

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
        np.random.seed(seed=42)
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
        
    def test_StepSampler(self):
        np.random.seed(seed=42)
        steps = StepSampler([1.1, 2.2, 3.3])
        f1 = Factory(self.ts,steps)
        items = np.unique(f1.create().values)        
        self.assertListEqual(items.tolist(),[1.1, 2.2, 3.3],'All the steps must come from the same result.')
        
    def test_StepSampler_by_probs(self):
        np.random.seed(seed=42)
        steps = StepSampler([1.1, 2.2, 3.3],probs=[.2,0.4,0.4])
        f1 = Factory(self.ts,steps)
        items = np.unique(f1.create().values)        
        self.assertListEqual(items.tolist(),[1.1, 2.2, 3.3],'All the steps must come from the same result.')
        
    def test_PDFSampler(self):
        np.random.seed(seed=42)
        pdf = norm(0,10) 
        gaussian = PDFSampler(pdf)
        f1 = Factory(self.ts,gaussian)
        series = f1.create()
        self.assertEqual(series[0],4.9671415301123272)
        
        np.random.seed(seed=42)
        mu = 1.6
        pdf = poisson(mu)
        pois =  PDFSampler(pdf)
        
        f2 = Factory(self.ts,pois)
        series = f2.create()
        self.assertEqual(series[0],3.0)
        self.assertEqual(series[-1],0.0)
        
        f3 = Factory(self.ts,pois + gaussian)
        series = f3.create()
        
    def s(self,idx,x,tick): 
        return math.sin(2.0*math.pi*x)
    def test_FunctionSampler(self):
       
        sin1 = FunctionSampler(self.s)
        f1 = Factory(self.ts,sin1)
        series = f1.create()
       
        self.assertEqual(series[0],0.0,'The first value for sin must be zero')
        self.assertEqual(series[6],1.0,'The 7th value for sin must be 1')
        
        sin2 = FunctionSampler(func= lambda idx,x,tick: math.sin(2.0*math.pi*x))        
        f2 = Factory(self.ts,sin2)
        series = f2.create()
        self.assertEqual(series[0],0.0,'The first value for sin must be zero')
        self.assertEqual(series[6],1.0,'The 7th value for sin must be 1')
        
        line = FunctionSampler(func= lambda idx,x,tick: 2*x + 3.0)       
        f3 = Factory(self.ts,line)
        series = f3.create()
        self.assertEqual(series[0],3.0,'The first value for the line must be 3')
        self.assertEqual(series[12],4.0,'The 14th value for the line must be 4')
        self.assertEqual(series[-1],5.0,'The last value for the line must be 5')
        
if __name__ == '__main__':
    unittest.main()         