# Dhcp snooping/Arp inspection option parsing
# Input:
#        string, which start with word 'ip dhcp snooping'/ 'ip arp inspection'
#        dictionary for settings
# Output:
#        dictionary with settings

import util
from pyparsing import Word,Suppress,alphas,restOfLine,ParseException

def __ifaceAttributes___ip_parse(value, dct):
    parse_mode = Word(alphas)
    parse_rate = Suppress('limit rate ') + restOfLine
    try:
        return util.int_dict_parse(parse_rate, value, 'limit', dct)
    except ParseException:
        pass
    try:
        return util.int_dict_parse(parse_mode, value, 'mode', dct)
    except ParseException:
        pass