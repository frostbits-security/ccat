#!/usr/bin/env python3
import args
import parsing
filenames=args.getfilenames()
print (args.args)
vlanmap=parsing.vlanmap_parse(filenames.pop(0))
print(vlanmap)
interfaces=parsing.interface_parse(filenames[0])
global_params=parsing.global_parse(filenames[0])

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
