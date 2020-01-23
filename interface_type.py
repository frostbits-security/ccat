# Determine interface type (critical/unknown/trusted) if vlanmap defined
# Input:
#       vlanmap dictionary
#       interface dictionary
# Output:
#       vlanmap result word
#           'dmz'/'other'/'management'
#       vlanmap options dictionary
#           {'vlanmap warning': [1, 'Trusted and Critical vlans on interface'], 'vlanmap type': [2, 'dmz']}
def determine(vlanmap, interface):
    result_dict = {}

    # Create empty dictionary and fill it: if interface is access - will be filled only 1 list, if interface is trunk -
    # might be filled some lists
    vlanmap_check = {'dmz': [], 'other': [], 'management': []}
    find = False
    area_num = 0
    for area in vlanmap:
        for config_vlan in interface['vlans']:
            if config_vlan in area:
                if area_num == 0:
                    vlanmap_check['dmz'].append(config_vlan)
                elif area_num == 1:
                    vlanmap_check['other'] .append(config_vlan)
                else:
                    vlanmap_check['management'] .append(config_vlan)
                find = True
        area_num += 1


    # if interface vlans are not in vlanmap - vlanmap type will be set as UNKNOWN
    if not find:
        result_dict['vlanmap type'] = [3, 'OTHER']


    # If interface has at least 1 critical vlan - it's vlanmap type will be set as CRITICAL, if 0 critical vlans, but
    # at least 1 unknown vlan - vlanmap type will be set as UNKNOWN, if interface has only trusted vlans - vlanmap type
    # will be set as TRUSTED
    else:
        if vlanmap_check['dmz']:
            result_dict['vlanmap type'] = [3, 'DMZ']#critical
        elif vlanmap_check['other']:
            result_dict['vlanmap type'] = [3, 'OTHER']#unknown
        elif vlanmap_check['management']:
            result_dict['vlanmap type'] = [3, 'MANAGEMENT']#trusted

    # if 1 trunk interface has critical and trusted vlans - it may be insecure for network segment so its warning type
        if vlanmap_check['dmz'] and vlanmap_check['management']:
            result_dict['vlanmap warning'] = [1, 'Management and DMZ vlans on interface', 'It may be a potential threat']


    return result_dict
