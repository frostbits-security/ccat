
# Storm-control options check
# Input:
#        interface dictionary
#        config result dictionary
# Output:
#        updated result dictionary
#

# check storm-control level
# if level incorrect return [0,level, maximum appropriate level]
def storm_lvl_check(lvl):
    return ([1] if float(lvl) < 80.0 else [0,lvl,80])

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
            result.update({each + ' storm': type_dct[each]})
    return result

def iter_type(each, type_dct):
    if each in type_dct:
        type_dct[each] = 1
    return type_dct

def check(iface_dct, result):
    # key  availability check
    if 'storm control' in iface_dct:
        storm_dct = iface_dct['storm control']
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
                                result['storm level'] = 0
                            else:
                                result['storm level'] = storm_lvl_check(lvl_list[1])
                        else:
                            result['storm level'] = 0
                    else:
                        if int(lvl_list[1]) == 0 or int(lvl_list[1]) == 100 or int(lvl_list[1]) == 1:
                            result['storm level'] = 0
                else:
                    result['storm level'] = storm_lvl_check(lvl_list)
        # check storm-control traffic type
                check_storm_type(lvl_type, result, 0)

        if 'type' in storm_dct:
            check_storm_type(storm_dct['type'], result, 1)

    return result
