#!/usr/bin/env python3
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

# prepare vars for file output
outtype=None
file=None
# check ouput type
if(args.args.o):
    file=open(args.args.o,'w')
    if(args.args.o[-4:]=='html'):
        outtype='html'
    else:
        outtype='txt'
# prepare html file
if(outtype=='html'):
        file.write("<!doctype html><html><head></head><body><table>")

# processing configs one by one
for filename in filenames[0]:
    # parsing configs
    parsing.parseconfigs(filename)
    # getting parse output
    interfaces = parsing.iface_local
    global_params = parsing.iface_global
    # prepare results dictionary
    print('\n\nRESULTS FOR', filename)
    result_dict = {'services': {}, 'enable_password': {}, 'users': {}, 'ip':
        {'dhcp_snooping': {}, 'arp_inspection': {}, 'ssh': {}, 'active_service': {}}, 'line': {}}

    # checks
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
    
    # interface-only checks
    for iface in interfaces[filename]:
        if 'loop' not in iface.lower() and 'vlan' not in iface.lower():
            result_dict[iface] = {}
            result_dict[iface].update(checks.storm_control.check(interfaces[filename][iface]))
            result_dict[iface].update(checks.cdp.check(interfaces[filename][iface]))
            result_dict[iface].update(checks.dtp.check(interfaces[filename][iface]))
            result_dict[iface].update(checks.stp.check(interfaces[filename][iface]))
    # writing filename to output file
    if(outtype and outtype=='txt'):
        file.write('\n\n'+filename+':\n\n')
    # same in html
    elif(outtype):
        file.write('<tr><td style="color:blue; font-size: 2em;">' + filename + ':</td><td></td></tr>\n')
    # processing results
    display.display_results(result_dict,file,outtype)

# closing files
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
