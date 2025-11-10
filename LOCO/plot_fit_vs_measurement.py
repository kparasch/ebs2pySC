import at    
from pyLOCO.pyloco import plot_data
import h5py
import numpy as np
import pySC
from pySC.apps.interface import pySCOrbitInterface
import logging
import numpy as np
import time
from pySC.tuning.response_measurements import measure_RFFrequencyOrbitResponse
from pySC.apps import measure_ORM


#logging.getLogger('pySC.apps.response').setLevel(logging.DEBUG)
logger = logging.getLogger(__name__)


# --- Load Measurments ---
with h5py.File("/machfs/MDT/2025/2025_11_10/ebs2pySC/data/ORM_for_pyLOCO_20251110_174636.h5", "r") as f:
    measured_orm = np.array(f["response_matrix"])  # in meter [BPMs X Cor]
    delta_correctors = np.array(f["full_delta"])

with h5py.File("/machfs/MDT/2025/2025_11_10/ebs2pySC/data/measured_dispersion_loco.h5", "r") as f:  # in meter
    measured_eta_x_ = np.array(f["measured_eta_x"])
    measured_eta_y_ = np.array(f["measured_eta_y"])
    rf_full_step = np.array(f.attrs["rf_full_step"])


ring = at.load_lattice('/operation/beamdyn/optics/sr/theory/betamodel.mat', use='betamodel')
ring.disable_6d()
elements_ind = at.get_refpts(ring, "*")
_, _, twiss = at.get_optics(ring, elements_ind)

ring_pyloco = at.load_lattice('/machfs/MDT/2025/2025_11_10/ebs2pySC/output/ring_pyloco.mat', use='ring')
elements_ind = at.get_refpts(ring_pyloco, "*")

print('Lattice tune after loco :' , at.get_tune(ring_pyloco))
_, _, twiss_err = at.get_optics(ring_pyloco, elements_ind)
s_pos = twiss_err.s_pos
bx = (twiss_err.beta[:, 0]) / twiss.beta[:, 0]
by = (twiss_err.beta[:, 1]) / twiss.beta[:, 1]
plot_data(s_pos, bx, "s [m]", r"$\Delta\beta_x / \beta_x$ ", "Horizontal beta beating")
plot_data(s_pos, by, "s [m]", r"$\Delta\beta_y / \beta_y$ ", "Vertical beta beating")

# use pySC to measure dispersion and ORM on model

# needs ring_pyLOCO.mat
SC = pySC.generate_SC('/machfs/MDT/2025/2025_11_10/ebs2pySC/pySC_tests/betamodel_conf_fitted.yaml', seed=1, sigma_truncate=3)
interface = pySCOrbitInterface(SC=SC)

eta =  measure_RFFrequencyOrbitResponse(SC, delta_frf =200, normalize = False, bipolar=True)

indices = at.get_uint32_index(ring_pyloco, 'S[FIJ]2A')

corrector_names= [str(int(idx)) + '/B1L' for idx in indices] + [str(int(idx)) + '/A1L' for idx in indices]

generator = measure_ORM(interface=interface, corrector_names=corrector_names, delta=100e-6,
                        shots_per_orbit=1, bipolar=True, skip_save=True)

for code, measurement in generator:
    logger.info(f"{measurement.last_number+1}/{len(corrector_names)}, (code={code.name}), last_corrector={measurement.last_input}")

ORM_fit = measurement.response_data.not_normalized_response_matrix

import matplotlib.pyplot as plt

fig, ax = plt.subplots(nrows=2)
ax[0].plot(measured_eta_x_, label='measured')
ax[0].plot(eta[0:320], label='fitted')
ax[0].set_title('hor dispersion')
ax[0].legend()
ax[1].plot(measured_eta_y_, label='measured')
ax[1].plot(eta[320:640], label='fitted')
ax[1].set_title('ver dispersion')
ax[1].legend()


fig, ax = plt.subplots()
ax.plot(measured_orm.flatten(), label='measured')
ax.plot(ORM_fit.flatten(), label='fitted')
ax.legend()

plt.show()