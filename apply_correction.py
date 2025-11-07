#!/usr/bin/env python
# coding: utf-8

# In[3]:


import json
from interface import Interface
import numpy as np
ebs = Interface()
delta_q_s =  json.load(open("./pySC_tests/LOCO/output/quad_skew_deltas_lengths.json")) ##

# Normal quads
normal_deltas = delta_q_s["normal_quads"]["delta"]
normal_lengths = delta_q_s["normal_quads"]["length"]

# Skew quads
skew_deltas = delta_q_s["skew_quads"]["delta"]
skew_lengths = delta_q_s["skew_quads"]["length"]


name = SC.magnet_settings.index_mapping[elem_ind]+comp ##


trim_normal = np.array(list(normal_deltas.values())) * np.array(list(normal_lengths.values()))
trim_skew   = np.array(list(skew_deltas.values()))   * np.array(list(skew_lengths.values()))

names = []
trims = []
data = ebs.get_many(names)

for name, trim in zip(names, trims):
    data[name] += trim

ebs.set_many(data)

