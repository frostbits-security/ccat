# Determine interface type (critical/unknown/trusted) if vlanmap defined
# Input:
#       vlanmap dictionary
#       interface dictionary
# Output:
#       vlanmap result word
#           'CRITICAL'/'UNKNOWN'/'TRUSTED'
#       vlanmap options dictionary
#           {'vlanmap warning': [1, 'Trusted and Critical vlans on interface'], 'vlanmap type': [2, 'CRITICAL']}
#
def determine(vlanmap, interface):
    result_dict = {}

# Create empty dictionary and fill it: if interface is access - will be filled only 1 list, if interface is trunk - might
# be filled some lists
    vlanmap_check = {'critical': [], 'unknown': [], 'trusted': []}
    area_num = 0
    for area in vlanmap:
        for vlan_vlanmap in area:
            for config_vlan in interface['vlans']:
                if config_vlan == vlan_vlanmap:
                    if area_num == 0:
                        vlanmap_check['critical'].append(config_vlan)
                    elif area_num == 1:
                        vlanmap_check['unknown'].append(config_vlan)
                    else:
                        vlanmap_check['trusted'].append(config_vlan)
        area_num += 1

# if 1 trunk interface has critical and trusted vlans - it may be bad for network segment so its warning type
    if vlanmap_check['critical'] and vlanmap_check['trusted']:
        result_dict['vlanmap warning'] = [1, 'Trusted and Critical vlans on interface']

# If interface has at least 1 critical vlan - it's vlanmap type will be CRITICAL, if 0 criticals vlans, but at least 1
# unknown vlan - vlanmap type will be UNKNOWN, if interface has only trusted vlans - vlanmap type will be TRUSTED
    if vlanmap_check['critical']:
        result_dict['vlanmap type'] = [2, 'CRITICAL']
    elif vlanmap_check['unknown']:
        result_dict['vlanmap type'] = [2, 'UNKNOWN']
    elif vlanmap_check['trusted']:
        result_dict['vlanmap type'] = [2, 'TRUSTED']
    vlanmap_result = result_dict['vlanmap type'][1]

    return vlanmap_result, result_dict
