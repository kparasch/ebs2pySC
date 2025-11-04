from pySC import generate_SC
from pySC.apps.interface import pySCOrbitInterface
from pySC.apps import measure_bba
from pySC.apps.bba import analyze_bba_data
from pySC.tuning.orbit_bba import get_slopes_center, reject_bpm_outlier, reject_center_outlier, reject_slopes, get_offset
from pySC import ResponseMatrix
import numpy as np
import json
import logging

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
    print(code.name)

## Analysis
offset_h, offset_h_err = analyze_bba_data(measurement_object.H_data)
print(f"BBA offset H = {offset_h*1e6:.1f} +- {offset_h_err*1e6:.1f} μm.")