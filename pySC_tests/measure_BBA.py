from pySC import generate_SC
from pySC.apps.interface import pySCOrbitInterface
from pySC.apps import measure_bba
from pySC.apps.bba import analyze_bba_data, get_bba_analysis_data
from pySC.apps.bba import BBACode
import json
import logging
import matplotlib.pyplot as plt
import numpy as np

logging.getLogger('pySC.apps.bba').setLevel(logging.DEBUG)
logger = logging.getLogger(__name__)

# needs betamodel.mat
SC = generate_SC('betamodel_conf_ideal.yaml', seed=1, sigma_truncate=3)
interface = pySCOrbitInterface(SC=SC)

with open('bba_config.json','r') as fp:
    bba_config = json.load(fp)

bpm_name = "srdiag/beam-position/c05-05"
one_config = bba_config[bpm_name]

generator = measure_bba(interface=interface, bpm_name=bpm_name, config=one_config,
                        shots_per_orbit=2, n_corr_steps=7, bipolar=True, skip_save=True)

for code, measurement_object in generator:
#    logger.debug(f"Got code: {code.name}")
    if code == BBACode.HORIZONTAL_DONE:
        offset_h, offset_h_err = analyze_bba_data(measurement_object.H_data)
        logger.info(f"BBA offset H = {offset_h*1e6:.1f} +- {offset_h_err*1e6:.1f} μm.")
    if code == BBACode.VERTICAL_DONE:
        offset_v, offset_v_err = analyze_bba_data(measurement_object.V_data)
        logger.info(f"BBA offset V = {offset_v*1e6:.1f} +- {offset_v_err*1e6:.1f} μm.")

## Summary
logger.info("")
logger.info(f"Summary for BPM {bpm_name}:")
logger.info(f"  BBA offset H = {offset_h*1e6:.2f} +- {offset_h_err*1e6:.2f} μm.")
logger.info(f"  BBA offset V = {offset_v*1e6:.2f} +- {offset_v_err*1e6:.2f} μm.")
logger.info(f"Saved H. data to {measurement_object.H_data.original_save_path}")
logger.info(f"Saved V. data to {measurement_object.V_data.original_save_path}")

# import matplotlib.pyplot as plt
# plt.figure()
# 

def plot_data(data):
    fig1, axes1 = plt.subplot_mosaic(mosaic=[['A','A','S','S'],['A','A','C','C']])
    bpm_pos_h, orbits_h, slopes_h, center_h, final_mask_h, off_h = get_bba_analysis_data(data)
    
    xp_min = np.min(bpm_pos_h)*1e6
    xp_max = np.max(bpm_pos_h)*1e6
    for ii in range(2):
        for kk in range(len(orbits_h[0, ii, :])):
            p0 = np.polyfit(bpm_pos_h[:, ii]*1e6, orbits_h[:, ii, kk]*1e6, 1)
            xp = np.linspace(xp_min, xp_max, 10)
            yp = p0[0]*xp + p0[1]
            axes1['A'].plot(xp, yp, '-', c='C0' if final_mask_h[kk] else 'C1', alpha=0.3)
    
    for ii in range(2):
        for kk in range(len(bpm_pos_h[:, ii])):
            yy = orbits_h[kk, ii] * 1e6
            xx = np.ones_like(yy) * bpm_pos_h[kk, ii] * 1e6
            axes1['A'].plot(xx[final_mask_h], yy[final_mask_h], '.', c='C0')
            axes1['A'].plot(xx[~final_mask_h], yy[~final_mask_h], '.', c='C1')
    
    axes1['A'].set_xlabel('BPM position [μm]')
    axes1['A'].set_ylabel('Modulation [μm]')
    axes1['A'].grid()
    
    bpm_numbers = np.arange(len(final_mask_h))
    axes1['S'].plot(bpm_numbers[final_mask_h], slopes_h[final_mask_h], '.', c='C0')
    axes1['S'].plot(bpm_numbers[~final_mask_h], slopes_h[~final_mask_h], '.', c='C1')
    axes1['S'].set_xlabel('BPM number')
    axes1['S'].set_ylabel('Slope')
    axes1['S'].grid()
    
    axes1['C'].plot(bpm_numbers[final_mask_h], center_h[final_mask_h]*1e6, '.', c='C0')
    axes1['C'].plot(bpm_numbers[~final_mask_h], center_h[~final_mask_h]*1e6, '.', c='C1')
    axes1['C'].set_xlabel('BPM number')
    axes1['C'].set_ylabel('Center [μm]')
    axes1['C'].grid()
    fig1.tight_layout()
    return fig1, axes1

figh, axh = plot_data(measurement_object.H_data)
figv, axv = plot_data(measurement_object.V_data)

plt.show()

# bpm1 with sh1a
# bpm2 with sd1a
# bpm3 with sd1b
# bpm5 with sh2b