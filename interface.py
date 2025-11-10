from tango import AttributeProxy, DeviceProxy
import os
import time
from pathlib import Path
data_folder = Path('./data')

os.environ['TANGO_HOST'] = 'acs.esrf.fr:10000,acs.esrf.fr:11000'
# os.environ['TANGO_HOST'] = 'ebs-simu-1:10000'

present_host = os.environ['TANGO_HOST']
print(present_host)

master_source = AttributeProxy('sy/ms/1/Frequency')

HRefOrb = AttributeProxy('sr/beam-orbitcor/svd-h/BumpOrbit')
VRefOrb = AttributeProxy('sr/beam-orbitcor/svd-v/BumpOrbit') 

HBPM = AttributeProxy('srdiag/bpm/all/All_SA_HPosition')
VBPM = AttributeProxy('srdiag/bpm/all/All_SA_VPosition')

hst = DeviceProxy('srmag/hst/all')  # 384 hor steerers (include DQ hor steerer)
vst = DeviceProxy('srmag/vst/all')  # 288 ver steerers
sqp = DeviceProxy('srmag/sqp/all')  # 288 skew quads
sext = DeviceProxy('srmag/m-s/all')  # 192 Sextupoles
quad = DeviceProxy('srmag/m-q/all')  # 610 quadrupoles (includes DQ quad)
oct = DeviceProxy('srmag/m-o/all')  # 64 octupoles

# get names in arrays 
hst_names = hst.CorrectorNames
vst_names = vst.CorrectorNames 
sqp_names = sqp.CorrectorNames 
sext_names = sext.MagnetNames
quad_names = quad.MagnetNames
oct_names = oct.MagnetNames

