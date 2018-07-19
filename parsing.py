# Разные варианты парсинга конфига на примере параметров SERVICE и NO SERVICE
#
#
# Парсинг строки service и no service одной операцией
#
#
# import sys
# sys.path.append(r"C:\\Program Files (x86)\\Python36-32\\Lib\\site-packages")
#
# from pyparsing import *
# service_type = Optional('no') + 'service '
# service_name = restOfLine
# parse_service = (service_type + service_name)
#
# service_dict ={'service ': [], 'no': []}
#
# filenames = ['file1.txt']
# for fname in filenames:
#     with open(fname) as config:
#         for line in config:
#             try:
#                 dict_key = service_type.parseString(line).asList()[0]
#                 service_dict[dict_key].append(parse_service.parseString(line).asList()[-1])
#             except ParseException:
#                 pass
# print(service_dict)
#
#
# Создается словарь со службами вида: {'service ':[активные службы], 'no':[выключенные службы]}


# Парсинг строк service происходит отдельно для включенных и выключенных служб
#

from pyparsing import *
active_service = Suppress('service ')
disable_service = Suppress('no service ')
service_name = restOfLine

parse_active_service = (active_service + service_name)
parse_disable_service = (disable_service + service_name)

service_dict ={'active_service': [], 'disable_service': []}

filenames = ['example\\10.164.132.1.conf']
for fname in filenames:
    with open(fname) as config:
        for line in config:
            try:
                service_dict['active_service'].append(parse_active_service.parseString(line).asList()[-1])
            except ParseException:
                pass
            try:
                    service_dict['disable_service'].append(parse_disable_service.parseString(line).asList()[-1])
            except ParseException:
                pass
print(service_dict)


# Создается словарь вида {'active_service':[активные службы], 'disable_service':[выкл службы]}