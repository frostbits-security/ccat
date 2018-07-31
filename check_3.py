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
                        result['trunk portfast'] = 1

            result_dct[iface] = result
        dct[config] = result_dct
        check_settings(dct[config], config)

        # with open('result.txt', 'a') as f:
        #     f.write('\n' + config + '\n')
        #     f.write(str(result_dct))


# Config global parameters parsing
# INPUT:  dictionary with config global options
# SAMPLE: {'ip_dhcp_snoop': {...}, 'ip_arp_inspection': {...}, 'active_service': [...], ...}
# OUTPUT: dictionary with defined bad(0)/good(1)/warning(2) parameters
# SAMPLE: {'ip_dhcp_snoop': {'active': 0}, 'ip_arp_inspection': {'active': 0}, 'active_service': {'password-encryption': 1, ...}}
def global_params_check(global_params):
    global_params_results_dict = {'ip_dhcp_snoop':{}, 'ip_arp_inspection':{}, 'active_service':{}, 'disable_service':{},
                                  'users':{}, 'line':{}, 'ip_ssh':{}}

# active services section
    if 'password-encryption' in global_params['active_service']:
        global_params_results_dict['active_service']['password-encryption'] = 1
    else:
        global_params_results_dict['active_service']['password-encryption'] = 0
    if 'tcp-keepalives-in' in global_params['active_service']:
        global_params_results_dict['active_service']['tcp-keepalives-in'] = 1
    else:
        global_params_results_dict['active_service']['tcp-keepalives-in'] = 2
    if 'udp-small-servers' in global_params['active_service']:
        global_params_results_dict['active_service']['udp-small-servers'] = 0
    else:
        global_params_results_dict['active_service']['udp-small-servers'] = 1
    if 'tcp-small-servers' in global_params['active_service']:
        global_params_results_dict['active_service']['tcp-small-servers'] = 0
    else:
        global_params_results_dict['active_service']['tcp-small-servers'] = 1

# disable services section
    if 'pad' in global_params['disable_service']:
        global_params_results_dict['disable_service']['pad'] = 1
    else:
        global_params_results_dict['disable_service']['pad'] = 0

# enable password section
    if 'enable_password' in global_params:
        if global_params['enable_password'] == '5':
            global_params_results_dict['enable_password'] = 1
        else:
            global_params_results_dict['enable_password'] = 0

# users section
    for user in global_params['users']:
        global_params_results_dict['users'][user] = {}
        if global_params['users'][user]['password_type'] == '5':
            global_params_results_dict['users'][user]['password_type'] = 1
        else:
            global_params_results_dict['users'][user]['password_type'] = 0
        if 'privilege' in global_params['users'][user]:
            if global_params['users'][user]['privilege'] == '15':
                global_params_results_dict['users'][user]['privilege'] = 2

# IP DHCP snooping section
    if global_params['ip_dhcp_snoop']['active'] == 'yes':
        global_params_results_dict['ip_dhcp_snoop']['active'] = 1
    else:
        global_params_results_dict['ip_dhcp_snoop']['active'] = 0

# IP ARP inspection section
    if global_params['ip_arp_inspection']['active'] == 'yes':
        global_params_results_dict['ip_arp_inspection']['active'] = 1
    else:
        global_params_results_dict['ip_arp_inspection']['active'] = 0

# ssh section
    if 'version' in global_params['ip_ssh']:
        if global_params['ip_ssh']['version'] == '2':
            global_params_results_dict['ip_ssh']['version'] = 1
        else:
            global_params_results_dict['ip_ssh']['version'] = 2
    if 'authentication-retries' in global_params['ip_ssh']:
        if int(global_params['ip_ssh']['authentication-retries']) > 5:
            global_params_results_dict['ip_ssh']['authentication-retries'] = 2
    if 'time-out' in global_params['ip_ssh']:
        if int(global_params['ip_ssh']['time-out']) < 100:
            global_params_results_dict['ip_ssh']['time-out'] = 1
        elif 100 < int(global_params['ip_ssh']['time-out']) <= 300:
            global_params_results_dict['ip_ssh']['time-out'] = 2
        elif int(global_params['ip_ssh']['time-out']) > 300:
            global_params_results_dict['ip_ssh']['time-out'] = 0

# console and vty lines section
    for line in global_params['line']:
        global_params_results_dict['line'][line] = {}
        if 'log_sync' in global_params['line'][line]:
            if global_params['line'][line]['log_sync'] == 'yes':
                global_params_results_dict['line'][line]['log_sync'] = 1
            else:
                global_params_results_dict['line'][line]['log_sync'] = 2
        if 'exec_timeout' in global_params['line'][line]:
            if global_params['line'][line]['exec_timeout'] < 15:
                global_params_results_dict['line'][line]['exec_timeout'] = 1
            elif 15 < global_params['line'][line]['exec_timeout'] <= 30:
                global_params_results_dict['line'][line]['exec_timeout'] = 2
            elif global_params['line'][line]['exec_timeout'] > 30:
                global_params_results_dict['line'][line]['exec_timeout'] = 0
        if 'privilege' in global_params['line'][line]:
            if global_params['line'][line]['privilege'] == '15':
                global_params_results_dict['line'][line]['privilege'] = 2
        if 'transp_in' in global_params['line'][line]:
            if global_params['line'][line]['transp_in'] == 'ssh':
                global_params_results_dict['line'][line]['transp_in'] = 1
            else:
                global_params_results_dict['line'][line]['transp_in'] = 2
        if 'transp_out' in global_params['line'][line]:
            if global_params['line'][line]['transp_out'] == 'ssh':
                global_params_results_dict['line'][line]['transp_out'] = 1
            else:
                global_params_results_dict['line'][line]['transp_out'] = 2
    return global_params_results_dict


# Display global options check result
# INPUT:  dictionary from global_params_check function
# SAMPLE: see global_params_check output
# OUTPUT: display option name and its grade
# SAMPLE: 'ip_arp_inspection active IS BAD'
def show_global_options(dictionary):
    for key in dictionary:
        print(key, end=' ')
        if dictionary[key] == 0 or dictionary[key] == 1 or dictionary[key] == 2:
            if dictionary[key] == 0:
                print('IS BAD')
            elif dictionary[key] == 1:
                print('IS GOOD')
            elif dictionary[key] == 2:
                print('IS WARNING')
        else:
            show_global_options(dictionary[key])
            print('\n')
            
# FOR DEBUG
#
# import parsing
#
# for fname in parsing.filenames:
#     result_dictionary = global_params_check(parsing.global_params[fname])
#     print(result_dictionary)
#     show_global_options(result_dictionary)


