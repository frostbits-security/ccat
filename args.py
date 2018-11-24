# Command line arguments parsing
# Input:
#        full path of the configuration_file/directory with config[s]
#        filename of vlanmap
# Output:
#        list of config[s]+vlanmap
#
# vlanmap structure can be seen in example folder (vlmap.txt)

import argparse
import os
from sys import exit

# to make possible access to args from main module
args=0

def _getargs___arg_parser(config, vlanmap):
    result = []
    if vlanmap:
        if os.path.exists(vlanmap):
            result.append(vlanmap)
        else:
            print('Error opening vlanmap')
            exit()
    else:
        result.append(0)
    try:
        if os.path.isdir(config):
            config_lst = [config + i for i in os.listdir(config)]
            if vlanmap in config_lst:
                config_lst.remove(vlanmap)
            result.append(config_lst)
        elif os.path.isfile(config):
            result.append([config])
    except OSError:
        exit()
    return result


# module main, returns list of filepaths list[0] is vlanmap, others are configs

def getfilenames():
    global args
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description="Cisco Configuration Analysis Tool",
                                     epilog='Usage example:\n  ccat  smth/config_folder -vlanmap smth/vlanmap_file')
    parser.add_argument("configs", type=str, nargs='?', default=0, help="full path to the configuration file or folder with config(s)")
    parser.add_argument("-vlanmap", type=str, help="path to vlanmap (file that determine how critical is certain vlan, you can find example in 'example' folder)")
    parser.add_argument("-output", type=str, help="path to output html files directory")
    parser.add_argument("--no-console-display", action='store_true', help="to output analysis results in html files directory or into network graph")
    parser.add_argument("--no-ipv6", action='store_true', help="if you're not using IPv6")
    parser.add_argument("--disabled-interfaces", action='store_true', help="check interfaces even if they are turned off")
    parser.add_argument("--storm_level", type=float, help="to set up appropriate level for storm-control (by default value=80)")
    parser.add_argument("--max_number_mac", type=int, help="to set up maximum number of mac-addresses for port-security (by default value=10)")
    parser.add_argument("--dump-creds", action='store_true', help="enable credentials harvesting")
    parser.add_argument("--debug", action='store_true', help="enable debug output")
    graph_group = parser.add_argument_group('Network graph')
    graph_group.add_argument("--graph", type=str, nargs='?', default=0, help="left the argument empty to get into interactive mode or define a file name for graph output in png extension")
    args = parser.parse_args()
    if not(args.configs):
        print ('Usage example:\n  ccat  smth/config_folder -vlanmap smth/vlanmap_file\n\nFor more details try --help')
        exit()
    if args.no_console_display and not args.output and args.graph == 0:
        print('\nYou should define html files directory with -output key OR use --graph key to use this options\n\nFor more details try --help')
        exit()
    return _getargs___arg_parser(args.configs, args.vlanmap)
