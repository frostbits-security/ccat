#!/usr/bin/env python3
import os
import args
import parsing
#import progressbar
import display
import interface_type
import checks
from checks import *

# get filenames from args
filenames = args.getfilenames()

# debug output
print(args.args)

# get vlanmap
vlanmap = parsing.vlanmap_parse(filenames.pop(0))

# variables for html output option
html_directory   = None
html_file        = None
config_directory = args.args.config
# Create directory for html files output or check its exist
if args.args.o:
    html_directory = args.args.o
    try:
        os.makedirs(html_directory, exist_ok=True)
    except OSError:
        html_directory = html_directory[:-1] + '\\'
        os.makedirs(html_directory, exist_ok=True)

# check shutdown interfaces flag
if args.args.disabled_interfaces:
    check_disabled = True
else:
    check_disabled = False

# output results only into html files directory
if args.args.no_console_display:
    no_console_display = True
else:
    no_console_display = False

# start progress bar for html output files
if no_console_display:
    config_number = len(filenames[0])
    config_checked = 0
    bar = progressbar.ProgressBar(maxval=config_number, widgets=[
        progressbar.Bar(left='[', marker='=', right=']'), # Прогресс
        progressbar.SimpleProgress(),
    ]).start()

# processing configs one by one
for filename in filenames[0]:

    # Define config file name
    config_name = filename.partition(config_directory)[2]

    # Create output html file full path if needed
    if html_directory:
        html_file = html_directory + config_name + '.html'

    # parsing configs
    parsing.parseconfigs(filename, check_disabled)

    # getting parse output
    interfaces    = parsing.iface_local
    global_params = parsing.iface_global

    if no_console_display == False:
        print('\n\n--------------------RESULTS FOR:', config_name[1:] + '--------------------')

    # prepare results dictionary
    # WE CAN DELETE IT AND USE .update ATTRIBUTE TO FILL DICTIONARY
    result_dict = {'IP options': {'dhcp_snooping': {}, 'arp_inspection': {}} }

    # global checks
    result_dict.update(checks.services   .check(global_params))
    result_dict.update(checks.users      .check(global_params))
    result_dict.update(checks.ip_global  .check(global_params))
    result_dict.update(checks.console_vty.check(global_params))

    result_vtp=checks.vtp.check(global_params)
    if result_vtp:
        result_dict.update(result_vtp)


    # global checks with nessesary flags for further interface checks
    result,      bpdu_flag = checks.stp_global       .check(global_params)
    result_dict.update(result)

    result_arp,   arp_flag = checks.arp_insp_global  .check(global_params,result_dict)
    result_dict.update(result_arp)

    result_dhcp, dhcp_flag = checks.dhcp_snoop_global.check(global_params,result_dict)
    result_dict.update(result_dhcp)

    # interface checks
    for iface in interfaces:

        # check interface if it has at least 1 options
        if 'unknow_inface' not in interfaces[iface]:

            # skip loopback and vlan interfaces
            if 'loop' not in iface.lower() and 'vlan' not in iface.lower():

                # skip shutdown interfaces if there was not --disabled-interfaces argument
                if   interfaces[iface]['shutdown'] == 'yes' and check_disabled == False:
                    continue

                result_dict[iface] = {}

                # set DISABLE status if interface is shutdown and disabled-interfaces argument is true
                if interfaces[iface]['shutdown'] == 'yes' and check_disabled == True:
                    result_dict[iface]['status'] = [3,'DISABLED']

                # If type is not defined - interface is working in Dynamic Auto mode
                if 'type' not in interfaces[iface]:
                    result_dict[iface]['mode'] = [0, 'DYNAMIC', 'The interfaces of your switches must be in trunk or access mode.']

                # determine vlanmap type (critical/unknown/trusted) if vlanmap defined and interface has at least 1 vlan
                if vlanmap and interfaces[iface]['vlans']:
                    result_dict[iface].update(interface_type.determine(vlanmap, interfaces[iface]))
                    # set vlanmap result as 'CRITICAL' / 'UNKNOWN' / 'TRUSTED'
                    vlanmap_result = result_dict[iface]['vlanmap type'][1]
                else:
                    vlanmap_result = None


                # example with using vlanmap_result type
                result_dict[iface].update(checks.cdp .check(interfaces[iface], vlanmap_result))
                result_dict[iface].update(checks.dtp .check(interfaces[iface]))
                result_dict[iface].update(checks.source_guard.check(interfaces[iface],dhcp_flag))

                stp_result = checks.stp.check(interfaces[iface], bpdu_flag)

                if stp_result:
                    result_dict[iface].update(stp_result)

                dhcp_result = checks.dhcp_snooping.check(interfaces[iface], vlanmap, args.args.disabled_interfaces,dhcp_flag)

                if dhcp_result:
                    result_dict[iface].update(dhcp_result)

                arp_result = checks.arp_inspection.check(interfaces[iface], vlanmap, args.args.disabled_interfaces,
                                                         arp_flag)

                if arp_result:
                    result_dict[iface].update(arp_result)

                if args.args.storm_level:
                    result_dict[iface].update(checks.storm_control.check(interfaces[iface], args.args.storm_level))
                else:
                    result_dict[iface].update(checks.storm_control.check(interfaces[iface]))

                if args.args.max_number_mac:
                    port_result = checks.port_security.check(interfaces[iface], args.args.max_number_mac)
                else:
                    port_result=checks.port_security.check(interfaces[iface])

                if port_result:
                    result_dict[iface].update(port_result)


                # access/trunk mode check
                # result_dict[iface].update(checks.mode.check(interfaces[iface]))
        else:
            result_dict[iface] = {'Unused Interface': [0, 'ENABLE', 'An interface that is not used must be disabled']}

    # processing results
    display.display_results(result_dict,html_file, no_console_display)

    # update progress bar if it is enabled
    if no_console_display:
        config_checked += 1
        bar.update(config_checked)

# finish progress bar
if no_console_display:
    bar.finish()


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