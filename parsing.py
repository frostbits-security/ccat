# Cisco config parsing
# Creating 2 dictionaries with global and local options.
#
# Global dictionary
# {'file1.txt': {'active_service': [...], 'disable_service': [...], 'username': {...}, 'aaa': [...], 'ip_dhcp': [...],
#                'ip_ssh': {...}, 'line': {...}}
#  'file2.txt': {...}}
#
# Interface dictionary
# {'file1.txt': {'vlans': [1,2,3], 'shutdown': 'yes'/'no', 'description': '...', 'type': 'access'/'trunk',
#                'storm-control': {'level': {'type', 'range'}, 'action': '...'}}
#  'file2.txt': {...}}
#
#
# FOR DEBUG
import sys
sys.path.append(r"C:\\Program Files (x86)\\Python36-32\\Lib\\site-packages")

from pyparsing import Suppress, Optional, restOfLine, ParseException, MatchFirst, Word, nums, ZeroOrMore, NotAny, White,\
                      Or, printables, oneOf, alphas
import re
import util


# Parse any attributes with whitespace as first symbol into list

def get_attributes (config):
    options_list = []
    option = White(exact = 1) + Suppress(Optional(White())) + restOfLine
    next_line = config.readline()
    option_parse = option.parseString(next_line)
    try:
        while option_parse[0] == ' ':
            options_list.append(option_parse[-1])
            next_line = config.readline()
            option_parse = option.parseString(next_line)
    except:
        pass

    return options_list, next_line


# Username options parsing

def _globalParse___username_attributes (line):
    username_dict = {}
    username       = (Word(printables))                             ('user')
    privilege      = (Optional(Suppress('privilege') + Word(nums))) ('priv_num')
    password_type  = (Suppress('secret')             + Word(nums))  ('pass_type')
    parse_username = (username + privilege + password_type + Suppress(restOfLine))
    res = parse_username.parseString(line)

    username_dict[res.user] = {}
    username_dict[res.user]['password_type'] = res.pass_type.asList()[0]
    try:
        username_dict[res.user]['privilege'] = res.priv_num.asList()[0]
    except AttributeError:
        pass

    return username_dict


def _globalParse___aaa_attributes(line):
    aaa_dict = {}
    authentication = Suppress('authentication ') + restOfLine
    authorization = Suppress('authorization ') + restOfLine
    accounting = Suppress('accounting ') + restOfLine

    try:
        aaa_dict['authentication'] = authentication.parseString(line).asList()[-1]
    except ParseException:
        pass
    try:
        aaa_dict['authorization'] = authorization.parseString(line).asList()[-1]
    except ParseException:
        pass
    try:
        aaa_dict['accounting'] = accounting.parseString(line).asList()[-1]
    except ParseException:
        pass

    return aaa_dict



# Ssh options parsing

def _globalParse___ssh_attributes(line):
    ssh_dict = {}
    option = (Word(alphas + '-'))('opt')
    value  = (restOfLine)        ('val')
    res    = (option + White() + value).parseString(line)

    if res.opt == 'logging':
        ssh_dict['logging-events'] = 'yes'
    elif res.opt == 'port':
        ssh_dict['port'] = res.val.split()[0]
    else:
        ssh_dict[res.opt] = res.val

    return ssh_dict


# Console and vty line options parsing

