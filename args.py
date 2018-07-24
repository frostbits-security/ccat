# command line arguments parsing
# input: full path of the directory with config[s]+ filename of vlanmap
# vlanmap structure can be seen in example folder (vlmap.txt)
import argparse
import os


def arg_parser(config_folder, vlanmap):
    res = []
    if vlanmap:
        if os.path.exists(vlanmap):
            res.append(vlanmap)
        else:
            print('Incorrect vlanmap name!')
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

def getargs():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description="This is Cisco Configuration Analyzer Tool[CCAT].\nYou must load config to work. By default config is in example folder.",
                                     epilog='Usage example:\n  ccat\n  ccat  smth/config_folder -vl smth/vlanmap_folder -v')
    parser.add_argument("config", type=str, nargs='?', default="example", help="full path of the folder with config[s]")
    parser.add_argument("-vl", type=str, help="full path of the folder with vlanmap")
    parser.add_argument("-v", action='store_true', help="increase verbosity")
    parser.add_argument("--noIPv6", action='store_true', help="turn off IPv6 check")
    args = parser.parse_args()
    return arg_parser(args.config, args.vl)
