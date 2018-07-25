#!/usr/bin/env python3
import args
import parsing
filenames=args.getfilenames()
print (args.args)
vlanmap=parsing.vlanmap_parse(filenames[0])
print(vlanmap)
filenames.pop(0)
print(filenames)
interfaces=parsing.interface_parse(filenames)
global_params=parsing.global_parse(filenames)

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
