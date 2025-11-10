#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import h5py
import numpy as np
import at
from pyLOCO.helpers import load_config
from pyLOCO.pyloco import remove_bad_bpms, plot_matrices
from pyLOCO.response_matrix import response_matrix
from pyloco_config import FitInitConfig, RMConfig, fixed_parameters

# --- Load configuration ---
config_path = os.path.abspath("pyloco_config.py")
load_config(config_path=config_path)

# --- Load lattice ---
ring = at.load_lattice('betamodel.mat', use='betamodel')
ring.disable_6d()
# --- Get element indices ---
cor_indices = at.get_refpts(ring, 'S[HFDIJ]*')
used_bpm = at.get_refpts(ring, at.elements.Monitor)

# --- Load measurements ---
with h5py.File("./data/measured_orm_loco.h5", "r") as f:
    measured_orm = np.array(f["response_matrix"])  # [BPMs x COR]
    delta_correctors = np.array(f["full_delta"])

with h5py.File("./data/measured_dispersion_loco.h5", "r") as f:
    measured_eta_x_ = np.array(f["measured_eta_x"])
    measured_eta_y_ = np.array(f["measured_eta_y"])
    rf_full_step = np.array(f["rf_full_step"])

# --- Remove bad BPMs ---
bad_bpm_positions = np.array([27, 58, 157, 286])
used_bpms_ords = np.delete(used_bpm, bad_bpm_positions)

measured_eta_x = np.delete(measured_eta_x_, bad_bpm_positions)
measured_eta_y = np.delete(measured_eta_y_, bad_bpm_positions)
eta = np.concatenate([measured_eta_x, measured_eta_y])

measured_orm, removed = remove_bad_bpms(
    measured_orm,
    bad_bpm_positions,
    total_bpms=len(used_bpm),
    axis=0,
    input_type="positions"
)

# if include dispersion is true
#measured_orm = np.hstack((measured_orm, eta.reshape(-1, 1)))

# --- Prepare configuration for model ORM ---
Corords = [cor_indices, cor_indices]
CMstep = [[delta_correctors] * len(Corords[0]), [delta_correctors] * len(Corords[1])]


fit_cfg = FitInitConfig()
includeDispersion = False
HCMCoupling = np.zeros(len(Corords[0]))
VCMCoupling = np.zeros(len(Corords[1]))

cfg = RMConfig(
    dkick=CMstep,
    bpm_ords=used_bpms_ords,
    cm_ords=Corords,
    HCMCoupling=HCMCoupling,
    VCMCoupling=VCMCoupling,
    rfStep=rf_full_step,
    includeDispersion=includeDispersion
)

# --- Compute model ORM ---
orm_model = response_matrix(ring, config=cfg)

rms_diff = np.sqrt(np.mean((orm_model - measured_orm)**2))
print(f"RMS difference between model and measured ORM: {rms_diff:.3e} m")
os.makedirs("output", exist_ok=True)
plot_matrices(orm_model, measured_orm, titles=None, cmap='viridis', plot_type='3d', save_path="output/orms_comparison.png")



