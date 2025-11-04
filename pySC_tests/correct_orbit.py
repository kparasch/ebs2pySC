from pySC import generate_SC
from pySC.apps.interface import pySCOrbitInterface, get_ref_orbit
from pySC.apps import orbit_correction
from pySC import ResponseMatrix
import numpy as np

# needs betamodel.mat
SC = generate_SC('betamodel_conf_ideal.yaml', seed=1, sigma_truncate=3)

interface = pySCOrbitInterface(SC=SC)
interface.set('6/B1L', 13.7e-6)
interface.set('175/B1L', 22e-6)
interface.set('959/A1L', 9e-6)

ref_x, ref_y = interface.get_ref_orbit()
# ref_x, ref_y = SC.bpm_system.capture_orbit(use_design=True)

reference = np.concat((ref_x.flatten(order='F'), ref_y.flatten(order='F')))

response_matrix = ResponseMatrix.from_json('ideal_orm.json')

# corector_names are in response_matrix.input_names
# bpmnames are in response_matrix.outputput_names
# response_matrix.outputput_names is a list that repeats the bpm names for horizontal and vertical,
# while response_matrix.input_names are in the form "magnet_name/B1L" or "magnet_name/A1L",
# I think the best would be to replace at this point the pySC name to the control system name in the response_matrix with a mapping.

#######################
print()

x1, y1 = interface.get_orbit()
print(f'RMS before H: {np.std(x1-ref_x)*1e6} μm, V: {np.std(y1-ref_y)*1e6} μm')
trims = orbit_correction(interface=interface, response_matrix=response_matrix, reference=reference, method='micado', parameter=3, apply=True)

print(trims)

x2, y2 = interface.get_orbit()
print(f'RMS after H: {np.std(x2-ref_x)*1e6} μm, V: {np.std(y2-ref_y)*1e6} μm')

#######################

print()
interface.set_many({'6/B1L': 13.7e-6, '175/B1L': 0, '959/A1L': 0})

my_corrs = ['175/B1L']
print(f'Correct now only with correctors {my_corrs}, but do not apply')
response_matrix.disable_all_inputs_but(my_corrs)
trims = orbit_correction(interface=interface, response_matrix=response_matrix, reference=reference, method='micado', parameter=1, apply=False)
response_matrix.enable_all_inputs()
print(trims)