def _globalParse___line_attributes(config):
    line_list, next_line = get_attributes(config)
    line_dict = {'log_syng': 'no', 'access-class': {}}

    parse_exec_timeout = Suppress('exec-timeout ')     + restOfLine
    parse_pass_type    = Suppress('password ')         + restOfLine
    parse_privilege    = Suppress('privilege level ')  + restOfLine
    parse_transp_in    = Suppress('transport input ')  + restOfLine
    parse_transp_out   = Suppress('transport output ') + restOfLine
    parse_rotary       = Suppress('rotary ')           + restOfLine
    parse_access_class = Suppress('access-class')      + Word(alphas + '-') + MatchFirst(['in', 'out']) +\
                         Suppress(Optional(restOfLine))

    for option in line_list:
        if option == 'logging synchronous':
            line_dict['log_syng'] = 'yes'
            continue
        try:
            item = parse_exec_timeout.parseString(option).asList()[-1]
            item = item.split()
            if len(item) == 2:
                line_dict['exec_timeout'] = int(item[0]) + int(item[1])/60
            else:
                line_dict['exec_timeout'] = int(item[0])
            continue
        except ParseException:
            pass
        try:
            line_dict['pass_type'] = parse_pass_type.parseString(option).asList()[-1]
            continue
        except ParseException:
            pass
        try:
            line_dict['privilege'] = parse_privilege.parseString(option).asList()[-1]
            continue
        except ParseException:
            pass
        try:
            line_dict['transp_in'] = parse_transp_in.parseString(option).asList()[-1]
            continue
        except ParseException:
            pass
        try:
            line_dict['transp_out'] = parse_transp_out.parseString(option).asList()[-1]
            continue
        except ParseException:
            pass
        try:
            line_dict['rotary'] = parse_rotary.parseString(option).asList()[-1]
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


# Global options parsing

def global_parse(filenames):
    iface_global = {}

    parse_active_service  =                   Suppress('service ')    + restOfLine
    parse_disable_service =                   Suppress('no service ') + restOfLine
    parse_username        =                   Suppress('username ')   + restOfLine
    parse_aaa             =                   Suppress('aaa ')        + restOfLine
    parse_ip_dhcp         = NotAny(White()) + Suppress('ip dhcp ')    + restOfLine
    parse_ip_ssh          =                   Suppress('ip ssh ')     + restOfLine
    parse_line            =                   Suppress('line ')       + restOfLine

    for fname in filenames:
        with open(fname) as config:
            iface_global.update({fname: {'active_service': [], 'disable_service': [], 'aaa': {}, 'users': {},
                                    'ip_dhcp': [], 'ip_ssh': {}, 'line': {}}})
            for line in config:
                try:
                    iface_global[fname]['active_service'].append(parse_active_service.parseString(line).asList()[-1])
                    continue
                except ParseException:
                    pass
                try:
                    iface_global[fname]['disable_service'].append(parse_disable_service.parseString(line).asList()[-1])
                    continue
                except ParseException:
                    pass
                try:
                    current_line = parse_username.parseString(line).asList()[-1]
                    iface_global[fname]['users'].update(_globalParse___username_attributes(current_line))
                    continue
                except ParseException:
                    pass
                try:
                    current_line = parse_aaa.parseString(line).asList()[-1]
                    iface_global[fname]['aaa'].update(_globalParse___aaa_attributes(current_line))
                    continue
                except ParseException:
                    pass
                try:
                    iface_global[fname]['ip_dhcp'].append(parse_ip_dhcp.parseString(line).asList()[-1])
                    continue
                except ParseException:
                    pass
                try:
                    current_line = parse_ip_ssh.parseString(line).asList()[-1]
                    iface_global[fname]['ip_ssh'].update(_globalParse___ssh_attributes(current_line))
                    continue
                except ParseException:
                    pass
                try:
                    while line != '!':
                        item = parse_line.parseString(line).asList()[-1]
                        iface_global[fname]['line'][item], next_line = _globalParse___line_attributes(config)
                        line = next_line
                    continue
                except ParseException:
                    pass
    return iface_global


# Interface attributes parsing

