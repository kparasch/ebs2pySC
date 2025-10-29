from interface import Interface
from pySC.apps import orbit_correction #function doesn't exist yet
from pySC import ResponseMatrix

ebs = Interface()

# either we load response matrix here from file, 
# or we get it directly from pySC object (maybe it is unnecessary to fully load pySC)
RM = ResponseMatrix.from_json("ideal_orm.json") 

## map pySC corrector names to ebs control system names
# import yaml
# mapping = yaml.safe_load('pySC_to_ebs_names.yaml')
# RM.input_names = [mapping[pySC_name] for pySC_name in RM.input_names]


## Proposed arguments of orbit correction:
## get_orbit: function that returns the orbit of the machine
## settings: object that contains functions "get", "set", "get_many", "set_many"
## response_matrix: object that contains the response matrix and the corrector names
## correctors: list of corrector names to be used in the correction (the more I write this script the more sense it makes to attach CORR to response_matrix)
## method: method to be used in the correction (svd_cutoff, tikhonov, micado)
## parameter: parameter to be used in the correction (svd threshold, tikhonov alpha, micado number of correctors)
trims = orbit_correction(interface=ebs, response_matrix=RM, method='svd_cutoff', parameter=1e-4, apply=True)
trims = orbit_correction(interface=ebs, response_matrix=RM, method='tikhonov', parameter=10, apply=True)
trims = orbit_correction(interface=ebs, response_matrix=RM, method='micado', parameter=3, apply=True)

# or something like this: (especially if we use dedicated tango host to set all correctors at once)
# trims = orbit_correction(get_orbit=ebs.get_orbit, settings=ebs, response_matrix=RM, correctors=CORR, method='tikhonov', parameter=10, apply=False)
# ebs.set_many(trims)