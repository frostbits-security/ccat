# VTP option parsing
# Input:
#        string, which start with word 'vtp'
#        dictionary for vtp settings
# Output:
#        dictionary with vtp settings

import util
from pyparsing import Suppress,restOfLine,Optional,ParseException

def _globalParse___vtp_attributes(vtp, dct):
    parse_domain = Suppress('domain ') + restOfLine
    parse_mode = Suppress('mode ') + restOfLine
    try:
        return util.int_dict_parse(parse_domain, vtp, 'domain', dct)
    except ParseException:
        pass
    try:
        return util.int_dict_parse(parse_mode, vtp, 'mode', dct)
    except ParseException:
        pass
    return 0