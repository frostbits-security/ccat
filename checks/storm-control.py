
# Storm-control options check
# Input:
#        interface dictionary
#        config result dictionary
# Output:
#        updated result dictionary
#           {{'iface1': {'Storm-control': {'storm level': [severity(int), 'message', 'best practice'],'multicast storm':...}, 'iface2':...}}
#

# check storm-control level
# if level incorrect return [0,level, maximum appropriate level]

def storm_lvl_check(lvl):
    # return ([1,80] if float(lvl) < 80.0 else [0,lvl,80])
    if float(lvl) < 80.0:
        return [2,lvl,'Storm-control level should be less than 80']
    else:
        return [0,lvl,'Storm-control level should be less than 80']


# check storm-control traffic type
def check_storm_type(type_storm, result, flag):
    type_dct = {'broadcast': 0, 'multicast': 0, 'unicast': 0}
    if flag:
        for each in type_storm:
            type_dct = iter_type(each, type_dct)
    else:
        type_dct = iter_type(type_storm, type_dct)
    for each in type_dct:
        if type_dct[each] == 1:
            result.update({each + ' storm':[2,'OK',each.capitalize()+' storm-control should be turn on']})

    return result

def iter_type(each, type_dct):
    if each in type_dct:
        type_dct[each] = 1
    return type_dct


def check(iface_dct, dct):
    # key  availability check
    for iface in iface_dct:
        result = {}

        if 'vlan' not in iface.lower():
            # 'storm control' in iface_dct[iface] and
            if 'storm control' in iface_dct[iface] and len(iface_dct[iface]['storm control'])!=0:
                storm_dct = iface_dct[iface]['storm control']
                # check storm-control level

                if 'level' in storm_dct:
                    for i in range(len(storm_dct['level'])):
                        lvl_type = storm_dct['level'][i][0]
                        lvl_list = storm_dct['level'][i][1]

                        # if level pps[bps] level_1 level_2
                        if 'pps' in lvl_list or 'bps' in lvl_list:
                            lvl_list = lvl_list.split()
                            if len(lvl_list) == 3:
                                if lvl_list[1] > lvl_list[2] or lvl_list[1] != lvl_list[2]:
                                    if int(lvl_list[1]) == 0 or int(lvl_list[2]) == 0 or int(
                                            lvl_list[1]) == 100 or int(lvl_list[2]) == 100 or int(
                                        lvl_list[1]) == 1 or int(lvl_list[2]) == 1:
                                        result['storm level'] = [0,lvl_list,'Storm-control level should be less than 80(0.8)']
                                    else:
                                        result['storm level'] = storm_lvl_check(lvl_list[1])
                                else:
                                    result['storm level'] = [0,lvl_list,'Storm-control level shouldn`t be equal ']
                            else:
                                if int(lvl_list[1]) == 0 or int(lvl_list[1]) == 100 or int(lvl_list[1]) == 1:
                                    result['storm level'] = [0,'Bad','Storm-control level shouldn`t be equal 1(100) or 0']
                        else:
                            result['storm level'] = storm_lvl_check(lvl_list)

                # check storm-control traffic type
                        check_storm_type(lvl_type, result, 0)
                else:
                    result.update({'storm level': [0,'Storm-control level does not support', 'Storm-control level should be turn on']})
                if 'type' in storm_dct:
                    result.update(check_storm_type(storm_dct['type'], result, 1))

            else:
                result.update({'Storm-control': [0, 'Storm control does not enable', 'Storm-control should be enable']})
                dct.update({iface: {'Storm-Control':result}})
                continue
        for each in ['broadcast storm','multicast storm','unicast storm']:
            if each not in result:
                result.update({each:[0,'Turn off',each.capitalize()+' storm-control should be turn on']})

        dct.update({iface:{'Storm-Control':result}})
    return dct



