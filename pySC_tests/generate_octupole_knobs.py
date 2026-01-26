from pySC import generate_SC
import matplotlib.pyplot as plt
import numpy as np
import at
import logging
import json
from pySC.utils import rdt
logger = logging.getLogger(__name__)

def calc_all(SC):
    chrom_data = at.nonlinear.chromaticity(SC.lattice.ring)[0]
    dQx = chrom_data[0,1]
    dQy = chrom_data[1,1]
    ddQx = chrom_data[0,2]
    ddQy = chrom_data[1,2]
    a_data = at.nonlinear.detuning(SC.lattice.ring)[1]
    a_xx = a_data[0,0]
    a_xy = a_data[0,1]
    a_yx = a_data[1,0]
    a_yy = a_data[1,1]
    return dQx, dQy, ddQx, ddQy, a_xx, a_xy, a_yx, a_yy

def line(k, l, m):
    xx = np.array([0,1])
    yy = (m - k * xx)/l
    return xx, yy

plt.plot([0,0],[1,1], 'k')
plt.plot([0.16], [0.34], 'bo')
# plt.xlim(0.08, 0.24)
# plt.ylim(0.28, 0.42)

plt.axhline(1./3, c='C0')

plt.plot(*line(1,-2,0), c='C1')
plt.plot(*line(1,2,1), c='C2')

plt.plot(*line(2,-2,0), c='C3')
plt.plot(*line(2,2,1), c='C4')
plt.axvline(1./4, c='C5')
plt.axhline(1./4, c='C5')

SC = generate_SC('betamodel_conf_ideal.yaml', seed=1, sigma_truncate=3)
sextupoles = [cc for cc in SC.control_arrays['sextupoles'] if 'B3L' in cc]
octupoles = [cc for cc in SC.control_arrays['octupoles'] if 'B4L' in cc]

sextupoles_idx = [SC.magnet_settings.magnets[cc].sim_index for cc in SC.magnet_arrays['sextupoles']]
octupoles_idx = [SC.magnet_settings.magnets[cc].sim_index for cc in SC.magnet_arrays['octupoles']]

IM = SC.magnet_settings.index_mapping
qd2 = [IM[ii] + '/B2L' for ii in SC.lattice.find_with_regex('^QD2')[1:-1]]
qf1 = [IM[ii] + '/B2L' for ii in SC.lattice.find_with_regex('^QF1')[1:-1]]
SC.tuning.tune.tune_quad_controls_1 = qd2
SC.tuning.tune.tune_quad_controls_2 = qf1

nominal_integrated_strengths = rdt.get_integrated_strengths_with_feeddown(SC)

quads = qd2+qf1
ref_k1 = SC.magnet_settings.get_many(quads)

for _ in range(5):
    SC.tuning.tune.correct(measurement_method='cheat', gain=1, target_qx=0.16, target_qy=0.161)
ref_2002 = SC.magnet_settings.get_many(quads)
twiss_2002 = SC.lattice.get_twiss()

for _ in range(5):
    SC.tuning.tune.correct(measurement_method='cheat', gain=1, target_qx=0.16, target_qy=0.339)
ref_2020 = SC.magnet_settings.get_many(quads)
twiss_2020 = SC.lattice.get_twiss()

for _ in range(5):
    SC.tuning.tune.correct(measurement_method='cheat', gain=1, target_qx=0.249, target_qy=0.340)
ref_4000 = SC.magnet_settings.get_many(quads)
twiss_4000 = SC.lattice.get_twiss()

for _ in range(5):
    SC.tuning.tune.correct(measurement_method='cheat', gain=1, target_qx=0.16, target_qy=0.251)
ref_0040 = SC.magnet_settings.get_many(quads)
twiss_0040 = SC.lattice.get_twiss()

SC.magnet_settings.set_many(ref_k1)

dQx_0, dQy_0, ddQx_0, ddQy_0, a_xx_0, a_xy_0, a_yx_0, a_yy_0 = calc_all(SC)
f2002_0 = rdt.fjklm(SC, 2,0,0,2, integrated_strengths=nominal_integrated_strengths,
                      twiss=twiss_2002, normalized=False)
f2020_0 = rdt.fjklm(SC, 2,0,2,0, integrated_strengths=nominal_integrated_strengths,
                      twiss=twiss_2020, normalized=False)
f4000_0 = rdt.fjklm(SC, 4,0,0,0, integrated_strengths=nominal_integrated_strengths,
                      twiss=twiss_4000, normalized=False)
f0040_0 = rdt.fjklm(SC, 0,0,4,0, integrated_strengths=nominal_integrated_strengths,
                      twiss=twiss_0040, normalized=False)


octupole_response = np.zeros([len(octupoles), 16])

delta_s = 1e-3
for ii, ss in enumerate(octupoles):
    logger.info(f'Measuring for octupole {ss}, {ii}/{len(octupoles)})')
    k0 = SC.magnet_settings.get(ss)
    SC.magnet_settings.set(ss, k0 + delta_s)
    dQx, dQy, ddQx, ddQy, a_xx, a_xy, a_yx, a_yy = calc_all(SC)
    octupole_response[ii][0] = dQx - dQx_0
    octupole_response[ii][1] = dQy - dQy_0
    octupole_response[ii][2] = ddQx - ddQx_0
    octupole_response[ii][3] = ddQy - ddQy_0
    octupole_response[ii][4] = a_xx - a_xx_0
    octupole_response[ii][5] = a_xy - a_xy_0
    octupole_response[ii][6] = a_yx - a_yx_0
    octupole_response[ii][7] = a_yy - a_yy_0
    octupole_response[ii] /= delta_s
    SC.magnet_settings.set(ss, k0)
    sidx = sextupoles_idx[ii]
    nominal_integrated_strengths['norm'][3][sidx] += delta_s
    f2002 = rdt.fjklm(SC, 2,0,0,2, integrated_strengths=nominal_integrated_strengths,
                          twiss=twiss_2002, normalized=False)
    f2020 = rdt.fjklm(SC, 2,0,2,0, integrated_strengths=nominal_integrated_strengths,
                          twiss=twiss_2020, normalized=False)
    f4000 = rdt.fjklm(SC, 4,0,0,0, integrated_strengths=nominal_integrated_strengths,
                          twiss=twiss_4000, normalized=False)
    f0040 = rdt.fjklm(SC, 0,0,4,0, integrated_strengths=nominal_integrated_strengths,
                          twiss=twiss_0040, normalized=False)
    octupole_response[ii][8] = (f2002[0].real - f2002_0[0].real)/delta_s
    octupole_response[ii][9] = (f2002[0].imag - f2002_0[0].imag)/delta_s
    octupole_response[ii][10] = (f2020[0].real - f2020_0[0].real)/delta_s
    octupole_response[ii][11] = (f2020[0].imag - f2020_0[0].imag)/delta_s
    octupole_response[ii][12] = (f4000[0].real - f4000_0[0].real)/delta_s
    octupole_response[ii][13] = (f4000[0].imag - f4000_0[0].imag)/delta_s
    octupole_response[ii][14] = (f0040[0].real - f0040_0[0].real)/delta_s
    octupole_response[ii][15] = (f0040[0].imag - f0040_0[0].imag)/delta_s
    nominal_integrated_strengths['norm'][3][sidx] -= delta_s
    #break

data = {'octupole_responses': [list(a) for a in octupole_response]}

json.dump(data, open('octupole_matrix.json','w'), indent=2)


plt.show()




# SC = generate_SC('betamodel_conf_ideal.yaml')