# -*- coding: utf-8 -*-
"""
Created on Sun Apr 22 14:41:48 2018

@author: roozbeh
"""
from tsGen import TemporalTemplate
from tsGen import TemporalJitter

#%%
from scipy.stats import poisson
from scipy.stats import norm
##########################################
# Generate
#
recipe_1 = { 
            'start': '2018-01-01',
            'end': '2018-01-02',
            'delta': '1 h'
         }

ts1 = TemporalTemplate(recipe_1)
print('ts1:\n%s\n\n' % ts1)

recipe_2 = { 
            'start': '2018-01-01',
            'length': 25,
            'delta': '1 h'
         }

ts2 = TemporalTemplate(recipe_2)
print('ts2:\n%s\n\n' % ts2)

recipe_3 = { 
            'end': '2018-01-02',
            'length': 25,
            'delta': '1 h'
         }

ts3 = TemporalTemplate(recipe_3)
print('ts3:\n%s\n\n' % ts3)

recipe_4 = { 
            'start': '2018-01-01',
            'end': '2018-01-02',
            'length': 25
         }

ts4 = TemporalTemplate(recipe_4)
print('ts4:\n%s\n\n' % ts4)


recipe_5 = { 
            'start': '2018-01-01',
            'points': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24],
            'res': 'h'
         }

ts5 = TemporalTemplate(recipe_5)
print('ts5:\n%s\n\n' % ts5)

recipe_6 = { 
            'start': '2018-01-01',
            'points_delta': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            'res': 'h'
         }

ts6 = TemporalTemplate(recipe_6)
print('ts6:\n%s\n\n' % ts6)


####################################
# Operations

print(ts1[4:8])

print(ts1[::-1])

for i in ts1:
    print('item: %s' % i)
    
print('\nlen: %d \n\n' % len(ts1))

print(ts1 + ts2) # add by another object
print('\n\n')
print(ts1 + '5 h')# add by delta
print('\n\n')
print(ts1 + '2 D')# add by delta 
print('\n\n')
print('5 m' + ts1 )# add to delta
print('\n\n')
print(ts1 + '5 m' + ts2)# first add by delta and then by another
print('\n\n')

np.random.seed(seed=42)
        
mu = 0.6
rv = poisson(mu)        
j = TemporalJitter(pdf=rv,resolution='m')
print(ts1 + j)# add by a poissonian jitter in Minutes

print('\n\n')

j2 = TemporalJitter(pdf=rv,resolution='D')
print(ts1 + j2)# add by a poissonian jitter in Days

print('\n\n')

j2 = TemporalJitter(pdf=rv,resolution='D')
print(ts1 + j + j2)# add by a two jitters
print('\n\n')

print(ts1 - '5 h')# subtract by delta
print('\n\n')

############################################
# subtract from, delta cuase error
#print('5 h' - ts1 )

print(ts1 * 2)#multiply by two add one ticks between all consecutives
print('\n\n')

print(3 * ts1)#multiply by three add two ticks between all consecutives
print('len the main %d , len after multipling by three:%d' % (len(ts1), len(3*ts1)))
print('\n\n')

np.random.seed(seed=42)
rv = norm(0,10)        
j3 = TemporalJitter(pdf=rv,resolution='m')
print(ts1 * j3)#multipliy by a Gaussian jitter, add random number of ticks, sampled from Gaussian

print('\n\n')
print(ts1 >> 2)#expand by 2 as ratio

print('\n\n')
print(ts1 << 0.5)#shrink by half as ratio

print('\n\n')
print(ts1.zoom(3.5))#Zoom out by ratio 3.5

print('\n\n')
print(ts1.zoom(1.0/3))#Zoom in by ratio 0.333

print('\n\n')
print(ts1.drop(10))#Drop the first 10 elements
print('The start after droping 10 ticks: %s' % ts1.drop(10).start)#
print('The end after droping 10 ticks: %s' % ts1.drop(10).end)#


print('\n\n')
print(ts1.drop_r(10))#Drop the last 10 elements
print('The start after droping 10 ticks: %s' % ts1.drop_r(10).start)#
print('The end after droping 10 ticks: %s' % ts1.drop_r(10).end)#



print('\n\n')
print(ts1 // 10)#Randomly drop 10 elements from within
print('The start after randomly removing 10 ticks is always the start of the orginal: %s' % (ts1 // 10).start)#
print('The start after randomly removing 10 ticks is always the end of the orginal: %s' % (ts1 // 10).end)#
