from pySC import generate_SC
from pySC.apps.interface import pySCOrbitInterface
from pySC.apps import measure_bba
from pySC.apps.bba import analyze_bba_data
from pySC.apps.bba import BBACode
import json
import logging

logging.getLogger('pySC.apps.bba').setLevel(logging.DEBUG)
logger = logging.getLogger(__name__)

# needs betamodel.mat
SC = generate_SC('betamodel_conf_ideal.yaml', seed=1, sigma_truncate=3)
interface = pySCOrbitInterface(SC=SC)

with open('bba_config.json','r') as fp:
    bba_config = json.load(fp)

bpm_name = "122"
one_config = bba_config[bpm_name]

generator = measure_bba(interface=interface, bpm_name=bpm_name, config=one_config,
                        shots_per_orbit=2, n_corr_steps=7, bipolar=True, skip_save=False)

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