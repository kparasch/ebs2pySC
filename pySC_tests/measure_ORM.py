import pySC
from pySC.apps.interface import pySCOrbitInterface
from pySC.apps import measure_ORM, orbit_correction
from pySC.apps.codes import ResponseCode
import logging

pySC.disable_pySC_rich()

#logging.getLogger('pySC.apps.response').setLevel(logging.DEBUG)
logger = logging.getLogger(__name__)

# needs betamodel.mat
SC = pySC.generate_SC('betamodel_conf_ideal.yaml', seed=1, sigma_truncate=3)
interface = pySCOrbitInterface(SC=SC)

response_matrix = pySC.ResponseMatrix.from_json('ideal_orm.json')
corrector_names = response_matrix.input_names[:10]

generator = measure_ORM(interface=interface, corrector_names=corrector_names, delta=100e-6,
                        shots_per_orbit=1, bipolar=True, skip_save=False)

for code, measurement in generator:
    logger.info(f"{measurement.last_number+1}/{len(corrector_names)}, (code={code.name}), last_corrector={measurement.last_input}")
    if code is ResponseCode.MEASURING:
        last_corrector = measurement.last_input
        response_matrix.enable_all_inputs()
        response_matrix.disable_all_inputs_but([last_corrector])
        trims = orbit_correction(interface=interface, response_matrix=response_matrix, method='micado', parameter=1, apply=True)
        logger.info(f'Corrected orbit with: {trims}')
