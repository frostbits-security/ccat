# Parse AAA options
# Input:
#       line with AAA options, type of AAA, login count
#           login default group radius local, authentication, 1
# Output:
#       AAA option dictionary
#           {'login1': {'list': 'default', 'methods': ['radius', 'local']}}
from pyparsing import Word,Suppress,printables,restOfLine,OneOrMore,MatchFirst,Optional,nums


def _globalParse___aaa_attributes(line, type, count_aaa):
    aaa_dict = {}

    authentication_list    = (Suppress('login')                     + Word(printables))  ('authent_list')
    authentication_groups  = (OneOrMore(Optional(Suppress('group')) + Word(printables))) ('authent_methods')

    parse_authentication   = authentication_list + authentication_groups

    # parse_authorization_options  = MatchFirst(['exec', 'login']) + Word(printables) + OneOrMore(Optional(Suppress('group')) + Word(printables))

    accounting_login   = (MatchFirst(['exec', 'network', 'connection', 'commands'])) ('acc_login')
    accounting_list    = (Optional(Word(nums)) + Word(printables))                   ('acc_list')
    accounting_record  = (MatchFirst(['start-stop', 'stop-only', 'stop']))           ('acc_record')
    accounting_methods = (OneOrMore(Optional(Suppress('group')) + Word(printables))) ('acc_methods')

    parse_accounting   = accounting_login + accounting_list + accounting_record + accounting_methods

    if   type == 'authentication':
        result = parse_authentication.parseString(line)
        aaa_dict.update({'login' + str(count_aaa): {}})
        aaa_dict['login' + str(count_aaa)]['list']    = result.authent_list[0]
        aaa_dict['login' + str(count_aaa)]['methods'] = result.authent_methods.asList()
    # elif type == 'authorization':
    #     result = parse_authorization_options.parseString(line)
    #     aaa_dict.update({'login' + str(count_aaa): {}})
    #     aaa_dict['login' + str(count_aaa)]['login']   = result.pop(0)
    #     aaa_dict['login' + str(count_aaa)]['list']    = result.pop(0)
    #     aaa_dict['login' + str(count_aaa)]['methods'] = result.asList()
    elif type == 'accounting':
        result = parse_accounting.parseString(line)
        aaa_dict.update({'login' + str(count_aaa): {}})
        aaa_dict['login' + str(count_aaa)]['login']   = result.acc_login
        aaa_dict['login' + str(count_aaa)]['list']    = result.acc_list.asList()
        aaa_dict['login' + str(count_aaa)]['record']  = result.acc_record
        aaa_dict['login' + str(count_aaa)]['methods'] = result.acc_methods.asList()

    return aaa_dict
