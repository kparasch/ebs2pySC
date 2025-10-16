from tango import AttributeProxy, DeviceProxy
import os
import time

os.environ['TANGO_HOST'] = 'acs.esrf.fr:10000,acs.esrf.fr:11000'
# os.environ['TANGO_HOST'] = 'ebs-simu-1:10000'

present_host = os.environ['TANGO_HOST']
print(present_host)

class Interface:
    def get_orbit(self):
        '''
        returns the orbit of the machine in two lists/arrays:
        e.g. x, y = ebs.get_orbit()

        we should make sure here that we can call this function twice and not get the same reading (i.e. wait that the orbit has refreshed).
        '''

        orb_ref_h = AttributeProxy('srdiag/bpm/all/All_SA_HPosition').read().value
        orb_ref_v = AttributeProxy('srdiag/bpm/all/All_SA_VPosition').read().value
        
        time.sleep(1) # 1 second polling time

        return orb_ref_h, orb_ref_v

    def get(self, name: str) -> float:
        '''
        gets a magnet strength in the machine (physics units), integrated or not.
        e.g. k0 = ebs.get('SD1A-C01-H')
        '''
        pass

    def set(self, name: str, value: float):
        '''
        sets a magnet strength in the machine (physics units), integrated or not.
        e.g. ebs.set('SD1A-C01-H', 100e-6)

        waiting time to make sure power supply is settled and eddy currents are decayed to be handled also here.
        '''

    def get_many(self, names: list) -> dict[str, float]:
        '''
        gets many magnet strengths in the machine (physics units), integrated or not.
        e.g. data_k0 = ebs.get_many(['SD1A-C01-H', 'SD1A-C01-V'])
        resulting in data_k0 as {'SD1A-C01-H': 100e-6, 'SD1A-C01-V': 200e-6} for example
        '''
        pass

    def set_many(self, data: dict[str, float]):
        '''
        perhaps there is a specific host you use to set all corrector settings?

        sets many magnet strengths in the machine (physics units), integrated or not.
        e.g. ebs.set_many({'SD1A-C01-H': 100e-6, 'SD1A-C01-V': 200e-6})

        waiting time to make sure power supply is settled and eddy currents are decayed to be handled also here.
        '''
        pass