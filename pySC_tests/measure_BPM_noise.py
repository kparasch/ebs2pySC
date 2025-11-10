import pySC
from pySC.apps.interface import pySCOrbitInterface
from pySC.apps import measure_ORM, orbit_correction
from pySC.apps.codes import ResponseCode
import logging
import numpy as np
import time


pySC.disable_pySC_rich()

#logging.getLogger('pySC.apps.response').setLevel(logging.DEBUG)
logger = logging.getLogger(__name__)

# needs betamodel.mat
SC = pySC.generate_SC('betamodel_conf_ideal.yaml', seed=1, sigma_truncate=3)
interface = pySCOrbitInterface(SC=SC)

def get_average_orbit(n_orbits=10):
    orbit_x, orbit_y = interface.get_orbit()
    all_orbit_x = np.zeros((len(orbit_x), n_orbits))
    all_orbit_y = np.zeros((len(orbit_y), n_orbits))

    all_orbit_x[:, 0] = orbit_x
    all_orbit_y[:, 0] = orbit_y
    for ii in range(1, n_orbits):
        all_orbit_x[:, ii], all_orbit_y[:, ii] = interface.get_orbit()

    mean_orbit_x = np.mean(all_orbit_x, axis=1)
    mean_orbit_y = np.mean(all_orbit_y, axis=1)
    std_orbit_x = np.std(all_orbit_x, axis=1)
    std_orbit_y = np.std(all_orbit_y, axis=1)
    return mean_orbit_x, mean_orbit_y, std_orbit_x, std_orbit_y


import time
start_time = time.time()

n_orbits = 180

mean_orbit_x, mean_orbit_y, std_orbit_x, std_orbit_y = get_average_orbit(n_orbits=n_orbits)


end_time = time.time()
executing_time = end_time - start_time

print(f"\ntime: {executing_time:.3f} seconds")

import h5py
import os
os.makedirs("./data", exist_ok=True)
with h5py.File("./data/measured_BPM_noise_loco.h5", "w") as f:
    f.create_dataset("mean_orbit_x", data=mean_orbit_x)
    f.create_dataset("mean_orbit_y", data=mean_orbit_y)
    f.create_dataset("Noise_BPMx", data=std_orbit_x)
    f.create_dataset("Noise_BPMy", data=std_orbit_y)
    f.attrs["n_orbits"] = n_orbits
    f.attrs["execution_time_sec"] = executing_time