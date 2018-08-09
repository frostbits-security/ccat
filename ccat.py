#!/usr/bin/env python3
import args
import parsing
import display
import checks
from checks import *

filenames = args.getfilenames()
print(args.args)
vlanmap = parsing.vlanmap_parse(filenames.pop(0))
outtype=None
file=None

if(args.args.o):
    file=open(args.args.o,'w')
    if(args.args.o[-4:]=='html'):
        outtype='html'
    else:
        outtype='txt'
if(outtype=='html'):
        file.write("<!doctype html><html><head></head><body><table>")

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

#    checks.arp_inspection.check (global_params[filename], interfaces[filename], vlanmap, args.args.disabled_interfaces, result_dict)
#     checks.dhcp_snooping.check  (global_params[filename], interfaces[filename], vlanmap, args.args.disabled_interfaces, result_dict)

    # checks.mode.check           (interfaces[filename], result_dict)


    # Need to change these functions like 4 above
    #
    # checks.storm_control.check  (interfaces[filename], result_dict)
    # checks.stp_global.check     (interfaces[filename], result_dict)
    for iface in interfaces[filename]:
        if 'loop' not in iface.lower() and 'vlan' not in iface.lower():
            result_dict[iface] = {}
            result_dict[iface].update(checks.storm_control.check(interfaces[filename][iface]))
            result_dict[iface].update(checks.cdp.check(interfaces[filename][iface]))
            result_dict[iface].update(checks.dtp.check(interfaces[filename][iface]))
            result_dict[iface].update(checks.stp.check(interfaces[filename][iface]))
    
    if(outtype and outtype=='txt'):
        file.write(key)
    elif(outtype):
        file.write('<tr><td style="color:blue; font-size: 2em;">' + filename + '</td><td></td></tr>\n')
    display.display_results(result_dict,file,outtype)

if(outtype=='html'):
    file.write('<tr><td>&nbsp;</td></tr>\n</table></body></html>')
    
if(outtype):
    file.close()

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
