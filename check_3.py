from termcolor import colored


def storm_lvl_check(lvl):
    return (1 if float(lvl) < 80.0 else 0)


def key_check(key, dct):
    return (1 if key in dct.keys() else 0)


# 0-protocol is turned off,1-protocol turn on

def check_DTPorSTP(protocol, iface_dct, result):
    if key_check(protocol, iface_dct):
        if iface_dct[protocol] == 'no':
            result[protocol] = 0
        else:
            result[protocol] = 1


def _check_stp__control(option, dct, dct_res):
    if option in dct:
        dct_res[option] = 1
    else:
        dct_res[option] = 0
    return (dct_res)


def check_stp(config, global_dct):
    stp_res = {}
    stp_res.update(_check_stp__control('portfast', global_dct[config]['stp'], stp_res))
    stp_res.update(_check_stp__control('loopguard', global_dct[config]['stp'], stp_res))
    stp_res.update(_check_stp__control('bpdu', global_dct[config]['stp'], stp_res))
    return (stp_res)


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


def iter_type(each, type_dct):
    if each in type_dct:
        type_dct[each] = 1
    return type_dct


def check_settings(set_dct, config):
    storm_lst = ['multicast storm', 'broadcast storm', 'unicast storm']
    print('{} MISTAKES:'.format(config))
    for key in set_dct:
        if key == 'global':
            for each in set_dct['global']:
                if set_dct['global'][each] != 1:
                    print('{} is turn off It can be insecure!'.format(key))
        elif 'loopback' not in key.lower() and 'vlan' not in key.lower():
            print('{}\n-------------------------'.format(key))
            if 'storm level' not in set_dct[key] or set_dct[key]['storm level'] == 0:
                print(' - Storm-Control Level\t\t\t\t[{}]'.format(colored('Warning', 'red')))
            for each in storm_lst:
                if each not in set_dct[key]:
                    if each == 'broadcast storm':
                        print(' - Broadcast Storm-Control\t\t\t[{}]'.format(colored('Warning', 'red')))
                    elif each == 'multicast storm':
                        print(' - Multicast Storm-Control\t\t\t[{}]'.format(colored('Not Found', 'yellow')))
                    else:
                        print(' - Unicast Storm-Control\t\t\t[{}]'.format(colored('Not Enabled', 'white')))

            for protocol in ['dtp', 'cdp']:
                if protocol not in set_dct[key] or set_dct[key][protocol] == 1:
                    if protocol == 'dtp':
                        print(' - DTP\\t\t\t\t\t\t[{}]'.format(colored('Enabled', 'red')))
                    else:
                        print(' - CDP\\t\t\t\t\t\t[{}]'.format(colored('Enabled', 'white')))
            if 'stp portfast' not in set_dct[key] or set_dct[key] == 0:
                print(' - Portfast\t\t\t\t\t[{}]'.format(colored('Not Found', 'yellow')))


#
# incorrect/insecure settings==0
# correct/secure settings==1

def check_features(config_dct, global_dct):
    dct = {}
    for config in config_dct:
        result_dct = {}
        if key_check('stp', global_dct[config]):
            result_dct['global'] = check_stp(config, global_dct)
        for iface in config_dct[config]:
            result = {}
            iface_dct = config_dct[config][iface]
            # print(iface_dct)
            if key_check('shutdown', iface_dct):
                if len(iface_dct) <= 5:
                    if iface_dct['shutdown'] != 'yes':
                        result['shutdown'] = 0
                # if iface_dct['shutdown'] == 'no':
                # MODE
                if key_check('type', iface_dct):
                    mode = iface_dct['type']
                    if mode == 'access':
                        result['type'] = 0
                    else:
                        result['type'] = 1
                # STORM-CONTROL
                if key_check('storm control', iface_dct):

                    storm_dct = iface_dct['storm control']
                    if 'level' in storm_dct.keys():
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

                            check_storm_type(lvl_type, result, 0)

                    if 'type' in storm_dct.keys():
                        check_storm_type(storm_dct['type'], result, 1)

                # CDP
                check_DTPorSTP('cdp', iface_dct, result)

                # DTP
                check_DTPorSTP('dtp', iface_dct, result)

                # STP
                if key_check('stp', iface_dct):
                    if iface_dct['type'] == 'access' and iface_dct['stp'] == 'portfast':
                        result['stp portfast'] = 1
                    elif 'trunk' in iface_dct['stp']:
                        print('DANGEROUS!!')
                        result['trunk portfast'] = 1

            result_dct[iface] = result
        dct[config] = result_dct
        check_settings(dct[config], config)

        # with open('result.txt', 'a') as f:
        #     f.write('\n' + config + '\n')
        #     f.write(str(result_dct))




