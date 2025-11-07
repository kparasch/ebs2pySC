import json
from interface import Interface
ebs = Interface()

## delta_q_s is a dictionary with keys as the names, and values as the deltaK (integrated or not yet?)
delta_q_s =  json.load(open("./PATH/output/delta_quad_skew.json")) ## check the path

## make sure values and pySC names are for integrated quads

## map pySC corrector names to ebs control system names
mapping = json.load(open('name_mapping.json'))

names = []
trims = []
for pySC_name, trim in delta_q_s.items():
    names.append(mapping[pySC_name])
    trims.append(trim)

data = ebs.get_many(names)
for name, trim in zip(names, trims):
    data[name] += trim
ebs.set_many(data)
