#!/usr/bin/env python3
#на вход полный путь к папке с конфигами и картой сети, название файла с картой сети
import argparse
import os
import re
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

# let the parse begin!
vmapf=open(vlanmap,"r")
vlanmap=vmapf.read()
vmapf.close()
vlanpattern=re.compile(': ([0-9,]+)')
vlanmap=re.findall(vlanpattern,vlanmap)
critical_area=vlanmap[0].split(',')
unknown_area=vlanmap[1].split(',')
trusted_area=vlanmap[2].split(',')
print(critical_area)
print(unknown_area)
print(trusted_area)