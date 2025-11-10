import json
from interface import Interface
import numpy as np
ebs = Interface()
delta_q_s =  json.load(open("./LOCO/output/quad_skew_deltas_lengths.json")) ##

# Normal quads
normal_deltas = delta_q_s["normal_quads"]["delta"]
normal_lengths = delta_q_s["normal_quads"]["length"]

# Skew quads
skew_deltas = delta_q_s["skew_quads"]["delta"]
skew_lengths = delta_q_s["skew_quads"]["length"]


mapping = json.load(open("name_mapping.json"))

pySC_names_normal = [name+"/B2L" for name in normal_deltas.keys()]
pySC_names_skew = [name+"/A2L" for name in skew_deltas.keys()]

trim_normal = np.array(list(normal_deltas.values())) * np.array(list(normal_lengths.values()))
trim_skew   = np.array(list(skew_deltas.values()))   * np.array(list(skew_lengths.values()))

names = []
trims = []

for pySC_name , trim in zip(pySC_names_normal, trim_normal):
    names.append(mapping[pySC_name])
    trims.append(trim)

for pySC_name, trim in zip(pySC_names_skew, trim_skew):
    names.append(mapping[pySC_name])
    trims.append(trim)

data = ebs.get_many(names)

for name, trim in zip(names, trims):
    data[name] += trim

#ebs.set_many(data)

