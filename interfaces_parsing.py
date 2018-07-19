# Парсинг интерфесов из конфига
#
# (без явного указания пути модуль у меня не импортировался, пока оставил так)
#import sys
#sys.path.append(r"C:\\Program Files (x86)\\Python36-32\\Lib\\site-packages")
from pyparsing import *

# Получение атрибутов для каждого интерфейса в виде списка
def get_iface_attributes ():
    iface_list = []
    x = config.readline()
    while len(x) > 3:
        iface_list.append(x[1:-1])
        x = config.readline()
    return (iface_list)

parse_iface = (Suppress('interface ') + restOfLine)

filenames = ['example\\10.164.132.1.conf']
for fname in filenames:
    iface_dict = {fname: {}}
    with open(fname) as config:
        for line in config:
            try:
                item = parse_iface.parseString(line).asList()[-1]
                iface_dict[fname][item] = get_iface_attributes()
            except ParseException:
                pass
    print(fname, 'interfaces:')
    for key in iface_dict[fname]:
        print(key,iface_dict[fname][key])

