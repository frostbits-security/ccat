# Parse AAA options
# Input:
#       line with AAA options, type of AAA, login count
#           login default group radius local, authentication, 1
# Output:
#       AAA option dictionary
#           {'login1': {'list': 'default', 'methods': ['radius', 'local']}}
from pyparsing import Word,Suppress,printables,restOfLine,OneOrMore,MatchFirst,Optional


def _globalParse___aaa_attributes(line, type, count_aaa):
    aaa_dict = {}

    parse_authentication_options = Suppress('login') + Word(printables) + OneOrMore(Optional(Suppress('group')) + Word(printables))
    parse_authorization_options  = MatchFirst(['exec', 'login']) + Word(printables) + OneOrMore(Optional(Suppress('group')) + Word(printables))
    parse_accounting_options     = MatchFirst(['exec', 'network']) + Word(printables) +\
                                   MatchFirst(['start-stop', 'stop-only', 'stop']) + OneOrMore(Optional(Suppress('group')) + Word(printables))

    if   type == 'authentication':
        result = parse_authentication_options.parseString(line)
        aaa_dict.update({'login' + str(count_aaa): {}})
        aaa_dict['login' + str(count_aaa)]['list']    = result.pop(0)
        aaa_dict['login' + str(count_aaa)]['methods'] = result.asList()
    elif type == 'authorization':
        result = parse_authorization_options.parseString(line)
        aaa_dict.update({'login' + str(count_aaa): {}})
        aaa_dict['login' + str(count_aaa)]['login']   = result.pop(0)
        aaa_dict['login' + str(count_aaa)]['list']    = result.pop(0)
        aaa_dict['login' + str(count_aaa)]['methods'] = result.asList()
    elif type == 'accounting':
        result = parse_accounting_options.parseString(line)
        aaa_dict.update({'login' + str(count_aaa): {}})
        aaa_dict['login' + str(count_aaa)]['login']   = result.pop(0)
        aaa_dict['login' + str(count_aaa)]['list']    = result.pop(0)
        aaa_dict['login' + str(count_aaa)]['record']  = result.pop(0)
        aaa_dict['login' + str(count_aaa)]['methods'] = result.asList()

    return aaa_dict
