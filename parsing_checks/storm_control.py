# Storm-control option parsing
# Input:
#        string, which start with word 'storm-control'
#        dictionary for storm-control settings
# Output:
#        dictionary with storm-control settings

import util
from pyparsing import Word,Suppress,alphas,restOfLine,Optional,ParseException

def __ifaceAttributes___storm_check(storm,dct):

    parse_level  = Word(alphas)        + Suppress('level ')            + restOfLine
    parse_action = Suppress('action ') + Word(alphas)
    parse_type   = Word(alphas)        + Suppress(Optional("include")) + Word(alphas)
    try:
        value = parse_level.parseString(storm).asList()
        if 'level' in dct:
            dct['level'].append(value)
        else:
            dct['level'] = [value]
        return dct
    except ParseException:
        pass
    try:
        return util.int_dict_parse(parse_action, storm, 'action', dct)
    except ParseException:
        pass
    try:
        return util.int_dict_parse(parse_type,   storm, 'type',   dct)
    except ParseException:
        pass