#!/usr/bin/env python3
# input: full path of the directory with config[s]+ file name of vlanmap
import argparse
import os
import re

def arg_parser(config_folder,vlanmap_name):
    try:
        config_lst = [config_folder + '/' + i for i in os.listdir(config_folder)]
        vlanmap = config_folder + '/' + vlanmap_name
        try:
            config_lst.remove(vlanmap)
            for each in config_lst:
                with open(each, 'r') as f:
                    pass
        except ValueError:
            print('Incorrect vlanmap name!')
    except OSError:
        print('The directory doesn`t exist!')

parser = argparse.ArgumentParser()
parser.add_argument("-vl",type=str, help="file name of vlanmap")
parser.add_argument("-c",type=str, help="full path of the folder with config[s] and vlanmap")
args = parser.parse_args()
if args.vl and args.c:
    arg_parser(args.c,args.vl)
else:
    print("You must load directory with config[s] and vlanmap! IT`S EXAMPLE:\n\npython arg.py -c example -vl vlmap.txt")
    arg_parser('example','vlmap.txt')

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