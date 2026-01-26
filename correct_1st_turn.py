from pySC import generate_SC
from pySC.apps.interface import pySCInjectionInterface
from interface import InterfaceInjection
from pySC.apps import orbit_correction
from pySC import ResponseMatrix
import numpy as np
import json

n_turns = 1
apply = True
ebs = InterfaceInjection()
ebs.n_turns = n_turns

ref_x, ref_y = ebs.get_ref_orbit()

reference = np.concat((ref_x.flatten(order='F'), ref_y.flatten(order='F')))

response_matrix = ResponseMatrix.from_json(f'ideal_{n_turns}turn_orm.json')
mapping = json.load(open('name_mapping.json'))
response_matrix.input_names = [mapping[pySC_name] for pySC_name in response_matrix.input_names]

print()

x1, y1 = ebs.get_orbit()
print(f'RMS before H: {np.std(x1-ref_x)*1e6} μm, V: {np.std(y1-ref_y)*1e6} μm')
trims = orbit_correction(interface=ebs, response_matrix=response_matrix, reference=reference,
                         method='svd_values', parameter=64, apply=apply,
                         plane='H')
trims = orbit_correction(interface=ebs, response_matrix=response_matrix, reference=reference,
                         method='svd_values', parameter=64, apply=apply,
                         plane='V')
#print(trims)

x2, y2 = ebs.get_orbit()
print(f'RMS after H: {np.std(x2-ref_x)*1e6} μm, V: {np.std(y2-ref_y)*1e6} μm')



# ebs = InterfaceInjection()
# x,y = ebs.get_orbit()
# xr,yr = ebs.get_ref_orbit()
# fig = plt.figure()
# ax1 = fig.add_subplot(211)
# ax2 = fig.add_subplot(212)
# ax1.plot(1e6*(x-xr))
# ax2.plot(1e6*(y-yr))
# ax1.set_ylabel('x [μm]')
# ax2.set_ylabel('y [μm]')
# plt.show()
