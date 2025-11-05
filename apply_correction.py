#!/usr/bin/env python
# coding: utf-8

# In[3]:


import json
from interface import Interface
ebs = Interface()
delta_q_s =  json.load(open("./PATH/output/delta_quad_skew.json")) ##

name = SC.magnet_settings.index_mapping[elem_ind]+comp ##

names = []
trims = []
data = ebs.get_many(names)

for name, trim in zip(names, trims):
    data[name] += trim

ebs.set_many(data)

