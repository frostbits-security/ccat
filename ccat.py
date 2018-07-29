#!/usr/bin/env python3
import args
import parsing
import checks
filenames=args.getfilenames()
print (args.args)
vlanmap=parsing.vlanmap_parse(filenames.pop(0))
print(vlanmap)
interfaces=parsing.interface_parse(filenames[0])
global_params=parsing.global_parse(filenames[0])

# Scoring system. 
# Determines severity of misconfiguration errors from 1 to 3 (critical)

score={}
# Main loop
for i in global_params:
	# Main idea - make all checks here and have some score to determine which config is worse
	# One loop iteration = one config file

	# Creating a list for scores of this config
	score[i]=[]
	
	print ("\nAnalysing "+i+" :")
	score[i].append(checks.dhcp_snoop(global_params[i],interfaces[i],vlanmap,args.args.disabled_interfaces))
	#score[i].append(checks.arp_inspection(global_params[i],interfaces[i]))

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
