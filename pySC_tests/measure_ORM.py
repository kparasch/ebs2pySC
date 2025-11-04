from pySC import generate_SC
from pySC.apps.interface import pySCOrbitInterface
from pySC.apps import measure_ORM
from pySC.apps.bba import analyze_bba_data
from pySC.apps.bba import BBACode
import json
import logging

logging.getLogger('pySC.apps.bba').setLevel(logging.DEBUG)
logger = logging.getLogger(__name__)

# needs betamodel.mat
SC = generate_SC('betamodel_conf_ideal.yaml', seed=1, sigma_truncate=3)
interface = pySCOrbitInterface(SC=SC)

corrector_names = SC.tuning.CORR[:10]

with open('bba_config.json','r') as fp:
    bba_config = json.load(fp)


generator = measure_ORM(interface=interface, corrector_names=corrector_names, delta=100e-6,
                        shots_per_orbit=1, bipolar=True, skip_save=False)

for code, measurement_object in generator:
    logger.debug(f"Got code: {code.name}")
    #logger.info(f"Last used corrector is {measurement_object.last_input}")
