from pySC import generate_SC
import json
import yaml
SC = generate_SC('betamodel_conf_ideal.yaml', seed=1, sigma_truncate=3)

mapping = {}
for magnet_name in SC.magnet_arrays['correctors']:
    index = SC.magnet_settings.magnets[magnet_name].sim_index
    device_name_template = SC.lattice.design[index].Device.split('/')
    cs_name = '/'.join(device_name_template)
    mapping[magnet_name+'/A1L'] = cs_name

for magnet_name in SC.magnet_arrays['correctors']:
    index = SC.magnet_settings.magnets[magnet_name].sim_index
    device_name_template = SC.lattice.design[index].Device.split('/')
    device_name_template[1] = device_name_template[1].replace('vst-','hst-')
    cs_name = '/'.join(device_name_template)
    mapping[magnet_name+'/B1L'] = cs_name

for magnet_name in SC.magnet_arrays['correctors']:
    index = SC.magnet_settings.magnets[magnet_name].sim_index
    device_name_template = SC.lattice.design[index].Device.split('/')
    device_name_template[1] = device_name_template[1].replace('vst-','sqp-')
    cs_name = '/'.join(device_name_template)
    mapping[magnet_name+'/A2L'] = cs_name

for magnet_name in SC.magnet_arrays['sextupoles']:
    index = SC.magnet_settings.magnets[magnet_name].sim_index
    device_name_template = SC.lattice.design[index].Device.split('/')
    device_name_template[1] = device_name_template[1].replace('m-','vst-')
    cs_name = '/'.join(device_name_template)
    mapping[magnet_name+'/A1L'] = cs_name

for magnet_name in SC.magnet_arrays['sextupoles']:
    index = SC.magnet_settings.magnets[magnet_name].sim_index
    device_name_template = SC.lattice.design[index].Device.split('/')
    device_name_template[1] = device_name_template[1].replace('m-','hst-')
    cs_name = '/'.join(device_name_template)
    mapping[magnet_name+'/B1L'] = cs_name

for magnet_name in SC.magnet_arrays['sextupoles']:
    index = SC.magnet_settings.magnets[magnet_name].sim_index
    device_name_template = SC.lattice.design[index].Device.split('/')
    device_name_template[1] = device_name_template[1].replace('m-','sqp-')
    cs_name = '/'.join(device_name_template)
    mapping[magnet_name+'/A2L'] = cs_name

for magnet_name in SC.magnet_arrays['sextupoles']:
    index = SC.magnet_settings.magnets[magnet_name].sim_index
    device_name_template = SC.lattice.design[index].Device.split('/')
    cs_name = '/'.join(device_name_template)
    mapping[magnet_name+'/B3L'] = cs_name

for magnet_name in SC.magnet_arrays['quadrupoles']:
    index = SC.magnet_settings.magnets[magnet_name].sim_index
    device_name_template = SC.lattice.design[index].Device.split('/')
    cs_name = '/'.join(device_name_template)
    mapping[magnet_name+'/B2L'] = cs_name
    #print(cs_name, SC.lattice.design[index].Device)


json.dump(mapping, open('name_mapping.json','w'), indent=4)


all_names = [ line.split(':')[-1].strip(',').strip() for line in open('devnames.txt','r').readlines()]
for key in mapping:
    assert mapping[key] in all_names, f"Missing {mapping[key]}"

for name in all_names:
    if 'beam-position' not in name and 'm-of' not in name and 'm-dq' not in name:
        assert name in list(mapping.values()), f"Missing {name} from mapping"