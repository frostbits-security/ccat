# Port-security option parsing
# Input:
#        string, which start with word 'port-security'
#        dictionary for port-security settings
# Output:
#        dictionary with port-security settings

import util
from pyparsing import Suppress,restOfLine,Optional,ParseException

def __ifaceAttributes___port_sec_parse(port, dct):
    parse_aging_time = Suppress('aging time ') + restOfLine
    parse_aging_type = Suppress('aging type ') + restOfLine
    parse_violat = Suppress('violation ') + restOfLine
    parse_max = Suppress('maximum ') + restOfLine
    parse_mac = Suppress('mac-address ') + Optional('sticky') + restOfLine
    try:
        return util.int_dict_parse(parse_aging_time, port, 'aging time', dct)
    except ParseException:
        pass
    try:
        return util.int_dict_parse(parse_aging_type, port, 'aging type', dct)
    except ParseException:
        pass
    try:
        return util.int_dict_parse(parse_violat, port, 'violation', dct)
    except ParseException:
        pass
    try:
        return util.int_dict_parse(parse_mac, port, 'mac-address', dct)
    except ParseException:
        pass
    try:
        return util.int_dict_parse(parse_max, port, 'maximum', dct)
    except ParseException:
        pass
