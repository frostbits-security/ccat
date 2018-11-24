#!/usr/bin/env python3
import os
import args
import parsing
import progressbar
import display
import interface_type
import checks
import graph
import harvester
from checks import *

# get filenames from args
filenames = args.getfilenames()

# get vlanmap
vlanmap = parsing.vlanmap_parse(filenames.pop(0))

# variables for html output option
html_directory = None
html_file = None
config_directory = args.args.configs
# Create directory for html files output or check its existence
if args.args.output:
    html_directory = args.args.output
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
        progressbar.Bar(left='[', marker='=', right=']'),  # Прогресс
        progressbar.SimpleProgress(),
    ]).start()

# Creating dictionary for drawing graph
dict_for_drawing_plot = {}
# creds harvester
if (args.args.dump_creds):
    harvester.harvest(filenames[0])

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
    global_params = parsing.iface_global
    interfaces = parsing.iface_local

    # debug output
    if (args.args.debug):
        print("\n\n[DEBUG] args:")
        print(args.args)
        print("\n\n[DEBUG] global:")
        print(global_params)
        print("\n\n[DEBUG] iface:")
        print(interfaces)
        print("\n\n[DEBUG] vlanmap:")
        print(vlanmap)

    if not no_console_display:
        print('\n\n-------------------- RESULTS FOR: {} --------------------'.format(config_name))

    # prepare results dictionary
    result_dict = {}

    # global checks
    result_dict.update(checks.services.check(global_params))
    # result_dict.update(checks.users.check(global_params))
    result_dict.update(checks.ip_global.check(global_params))
    result_dict.update(checks.console_vty.check(global_params))
    result_dict.update(checks.lldp.check(global_params))
    result_dict.update(checks.aaa.check(global_params))

    result_cdp, cdp_flag = checks.cdp.global_check(global_params)
    if result_cdp:
        result_dict.update(result_cdp)

    result_vtp = checks.vtp.check(global_params)
    if result_vtp:
        result_dict.update(result_vtp)

    # global checks with necessary flags for further interface checks
    result, bpdu_flag = checks.stp.global_check(global_params)
    result_dict.update(result)

    result_arp, arp_flag = checks.arp_inspection.check_global(global_params, result_dict)
    result_dict.update(result_arp)

    result_dhcp, dhcp_flag = checks.dhcp_snooping.check_global(global_params, result_dict)
    result_dict.update(result_dhcp)

    result_dict['IPv6 options'] = {}

    result_raguard, raguard_flag = checks.ipv6.raguard_global(global_params, result_dict)
    result_dict.update(result_raguard)

    result_snooping, snooping_flag = checks.ipv6.snooping_global(global_params, result_dict)
    result_dict.update(result_snooping)

    result_sourceguard, sourceguard_flag = checks.ipv6.sourceguard_global(global_params, result_dict)
    result_dict.update(result_sourceguard)

    result_dhcpguard, dhcpguard_flag = checks.ipv6.dhcpguard_global(global_params, result_dict)
    result_dict.update(result_dhcpguard)

    result_destinationguard, destinationguard_flag = checks.ipv6.destinationguard_global(global_params, result_dict)
    result_dict.update(result_destinationguard)

    arp_proxy_flag, arp_proxy = checks.arp_proxy.global_check(global_params)

    if arp_proxy_flag:
        result_dict.update(arp_proxy)

    # Adding device name to dictionary
    dict_for_drawing_plot.update({config_name: {}})

    # interface checks
    for iface in interfaces:

        # check interface if it has at least 1 options
        if 'unknown_iface' not in interfaces[iface]:

            # skip loopback and vlan interfaces
            if 'loop' not in iface.lower() and 'vlan' not in iface.lower():

                # skip shutdown interfaces if there was not --disabled-interfaces argument
                if interfaces[iface]['shutdown'] == 'yes' and not check_disabled:
                    continue

                # If an interface has any vlans - it is added to dictionary for graph
                if interfaces[iface]['vlans']:
                    dict_for_drawing_plot[config_name].update({iface: interfaces[iface]['vlans']})

                result_dict[iface] = {}

                # set DISABLE status if interface is shutdown and disabled-interfaces argument is true
                if interfaces[iface]['shutdown'] == 'yes' and check_disabled:
                    result_dict[iface]['status'] = [3, 'SHUTDOWN']

                # If type is not defined - interface is working in Dynamic Auto mode
                if 'type' not in interfaces[iface]:
                    result_dict[iface]['mode'] = [0, 'DYNAMIC',
                                                  'The interfaces of your switches must be in trunk or access mode.']

                # determine vlanmap type (critical/unknown/trusted) if vlanmap defined and interface has at least 1 vlan
                if vlanmap and interfaces[iface]['vlans']:
                    result_dict[iface].update(interface_type.determine(vlanmap, interfaces[iface]))
                    # set vlanmap result as 'CRITICAL' / 'UNKNOWN' / 'TRUSTED'
                    vlanmap_result = result_dict[iface]['vlanmap type'][1]
                else:
                    vlanmap_result = None

                # access/trunk mode check
                result_dict[iface].update(checks.mode.check(interfaces[iface]))

                # check cdp, dtp, mop and source guard options on current interface
                result_dict[iface].update(checks.dtp.check(global_params, interfaces[iface], vlanmap_result))
                result_dict[iface].update(checks.mop.check(interfaces[iface], vlanmap_result, iface))
                result_dict[iface].update(checks.source_guard.check(interfaces[iface], dhcp_flag, vlanmap_result))

                cdp_result = checks.cdp.iface_check(interfaces[iface], vlanmap_result, cdp_flag)
                if cdp_result:
                    result_dict[iface].update(cdp_result)

                stp_result = checks.stp.iface_check(interfaces[iface], bpdu_flag, vlanmap_result)

                if stp_result:
                    result_dict[iface].update(stp_result)

                dhcp_result = checks.dhcp_snooping.check_iface(interfaces[iface], vlanmap_result,
                                                               args.args.disabled_interfaces, dhcp_flag)

                if dhcp_result:
                    result_dict[iface].update(dhcp_result)

                if arp_proxy_flag == 0:
                    arp_proxy_result = checks.arp_proxy.iface_check(interfaces[iface], vlanmap_result)
                    result_dict[iface].update(arp_proxy_result)

                arp_result = checks.arp_inspection.check_iface(interfaces[iface], vlanmap_result,
                                                               args.args.disabled_interfaces,
                                                               arp_flag)
                if arp_result:
                    result_dict[iface].update(arp_result)
                result_dict[iface]['IPv6'] = {}
                sourceguard_result = checks.ipv6.sourceguard_iface(interfaces[iface], vlanmap_result,
                                                                   args.args.disabled_interfaces, sourceguard_flag)
                if sourceguard_result:
                    result_dict[iface]['IPv6'].update(sourceguard_result)
                raguard_result = checks.ipv6.raguard_iface(interfaces[iface], vlanmap_result,
                                                           args.args.disabled_interfaces, raguard_flag)
                if raguard_result:
                    result_dict[iface]['IPv6'].update(raguard_result)
                destinationguard_result = checks.ipv6.destinationguard_iface(interfaces[iface], vlanmap_result,
                                                                             args.args.disabled_interfaces,
                                                                             destinationguard_flag)
                if destinationguard_result:
                    result_dict[iface]['IPv6'].update(destinationguard_result)
                dhcpguard_result = checks.ipv6.dhcpguard_iface(interfaces[iface], vlanmap_result,
                                                               args.args.disabled_interfaces, dhcpguard_flag)
                if dhcpguard_result:
                    result_dict[iface]['IPv6'].update(dhcpguard_result)

                if args.args.storm_level:
                    result_dict[iface].update(
                        checks.storm_control.check(interfaces[iface], vlanmap_result, args.args.storm_level))
                else:
                    result_dict[iface].update(checks.storm_control.check(interfaces[iface], vlanmap_result))

                if args.args.max_number_mac:
                    port_result = checks.port_security.check(interfaces[iface], vlanmap_result,
                                                             args.args.max_number_mac)
                else:
                    port_result = checks.port_security.check(interfaces[iface], vlanmap_result)

                if port_result:
                    result_dict[iface].update(port_result)


        else:
            result_dict[iface] = {'Unused Interface': [0, 'ENABLED', 'An interface that is not used must be disabled']}

    if (args.args.debug):
        print("\n\n[DEBUG] results:")
        print(result_dict)

    # processing results
    display.display_results(result_dict, html_file, no_console_display)

    # update progress bar if it is enabled
    if no_console_display:
        config_checked += 1
        bar.update(config_checked)

# finish progress bar
if no_console_display:
    bar.finish()

# Draw gpaph if the key was defined
if args.args.graph != 0:
    graph.draw_plot(dict_for_drawing_plot, args.args.graph, vlanmap)

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