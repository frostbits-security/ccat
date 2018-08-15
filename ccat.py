#!/usr/bin/env python3
import os
import args
import parsing
import display
import checks
from checks import *

# get filenames from args
filenames = args.getfilenames()
# debug output
print(args.args)
# get vlanmap
vlanmap = parsing.vlanmap_parse(filenames.pop(0))


html_directory   = None
html_file        = None
config_directory = args.args.config
# Create directory for html files output or check its exist
if args.args.o:
    html_directory   = args.args.o
    try:
        os.makedirs(html_directory, exist_ok=True)
    except OSError:
        html_directory = html_directory[:-1] + '\\'
        os.makedirs(html_directory, exist_ok=True)


# processing configs one by one
for filename in filenames[0]:
    # Define config file name
    config_name = filename.partition(config_directory)[2]

    # Create output html file full path if needed
    if html_directory:
        html_file = html_directory + config_name + '.html'

    # parsing configs
    parsing.parseconfigs(filename)

    # getting parse output
    interfaces = parsing.iface_local
    global_params = parsing.iface_global

    # prepare results dictionary
    print('\n\n--------------------RESULTS FOR:', config_name[1:]+'--------------------')
    result_dict = {'Services': {}, 'EXEC password': {}, 'Users': {}, 'IP options': {'dhcp_snooping': {},
                    'arp_inspection': {}, 'SSH': {}, 'service': {}, 'WEB server':{}}, 'Lines': {},'Spanning-tree':{}}

    # global checks
    result_dict.update(checks.services   .check(global_params))
    result_dict.update(checks.users      .check(global_params))
    result_dict.update(checks.ip_global  .check(global_params))
    result_dict.update(checks.console_vty.check(global_params))

    result,bpdu_flag = checks.stp_global .check(global_params)
    result_dict['Spanning-tree'].update(result)

    # Need to divide these checks to interfaces and global options (remain global checks here and add interface checks to
    # cycle below) to avoid more than 1 interfaces iteration (there are 2 here and 1 below now, thats not good for speed)
    #
    # checks.arp_inspection.check (global_params, interfaces, vlanmap, args.args.disabled_interfaces, result_dict)
    # checks.dhcp_snooping.check  (global_params, interfaces, vlanmap, args.args.disabled_interfaces, result_dict)


    # interface-only checks
    for iface in interfaces:
        if 'unknow_inface' not in interfaces[iface]:
            if 'loop' not in iface.lower() and 'vlan' not in iface.lower() and interfaces[iface][
                'shutdown'] == 'no':
                result_dict[iface] = {}
                
                result_dict[iface].update(checks.cdp.check(interfaces[iface]))
                result_dict[iface].update(checks.dtp.check(interfaces[iface]))

                stp_result = checks.stp.check(interfaces[iface], bpdu_flag)

                if stp_result != 0:
                    result_dict[iface].update(stp_result)

                if args.args.storm_level:
                    result_dict[iface].update(checks.storm_control.check(interfaces[iface], args.args.storm_level))
                else:
                    result_dict[iface].update(checks.storm_control.check(interfaces[iface]))

                if args.args.max_number_mac:
                    port_result =checks.port_security.check(interfaces[iface], args.args.max_number_mac)
                else:
                    port_result=checks.port_security.check(interfaces[iface])

                if port_result != 0:
                    result_dict[iface].update(port_result)
        else:
            result_dict[iface] = {'Unused Interface': [0, 'ENABLE', 'An interface that is not used must be disabled']}

            # Trunk/access check
            # checks.mode.check           (interfaces, result_dict)

    # processing results
    display.display_results(result_dict,html_file)

# Do we really need scoring system ?
#
# Scoring system.
# Determines severity of misconfiguration errors from 1 to 3 (critical)

# score = {}
# # Main loop
# for i in global_params:
#     # Main idea - make all checks here and have some score to determine which config is worse
#     # One loop iteration = one config file
#
#     # Creating a list for scores of this config
#     score[i] = []
#
#     print("\nAnalysing " + i + ":")
#     score[i].append(checks.dhcp_snooping.check(global_params[i], interfaces[i], vlanmap, args.args.disabled_interfaces))
# # score[i].append(checks.arp_inspection(global_params[i],interfaces[i]))
#
# print()
# print(score)
