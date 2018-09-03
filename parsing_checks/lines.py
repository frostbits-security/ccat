# Parse console and vty line options
# Input:
#       line with console or vty line name
#           vty 0 4
# Output:
#       console or line options dictionary, next line (otherwise program will skip next line due to cursor placement)
#           {'log_syng': 'no', 'access-class': {'name': 'ssh-in', 'type': 'in'}, 'privilege': '15'}, 'line vty 5 15'
import util
from pyparsing import Word,alphas,MatchFirst,restOfLine,Suppress,Optional,ParseException


def _globalParse___line_attributes(config):
    line_list, next_line = util.get_attributes(config)
    line_dict = {'log_syng': 'no', 'no_exec': 'no', 'access-class': {}}

    parse_login_type   = Suppress('login ' + Optional('authentication ')) + restOfLine
    parse_exec_timeout = Suppress('exec-timeout ')                        + restOfLine
    parse_pass_type    = Suppress('password ')                            + restOfLine
    parse_privilege    = Suppress('privilege level ')                     + restOfLine
    parse_transp_in    = Suppress('transport input ')                     + restOfLine
    parse_transp_out   = Suppress('transport output ')                    + restOfLine
    parse_rotary       = Suppress('rotary ')                              + restOfLine
    parse_access_class = Suppress('access-class') + Word(alphas + '-') + MatchFirst(['in', 'out']) + Suppress(Optional(restOfLine))

    for option in line_list:
        if option == 'logging synchronous':
            line_dict['log_syng'] = 'yes'
            continue
        if option == 'no exec':
            line_dict['no_exec'] = 'yes'
            continue
        try:
            item = parse_exec_timeout.parseString(option).asList()[-1]
            item = item.split()
            if len(item) == 2:
                line_dict['exec_timeout'] = int(item[0]) + int(item[1]) / 60
            else:
                line_dict['exec_timeout'] = int(item[0])
            continue
        except ParseException:
            pass
        try:
            line_dict['login_type'] = parse_login_type.parseString(option).asList()[-1]
            continue
        except ParseException:
            pass
        try:
            line_dict['pass_type']  = parse_pass_type .parseString(option).asList()[-1]
            continue
        except ParseException:
            pass
        try:
            line_dict['privilege']  = parse_privilege .parseString(option).asList()[-1]
            continue
        except ParseException:
            pass
        try:
            line_dict['transp_in']  = parse_transp_in .parseString(option).asList()[-1]
            continue
        except ParseException:
            pass
        try:
            line_dict['transp_out'] = parse_transp_out.parseString(option).asList()[-1]
            continue
        except ParseException:
            pass
        try:
            line_dict['rotary']     = parse_rotary    .parseString(option).asList()[-1]
            continue
        except ParseException:
            pass
        try:
            item = parse_access_class.parseString(option).asList()
            line_dict['access-class']['name'] = item[0]
            line_dict['access-class']['type'] = item[-1]
            continue
        except ParseException:
            pass

    return line_dict, next_line
