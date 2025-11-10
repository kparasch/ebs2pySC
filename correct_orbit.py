from interface import Interface
from pySC.apps import orbit_correction #function doesn't exist yet
from pySC import ResponseMatrix
import json
import numpy as np


apply=False

ebs = Interface()
# load response matrix from file 
RM = ResponseMatrix.from_json("ideal_orm.json") 

## map pySC corrector names to ebs control system names
mapping = json.load(open('name_mapping.json'))
RM.input_names = [mapping[pySC_name] for pySC_name in RM.input_names]

reference_x, reference_y = ebs.get_ref_orbit()
reference = np.concat((reference_x.flatten(order='F'), reference_y.flatten(order='F')))


trims = orbit_correction(interface=ebs, response_matrix=RM, reference=reference, method='svd_cutoff', parameter=1e-3, apply=apply)
#trims = orbit_correction(interface=ebs, response_matrix=RM, method='svd_values', parameter=300, apply=apply)
print(trims)

trims = orbit_correction(interface=ebs, response_matrix=RM, reference=reference, method='micado', parameter=1, apply=False)
print(f'Micado trims: {trims}')