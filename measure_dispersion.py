from interface import Interface
import numpy as np
import time

ebs=Interface()

def get_average_orbit(n_orbits=10):
    orbit_x, orbit_y = ebs.get_orbit()
    all_orbit_x = np.zeros((len(orbit_x), n_orbits))
    all_orbit_y = np.zeros((len(orbit_y), n_orbits))

    all_orbit_x[:, 0] = orbit_x
    all_orbit_y[:, 0] = orbit_y
    for ii in range(1, n_orbits):
        all_orbit_x[:, ii], all_orbit_y[:, ii] = ebs.get_orbit()

    mean_orbit_x = np.mean(all_orbit_x, axis=1)
    mean_orbit_y = np.mean(all_orbit_y, axis=1)
    std_orbit_x = np.std(all_orbit_x, axis=1)
    std_orbit_y = np.std(all_orbit_y, axis=1)
    return mean_orbit_x, mean_orbit_y, std_orbit_x, std_orbit_y


import time
start_time = time.time()

dt = 5
n_orbits = 10
delta_rf = 200
step = delta_rf/2

print("setting the RF down")
frequency = ebs.get_rf_main_frequency()
ebs.set_rf_main_frequency(frequency - step)

mean_orbit_x_1, mean_orbit_y_1, _,_ = get_average_orbit(n_orbits=n_orbits)

print("setting the RF up")
ebs.set_rf_main_frequency(frequency + step)
time.sleep(dt)

mean_orbit_x_2, mean_orbit_y_2, _,_ = get_average_orbit(n_orbits=n_orbits)

mean_orbit_x = mean_orbit_x_2 - mean_orbit_x_1
mean_orbit_y = mean_orbit_y_2 - mean_orbit_y_1

print("setting the RF back ..")
ebs.set_rf_main_frequency(frequency)

end_time = time.time()
executing_time = end_time - start_time

print(f"\ntime: {executing_time:.3f} seconds")


import h5py
import os
os.makedirs("./data", exist_ok=True)
with h5py.File("./data/measured_dispersion_loco.h5", "w") as f:
    f.create_dataset("measured_eta_x", data=mean_orbit_x)
    f.create_dataset("measured_eta_y", data=mean_orbit_y)
    f.attrs["n_orbits"] = n_orbits
    f.attrs["dt"] = dt
    f.attrs["rf_full_step"] = delta_rf
    f.attrs["execution_time_sec"] = executing_time