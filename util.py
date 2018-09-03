# library with different useful functions to use them within various modules
from pyparsing import White,restOfLine,Suppress,Optional

# converts string list of numbers to list of ints with those numbers
# ['1','2','3'] -> [1,2,3]
def intify(strlist):
    res=[]
    for i in strlist:
        res.append(int(i))
    return res

#Add value to the feature interface_dict

def int_dict_parse(parse_meth,featur_str,name,featur_dict):

    value = parse_meth.parseString(featur_str).asList()
    featur_dict[name] = value
    return featur_dict


# Parse any attributes with whitespace as first symbol into list
# Input:
#       line with futher options (starts with whitespaces)
#           interface Loopback1
# Output:
#       further options list, next line (otherwise program may skip next line due to cursor placement)
#           ['description -= MGMT - core.nnn048.nnn =-', 'ip address 172.21.24.140 255.255.255.255'], '!'
def get_attributes(config):
    options_list = []
    option = White(exact=1) + Suppress(Optional(White())) + restOfLine
    next_line = config.readline()
    try:
        option_parse = option.parseString(next_line)
        while option_parse[0] == ' ':
            options_list.append(option_parse[-1])
            next_line = config.readline()
            option_parse = option.parseString(next_line)
    except:
        pass
    return options_list, next_line
