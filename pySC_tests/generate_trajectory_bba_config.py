from pySC import generate_SC, ResponseMatrix
import json

# needs betamodel.mat
SC = generate_SC('betamodel_conf_ideal.yaml', seed=1, sigma_truncate=3)
SC.tuning.response_matrix['trajectory1'] = ResponseMatrix.from_json('ideal_1turn_orm.json')
SC.tuning.response_matrix['trajectory2'] = ResponseMatrix.from_json('ideal_2turn_orm.json')
SC.tuning.generate_trajectory_bba_config(max_dx_at_bpm=300e-6, max_modulation=50e-6)

with open('tbba_config.json', 'w') as fp:
    json.dump(SC.tuning.trajectory_bba_config.config, fp, indent=4)

config = SC.tuning.trajectory_bba_config.config
with open('name_mapping.json', 'r') as fp:
    name_mapping = json.load(fp)

for key in config.keys():
    config[key]['QUAD'] = name_mapping[config[key]['QUAD']]
    config[key]['HCORR'] = name_mapping[config[key]['HCORR']]
    config[key]['VCORR'] = name_mapping[config[key]['VCORR']]

with open('tbba_config_tango.json', 'w') as fp:
    json.dump(SC.tuning.trajectory_bba_config.config, fp, indent=4)