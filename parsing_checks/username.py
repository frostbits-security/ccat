# Parse username options
# Input:
#       line with user options
#           vasya privilege 15 secret 5 $1$0k5Q$3h/ZPjj8T0iHu9DL/Ejt30
# Output:
#       user's options dictionary
#           {'vasya': {'password_type': '5', 'privilege': '15'}}
from pyparsing import Word,Suppress,printables,restOfLine,nums,MatchFirst,Optional


def _globalParse___username_attributes(line):
    username_dict = {}

    username       = (Word(printables))                                         ('user')
    privilege      = (Suppress('privilege') + Word(nums))                       ('priv_num')
    password_type  = (Suppress(MatchFirst(['secret', 'password'])) + Word(nums))('pass_type')

    parse_username = username + Optional(privilege) + password_type + Suppress(restOfLine)

    result = parse_username.parseString(line)

    username_dict[result.user] = {}
    username_dict[result.user]['password_type'] = result.pass_type.asList()[0]

    try:
        username_dict[result.user]['privilege'] = result.priv_num.asList()[0]
    except AttributeError:
        pass

    return username_dict
