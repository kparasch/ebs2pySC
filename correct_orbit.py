from interface import Interface
from pySC.tuning import orbit_correction #function doesn't exist yet
from pySC.tuning.response_matrix import ResponseMatrix

ebs = Interface()

# either we load response matrix here from file, 
# or we get it directly from pySC object (maybe it is unnecessary to fully load pySC)
RM = ResponseMatrix("orm.data") 

# get corrector names from:
# 1) load from file 
# 2) pySC
# 3) response matrix "metadata"
# 4) perhaps the best is to get it from ebs interface?
HCORR = []
VCORR = []
CORR = []


## Proposed arguments of orbit correction:
## get_orbit: function that returns the orbit of the machine
## settings: object that contains functions "get", "set", "get_many", "set_many"
## response_matrix: object that contains the response matrix and the corrector names
## correctors: list of corrector names to be used in the correction (the more I write this script the more sense it makes to attach CORR to response_matrix)
## method: method to be used in the correction (svd_cutoff, tikhonov, micado)
## parameter: parameter to be used in the correction (svd threshold, tikhonov alpha, micado number of correctors)
trims = orbit_correction(get_orbit=ebs.get_orbit, settings=ebs, response_matrix=RM, correctors=CORR, method='svd_cutoff', parameter=1e-4, apply=True)
trims = orbit_correction(get_orbit=ebs.get_orbit, settings=ebs, response_matrix=RM, correctors=CORR, method='tikhonov', parameter=10, apply=True)
trims = orbit_correction(get_orbit=ebs.get_orbit, settings=ebs, response_matrix=RM, correctors=CORR, method='micado', parameter=3, apply=True)

# or something like:
# trims = orbit_correction(get_orbit=ebs.get_orbit, settings=ebs, response_matrix=RM, correctors=CORR, method='tikhonov', parameter=10, apply=False)
# ebs.set_many(trims)