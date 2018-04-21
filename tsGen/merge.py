# -*- coding: utf-8 -*-
"""
Created on Fri Apr 20 20:11:30 2018

@author: roozbeh
"""
#%%
import numpy as np

def merge(temporal1,temporal2):
    start = min((temporal1.start,temporal2.start))
    end = max((temporal1.end,temporal2.end))
    joined_ticks = np.concatenate((temporal1.ticks,temporal2.ticks))
    ticks = np.sort(np.unique(joined_ticks))
    return TemporalTemplate(recipe=None, ticks=ticks)