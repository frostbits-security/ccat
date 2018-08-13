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
# import re

from re import findall

def storm_lvl_check(lvl):
    # return ([1,80] if float(lvl) < 80.0 else [0,lvl,80])
    if float(lvl) < 80.0:
        return [2, lvl, 'Storm-control level should be less than 80']
    else:
        return [0, lvl, 'Storm-control level should be less than 80']


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
            result.update({each + ' storm': [2, 'ENABLED', each.capitalize() + ' storm-control should be turn on']})

    return result


def iter_type(each, type_dct):
    if each in type_dct:
        type_dct[each] = 1
    return type_dct


def check(iface_dct):
    # key  availability check
    dct = {}
    if 'storm control' in iface_dct and len(iface_dct['storm control']) != 0:
        storm_dct = iface_dct['storm control']
        # check storm-control level

        if 'level' in storm_dct:
            for i in range(len(storm_dct['level'])):
                lvl_type = storm_dct['level'][i][0]
                lvl_list = storm_dct['level'][i][1]


                lvl_list = findall(r'([\d\.]+)', lvl_list)
                # if level pps[bps] level_1 level_2
                if len(lvl_list) == 2:
                    if lvl_list[0] > lvl_list[1] or lvl_list[0] != lvl_list[1]:
                        if float(lvl_list[0]) == 0 or float(lvl_list[1]) == 0 or float(
                                lvl_list[0]) == 100 or float(lvl_list[1]) == 100 or float(
                            lvl_list[0]) == 1 or float(lvl_list[1]) == 1:
                            dct.update(
                                {'storm level': [0, 'INCORRECT', 'Storm-control level should be less than 80(0.8)']})
                        else:
                            dct.update({'storm level': storm_lvl_check(lvl_list[0])})
                    else:
                        dct.update({'storm level': [0, 'INCORRECT', 'Storm-control level shouldn`t be equal']})
                else:
                    if float(lvl_list[0]) == 0 or float(lvl_list[0]) == 100 or float(lvl_list[0]) == 1:
                        dct.update({'storm level': [0, 'Bad', 'Storm-control level shouldn`t be equal 1(100) or 0']})
                    else:
                        dct.update({'storm level': storm_lvl_check(lvl_list[0])})

                # check storm-control traffic type

                check_storm_type(lvl_type, dct, 0)
        else:
            dct.update(
                {'storm level': [0, 'Storm-control level does not support', 'Storm-control level should be turn on']})

        if 'type' in storm_dct:
            dct.update(check_storm_type(storm_dct['type'], dct, 1))

        for each in ['broadcast storm', 'multicast storm', 'unicast storm']:
            if each not in dct:
                if each == 'unicast storm':
                    dct.update({each: [1, 'DISABLED', each.capitalize() + ' storm-control should be turn on']})
                else:
                    dct.update({each: [0, 'DISABLED', each.capitalize() + ' storm-control should be turn on']})
    else:
        dct.update({'Storm-control': [0, 'DISABLED', 'Storm-control should be enable']})
        return dct

    return dct


