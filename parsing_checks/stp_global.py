# STP option parsing
# Input:
#        string, which start with word 'spanning-tree'
#        dictionary for settings
# Output:
#        dictionary with settings

import util
from pyparsing import Suppress,restOfLine,ParseException

def _globalParse___stp_attributes(stp, dct):
    parse_portfast = Suppress('portfast ') + restOfLine
    parse_bpdu = Suppress('portfast bpduguard ') + restOfLine
    parse_loop = Suppress('loopguard ') + restOfLine
    try:
        return util.int_dict_parse(parse_bpdu, stp, 'bpduguard', dct)
    except ParseException:
        pass
    try:
        return util.int_dict_parse(parse_loop, stp, 'loopguard', dct)
    except ParseException:
        pass
    try:
        return util.int_dict_parse(parse_portfast, stp, 'portfast', dct)
    except ParseException:
        pass
    return 0