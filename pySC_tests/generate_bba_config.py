from pySC import generate_SC, ResponseMatrix
import json

# needs betamodel.mat
SC = generate_SC('betamodel_conf_ideal.yaml', seed=1, sigma_truncate=3)
SC.tuning.response_matrix['orbit'] = ResponseMatrix.from_json('ideal_orm.json')
SC.tuning.generate_orbit_bba_config(max_dx_at_bpm=300e-6, max_modulation=20e-6)

with open('bba_config.json', 'w') as fp:
    json.dump(SC.tuning.orbit_bba_config.config, fp, indent=4)