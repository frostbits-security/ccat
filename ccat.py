#!/usr/bin/env python3
import args
import parsing
import checks.dhcp_snooping
import checks.arp_inspection

filenames = args.getfilenames()
print(args.args)
vlanmap = parsing.vlanmap_parse(filenames.pop(0))
parsing.parseconfigs(filenames[0])
interfaces = parsing.iface_local
global_params = parsing.iface_global


# Scoring system. 
# Determines severity of misconfiguration errors from 1 to 3 (critical)

score = {}
# Main loop
for i in global_params:
    # Main idea - make all checks here and have some score to determine which config is worse
    # One loop iteration = one config file

    # Creating a list for scores of this config
    score[i] = []

    print("\nAnalysing " + i + ":")
    score[i].append(checks.dhcp_snooping.check(global_params[i], interfaces[i], vlanmap, args.args.disabled_interfaces))
# score[i].append(checks.arp_inspection(global_params[i],interfaces[i]))

print()
print(score)

# Output for debug
#
# for fname in filenames:
#     print('\n', fname, 'global options:\n')
#     for key in global_params[fname]:
#         print(key, global_params[fname][key])
#
#     print('\n', fname, 'interface options:\n')
#     for key in interfaces[fname]:
#         print(key, interfaces[fname][key])
#
#
# Example with global options check and display results
#
# import checks.console_vty
# import checks.ip_global
# import checks.services
# import checks.users
# import checks.display
# for filename in global_params:
# 	print('\nRESULTS FOR', filename)
# 	result_dict = {'active_service': {}, 'disable_service': {}, 'enable_password':{}, 'users': {}, 'ip':
# 				  {'dhcp_snooping': {}, 'arp_inspection': {}, 'ssh': {}, 'active_service': {}},  'line': {}}
#
# 	checks.console_vty.check(global_params[filename], result_dict)
# 	checks.ip_global.check(global_params[filename], result_dict)
# 	checks.services.check(global_params[filename], result_dict)
# 	checks.users.check(global_params[filename], result_dict)
#
# 	checks.display.display_results(result_dict)
