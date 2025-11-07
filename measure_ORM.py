import pySC
from pySC.apps import measure_ORM, orbit_correction
from pySC.apps.codes import ResponseCode
from interface import Interface
import logging
import json

pySC.disable_pySC_rich()

start_measurement=False
#logging.getLogger('pySC.apps.response').setLevel(logging.DEBUG)
logger = logging.getLogger(__name__)

ebs = Interface()

response_matrix = pySC.ResponseMatrix.from_json('ideal_orm.json')
## map pySC corrector names to ebs control system names
mapping = json.load(open('name_mapping.json'))
response_matrix.input_names = [mapping[pySC_name] for pySC_name in response_matrix.input_names]

corrector_names = response_matrix.input_names #[:10]

generator = measure_ORM(interface=ebs, corrector_names=corrector_names, delta=100e-6,
                        shots_per_orbit=1, bipolar=True, skip_save=False)

if start_measurement:
    for code, measurement in generator:
        logger.info(f"{measurement.last_number+1}/{len(corrector_names)}, (code={code.name}), last_corrector={measurement.last_input}")
        if code is ResponseCode.MEASURING:
            last_corrector = measurement.last_input
            response_matrix.enable_all_inputs()
            response_matrix.disable_all_inputs_but([last_corrector])
            trims = orbit_correction(interface=ebs, response_matrix=response_matrix, method='micado', parameter=1, apply=True)
            logger.info(f'Corrected orbit with: {trims}')
