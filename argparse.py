#на вход полный путь к папке с конфигами и картой сети, название файла с картой сети
import argparse
import os
parser = argparse.ArgumentParser()
parser.add_argument("-vl", "--vlanmap",type=str, help="file name of vlanmap")
parser.add_argument("-c","--config",type=str, help="full path of the folder with config[s] and vlanmap")
args = parser.parse_args()
if args.vlanmap and args.config:
    config_lst=[args.config+'/'+i for i in os.listdir(args.config)]
    vlanmap=args.config+'/'+args.vlanmap
    try:
        config_lst.remove(vlanmap)
        for each in config_lst:
            with open(each,'r') as f:
                pass
    except ValueError:
        print('incorrect vlanmap name!')
else:
    print("you must load config[s] and vlanmap!")