class Interface:
    wait_after_set = 1  # seconds
    quad_wait_time = 5  # seconds
    rf_wait_time = 5 # seconds
    orbit_wait_time = 1 # seconds

    def get_rf_main_frequency(self):
        """ get master source frequency in Hz"""

        return master_source.read().value

    def set_rf_main_frequency(self, frequency):
        """ set absolute value of master source frequency in Hz"""

        master_source.write(frequency)
        time.sleep(self.rf_wait_time)
        return

    def get_ref_orbit(self):
        '''
        returns the reference orbit of the machine in two lists/arrays:
        e.g. x, y = ebs.get_ref_orbit()

        we should make sure here that we can call this function twice and not get the same reading (i.e. wait that the orbit has refreshed).
        '''

        orb_ref_h = HRefOrb.read().value
        orb_ref_v = VRefOrb.read().value

        return orb_ref_h, orb_ref_v

    def get_orbit(self):
        '''
        returns the orbit of the machine in two lists/arrays:
        e.g. x, y = ebs.get_orbit()

        we should make sure here that we can call this function twice and not get the same reading (i.e. wait that the orbit has refreshed).
        '''

        time.sleep(self.orbit_wait_time) # 1 second polling time
        orb_h = HBPM.read().value
        orb_v = VBPM.read().value

        return orb_h, orb_v

    def get(self, name: str) -> float:
        '''
        gets a magnet strength in the machine (physics units), integrated or not.
        e.g. k0 = ebs.get('SD1A-C01-H')
        '''
        # name is a tango device in this format 'srmag/m-q/all/CorrectionStrengths' where is pySC exepcting to find the magnet names?
        mag = AttributeProxy(name+'/Strength')
        mag_SetPoint = mag.read().w_value

        return mag_SetPoint

    def set(self, name: str, value: float):
        '''
        sets a magnet strength in the machine (physics units), integrated or not.
        e.g. ebs.set('SD1A-C01-H', 100e-6)

        waiting time to make sure power supply is settled and eddy currents are decayed to be handled also here.
        '''
        AttributeProxy(name+'/Strength').write(value)
        if "m-q" in name:
            time.sleep(max(self.quad_wait_time, self.wait_after_set))
        else:
            time.sleep(self.wait_after_set)
        return

    def get_many(self, names: list) -> dict[str, float]:
        '''
        gets many magnet strengths in the machine (physics units), integrated or not.
        e.g. data_k0 = ebs.get_many(['SD1A-C01-H', 'SD1A-C01-V'])
        resulting in data_k0 as {'SD1A-C01-H': 100e-6, 'SD1A-C01-V': 200e-6} for example
        '''

        data_k0={}

        # init set points
        hst_SetPoint = []
        vst_SetPoint = []
        sqp_SetPoint = []
        sext_SetPoint = []
        quad_SetPoint = []
        oct_SetPoint = []

        for name in names:
            if "hst" in name: 
                # get set points only if a name is requested
                if hst_SetPoint == []:
                    hst_SetPoint = hst.read_attribute("Strengths").w_value # single call to read array
                # find name index
                data_k0[name] = hst_SetPoint[hst_names.index(name)]
            if "vst" in name: 
                # get set points only if a name is requested
                if vst_SetPoint == []:
                    vst_SetPoint = vst.read_attribute("Strengths").w_value # single call to read array
                # find name index
                data_k0[name] = vst_SetPoint[vst_names.index(name)]
            if "sqp" in name: 
                # get set points only if a name is requested
                if sqp_SetPoint == []:
                    sqp_SetPoint = sqp.read_attribute("CorrectionStrengths").w_value # single call to read array
                # find name index
                data_k0[name] = sqp_SetPoint[sqp_names.index(name)]
            if "m-s" in name: 
                # get set points only if a name is requested
                if sext_SetPoint == []:
                    sext_SetPoint = sext.read_attribute("CorrectionStrengths").w_value # single call to read array
                # find name index
                data_k0[name] = sext_SetPoint[sext_names.index(name)]
            if "m-q" in name: 
                # get set points only if a name is requested
                if quad_SetPoint == []:
                    quad_SetPoint = quad.read_attribute("CorrectionStrengths").w_value # single call to read array
                # find name index
                data_k0[name] = quad_SetPoint[quad_names.index(name)]
            if "m-o" in name: 
                # get set points only if a name is requested
                if oct_SetPoint == []:
                    oct_SetPoint = oct.read_attribute("CorrectionStrengths").w_value # single call to read array
                # find name index
                data_k0[name] = oct_SetPoint[oct_names.index(name)]

        return data_k0

    def set_many(self, data: dict[str, float]):
        '''
        perhaps there is a specific host you use to set all corrector settings?

        sets many magnet strengths in the machine (physics units), integrated or not.
        e.g. ebs.set_many({'SD1A-C01-H': 100e-6, 'SD1A-C01-V': 200e-6})

        waiting time to make sure power supply is settled and eddy currents are decayed to be handled also here.
        '''
        wait_time = self.wait_after_set

        # init set points
        hst_SetPoint = []
        vst_SetPoint = []
        sqp_SetPoint = []
        sext_SetPoint = []
        quad_SetPoint = []
        oct_SetPoint = []

        # apply setting to array:
        hst_apply = False
        vst_apply = False
        sqp_apply = False
        sext_apply =False
        quad_apply = False
        oct_apply = False

        # loop values to change
        for key, value in data.items():
            if "hst" in key:
                if hst_SetPoint == []:
                    hst_SetPoint = hst.read_attribute("Strengths").w_value # single call to read array
                    hst_apply = True
                hst_SetPoint[hst_names.index(key)] = value

            if "vst" in key:
                if vst_SetPoint == []:
                    vst_SetPoint = vst.read_attribute("Strengths").w_value # single call to read array
                    vst_apply = True
                vst_SetPoint[vst_names.index(key)] = value

            if "sqp" in key:
                if sqp_SetPoint == []:
                    sqp_SetPoint = sqp.read_attribute("CorrectionStrengths").w_value # single call to read array
                    sqp_apply = True
                sqp_SetPoint[sqp_names.index(key)] = value

            if "m-s" in key:
                if sext_SetPoint == []:
                    sext_SetPoint = sext.read_attribute("CorrectionStrengths").w_value # single call to read array
                    sext_apply = True
                sext_SetPoint[sext_names.index(key)] = value

            if "m-q" in key:
                if quad_SetPoint == []:
                    quad_SetPoint = quad.read_attribute("CorrectionStrengths").w_value # single call to read array
                    quad_apply = True
                quad_SetPoint[quad_names.index(key)] = value

            if "m-o" in key:
                if oct_SetPoint == []:
                    oct_SetPoint = oct.read_attribute("CorrectionStrengths").w_value # single call to read array
                    oct_apply = True
                oct_SetPoint[oct_names.index(key)] = value

        # apply values
        if hst_apply:
            hst.Strengths = hst_SetPoint
        if vst_apply:
            vst.Strengths = vst_SetPoint
        if sqp_apply:
            sqp.CorrectionStrengths = sqp_SetPoint
        if quad_apply:
            wait_time = max(wait_time, self.quad_wait_time)
            quad.CorrectionStrengths = quad_SetPoint
        if sext_apply:
            sext.CorrectionStrengths = sext_SetPoint
        if oct_apply:
            oct.CorrectionStrengths = oct_SetPoint

        time.sleep(wait_time)
        return