def _interfaceParse___iface_attributes (config):
    iface_list = get_attributes(config)[0]

    iface_dict = {'vlans':[], 'shutdown': 'no'}

    storm_dict = {}

    port_sec_dct = {}

    vlan_num = Word(nums + '-') + ZeroOrMore(Suppress(',') + Word(nums + '-'))
	
    parse_description = Suppress('description ')     + restOfLine
    parse_type        = Suppress('switchport mode ') + restOfLine
    parse_vlans       = Suppress('switchport ')      + Suppress(MatchFirst('access vlan ' +
                                                       ('trunk allowed vlan ' + Optional('add ')))) + vlan_num
    parse_storm=Suppress('storm-control ') + restOfLine
    parse_port_sec = Suppress('switchport port-security ') + restOfLine

    for option in iface_list:
        if option == 'shutdown':
            iface_dict['shutdown'] = 'yes'
            continue
        try:
            iface_dict['description'] = parse_description.parseString(option).asList()[-1]
            continue
        except ParseException:
            pass
        try:
            iface_dict['type'] = parse_type.parseString(option).asList()[-1]
            continue
        except ParseException:
            pass
        try:
            vlan_add = parse_vlans.parseString(option).asList()
            for unit in vlan_add:
                if '-' in unit:
                    range_units = unit.split('-')
                    range_list = [i for i in range(int(range_units[0]), int(range_units[1]) + 1)]
                    vlan_add.remove(unit)
                    iface_dict['vlans'].extend(range_list)
                else:
                    iface_dict['vlans'].append(int(unit))
            continue
        except ParseException:
            pass
        try:
            storm_control=parse_storm.parseString(option).asList()[-1]
            iface_dict['storm control']=__ifaceAttributes___storm_check(storm_control,storm_dict)
            continue
        except ParseException:
            pass
        if option == 'switchport nonegotiate':
            iface_dict['dtp'] = 'no'
        if option == 'no cdp enable':
            iface_dict['cdp'] = 'no'
        try:
            port_sec=parse_port_sec.parseString(option).asList()[-1]
            iface_dict['port-security'] = __ifaceAttributes___port_sec_parse(port_sec, port_sec_dct)
        except ParseException:
            pass
    return iface_dict


#Storm-control option parsing

def __ifaceAttributes___storm_check(storm,dct):

    parse_level  = Word(alphas) + Suppress('level ') + restOfLine
    parse_action = Suppress('action ') + Word(alphas)
    parse_type   = Word(alphas) + Suppress(Optional("include")) + Word(alphas)
    try:
        return util.int_dict_parse(parse_level, storm, 'level', dct)
    except ParseException:
        pass
    try:
        return util.int_dict_parse(parse_action, storm, 'action', dct)
    except ParseException:
        pass
    try:
        return util.int_dict_parse(parse_type, storm, 'type', dct)
    except ParseException:
        pass




#Port-security option parsing

def __ifaceAttributes___port_sec_parse(port,dct):
    parse_aging=Suppress('aging type ')+restOfLine
    parse_violat=Suppress('violation ')+restOfLine
    parse_mac=Suppress('mac-address ')+Optional('sticky')+restOfLine
    parse_max=Suppress('maximum ')
    try:
        return util.int_dict_parse(parse_aging, port, 'aging', dct)
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


# Interface options parsing

def interface_parse(filenames):
    iface_local = {}

    parse_iface = Suppress('interface ') + restOfLine

    for fname in filenames:
        iface_local.update({fname: {}})
        with open(fname) as config:
            for line in config:
                try:
                    item = parse_iface.parseString(line).asList()[-1]
                    iface_local[fname][item] = _interfaceParse___iface_attributes(config)
                except ParseException:
                    pass
    return iface_local


# OUTPUT FOR DEBUG

# filenames = ['example/10.164.132.1.conf', 'example/172.17.135.196.conf']
# global_parse(filenames)
# interface_parse(filenames)
#
# interfaces=interface_parse(filenames)
# global_params=global_parse(filenames)
#
# for fname in filenames:
#     print('\n', fname, 'global options:\n')
#     for key in global_params[fname]:
#         print(key, global_params[fname][key])
#
#     print('\n', fname, 'interface options:\n')
#     for key in interfaces[fname]:
#         print(key, interfaces[fname][key])

# vlanmap parsing, returns list of three lists with ints
# returns 0 if no vlanmap given
def vlanmap_parse(filename):
    if(filename):
        vmapf=open(filename,"r")
        vlanmap=vmapf.read()
        vmapf.close()
        vlanpattern=re.compile(': ([0-9,]+)')
        vlanmap=re.findall(vlanpattern,vlanmap)
        res=[]
        try:
            res.append(util.intify(vlanmap[0].split(','))) #critical
            res.append(util.intify(vlanmap[1].split(','))) #unknown 
            res.append(util.intify(vlanmap[2].split(','))) #trusted
        except:
            print("Error in vlanmap syntax")
            exit()
        return res
    else:
        return 0
    exit()