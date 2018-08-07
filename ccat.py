#!/usr/bin/env python3
import args
import parsing
import checks
from checks import *

filenames = args.getfilenames()
print(args.args)
vlanmap = parsing.vlanmap_parse(filenames.pop(0))
for filename in filenames[0]:
    parsing.parseconfigs(filename)
    interfaces = parsing.iface_local
    global_params = parsing.iface_global
    print('\n\nRESULTS FOR', filename)
    result_dict = {'services': {}, 'enable_password': {}, 'users': {}, 'ip':
        {'dhcp_snooping': {}, 'arp_inspection': {}, 'ssh': {}, 'active_service': {}}, 'line': {}}

    checks.services.check       (global_params[filename], result_dict)
    checks.users.check          (global_params[filename], result_dict)
    checks.ip_global.check      (global_params[filename], result_dict)
    checks.console_vty.check    (global_params[filename], result_dict)

    # Need to unify these functions
    #
    # allinterf = 'something'
    # checks.arp_inspection.check (global_params[filename], interfaces[filename], vlanmap, allinterf, result_dict)
    # checks.dhcp_snooping.check  (global_params[filename], interfaces[filename], vlanmap, allinterf, result_dict)

    checks.cdp.check            (interfaces[filename], result_dict)
    checks.dtp.check            (interfaces[filename], result_dict)
    checks.mode.check           (interfaces[filename], result_dict)
    checks.stp.check            (interfaces[filename], result_dict)

    # Need to change these functions like 4 above
    #
    # checks.storm_control.check  (interfaces[filename], result_dict)
    # checks.stp_global.check     (interfaces[filename], result_dict)

    checks.display.display_results(result_dict)#, filename)

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
