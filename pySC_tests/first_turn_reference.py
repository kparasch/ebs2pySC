from pySC import generate_SC
import numpy as np
import matplotlib.pyplot as plt

SC = generate_SC('betamodel_conf_ideal.yaml', seed=1, sigma_truncate=3)


# -15 mm bump
I1 = 2081.649271
I2 = 1771.630745
I3 = 1779.133870
I4 = 2072.310939

i2k1 = 2.3e-3/2e3
i2k2 = 2.28e-3/2e3
i2k3 = 2.27e-3/2e3
i2k4 = 2.31e-3/2e3

k1 = i2k1*I1
k2 = i2k2*I2
k3 = i2k3*I3
k4 = i2k4*I4

kicker_idx = SC.lattice.find_with_regex('DR_K')
SC.lattice.ring[kicker_idx[0]].PolynomB[0] = k3
SC.lattice.ring[kicker_idx[1]].PolynomB[0] = k4
SC.lattice.ring[kicker_idx[2]].PolynomB[0] = k1
SC.lattice.ring[kicker_idx[3]].PolynomB[0] = k2

x0, y0 = SC.bpm_system.capture_orbit(use_design=True)
x, y = SC.bpm_system.capture_orbit()
plt.plot((x-x0)*1e3)
plt.plot((y-y0)*1e3)

print(f"First bpm reference for 15mm bump: {(x[0]-x0[0])*1e3} mm")
plt.show()