# command line arguments parsing
# input: full path of the directory with config[s]+ filename of vlanmap
# vlanmap structure can be seen in example folder (vlmap.txt)
import argparse
import os

def arg_parser(config_folder,vlanmap_name):
    try:
        config_lst = [config_folder + '/' + i for i in os.listdir(config_folder)]
        vlanmap = config_folder + '/' + vlanmap_name
        res=[]
        res.append(vlanmap)
        try:
            config_lst.remove(vlanmap)
            for each in config_lst:
                with open(each, 'r') as f:
                    res.append(each)
                    pass
        except ValueError:
            print('Incorrect vlanmap name!')
            exit()
    except OSError:
        print('The directory doesn`t exist!')
        exit()
    return res

# module main, returns list of filepaths list[0] is vlanmap, others are configs
def getargs():
    parser = argparse.ArgumentParser()
    parser.add_argument("-vl",type=str, help="file name of vlanmap")
    parser.add_argument("-c",type=str, help="full path of the folder with config[s] and vlanmap")
    args = parser.parse_args()
    if args.vl and args.c:
        return arg_parser(args.c,args.vl)
    else:
        print("You must load directory with config[s] and vlanmap! \n\nEXAMPLE: ccat -c example -vl vlmap.txt")
        arg_parser('example','vlmap.txt')
        exit()