# command line arguments parsing
# input: full path of the directory with config[s]+ filename of vlanmap
# vlanmap structure can be seen in example folder (vlmap.txt)
import argparse
import os

# to make possible access to args from main module
args=0

def _getargs___arg_parser(config_folder, vlanmap):
    res = []
    if vlanmap:
        if os.path.exists(vlanmap):
            res.append(vlanmap)
        else:
            print('Error opening vlanmap')
            exit()
    else:
        res.append(0)
    try:
        config_lst = [config_folder + '/' + i for i in os.listdir(config_folder)]
        if vlanmap in config_lst:
            config_lst.remove(vlanmap)
        res.append(config_lst)
    except OSError:
        print('The directory doesn`t exist!')
        exit()
    return res


# module main, returns list of filepaths list[0] is vlanmap, others are configs

def getfilenames():
    global args
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description="Cisco Configuration Analysis Tool",
                                     epilog='Usage example:\n  ccat  smth/config_folder -vl smth/vlanmap_folder -v')
    parser.add_argument("config", type=str, nargs='?', default=0, help="full path to the folder with config(s)")
    parser.add_argument("-vl", type=str, help="path to vlanmap (file that determine how critical is certain vlan, you can find example in 'example' folder)")
    parser.add_argument("-o", type=str, help="path to output html files directory")
    parser.add_argument("--no-ipv6", action='store_true', help="if you're not using IPv6")
    parser.add_argument("--disabled-interfaces", action='store_true', help="check interfaces even if they are turned off")
    parser.add_argument("--storm_level", type=float, help="to set up appropriate level for storm-control (by default value=80)")
    parser.add_argument("--max_number_mac", type=int, help="to set up maximum number of mac-addresses for port-security (by default value=10)")
    args = parser.parse_args()
    if not(args.config):
        print ('Usage example:\n  ccat  smth/config_folder -vl smth/vlanmap_folder -v\n\nFor more details try --help')
        exit()
    return _getargs___arg_parser(args.config, args.vl)