from pySC import generate_SC

# needs betamodel.mat
SC = generate_SC('betamodel_conf_ideal.yaml', seed=1, sigma_truncate=3)
SC.tuning.calculate_model_trajectory_response_matrix(save_as='ideal_1turn_orm.json', n_turns=1)
SC.tuning.calculate_model_trajectory_response_matrix(save_as='ideal_2turn_orm.json', n_turns=2)