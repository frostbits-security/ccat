# Cisco config parsing
#
#
#
# FOR DEBUG
# import sys
# sys.path.append(r"C:\\Program Files (x86)\\Python36-32\\Lib\\site-packages")

from pyparsing import Suppress, Optional, restOfLine, ParseException, MatchFirst, Word, nums, ZeroOrMore, NotAny, White,\
                      Or, printables, oneOf, alphas

					  
# Parsing any attributes into list

def get_attributes (config):
    iface_list = []
    x = config.readline()
    while len(x) > 3:
        iface_list.append(x[1:-1])
        x = config.readline()
    return (iface_list)


# Username options parsing

def username_attributes (line):
    username_dict = {}
    username       = (Word(printables))                             ('user')
    privilege      = (Optional(Suppress('privilege') + Word(nums))) ('priv_num')
    password_type  = (Suppress('secret') + Word(nums))              ('pass_type')
    parse_username = (username + privilege + password_type + Suppress(restOfLine))
    res = parse_username.parseString(line)

    username_dict[res.user] = {}
    username_dict[res.user]['password_type'] = res.pass_type.asList()[0]
    try:
        username_dict[res.user]['privilege'] = res.priv_num.asList()[0]
    except AttributeError:
        pass

    return username_dict


# Ssh options parsing

def ssh_attributes(line):
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


# Global options parsing

def global_parse():

    parse_active_service  =                   Suppress('service ')    + restOfLine
    parse_disable_service =                   Suppress('no service ') + restOfLine
    parse_username        =                   Suppress('username ')   + restOfLine
    parse_aaa             =                   Suppress('aaa ')        + restOfLine
    parse_ip_dhcp         = NotAny(White()) + Suppress('ip dhcp ')    + restOfLine
    parse_ip_ssh          =                   Suppress('ip ssh ')     + restOfLine
    parse_line            =                   Suppress('line ')       + restOfLine

    filenames = ['file1.txt', 'file3.txt']
    for fname in filenames:
        with open(fname) as config:
            iface_global = {fname: {'active_service': [], 'disable_service': [], 'aaa': [], 'users': {},
                                    'ip_dhcp': [], 'ip_ssh': {}, 'line': []}}
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
                    iface_global[fname]['users'].update(username_attributes(current_line))
                    continue
                except ParseException:
                    pass
                try:
                    iface_global[fname]['aaa'].append(parse_aaa.parseString(line).asList()[-1])
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
                    iface_global[fname]['ip_ssh'].update(ssh_attributes(current_line))
                    continue
                except ParseException:
                    pass
                try:
                    iface_global[fname]['line'].append(parse_line.parseString(line).asList()[-1])
                    continue
                except ParseException:
                    pass

        print('\n', fname, 'global options:\n')
        for key in iface_global[fname]:
            print(key, iface_global[fname][key])

# Parsing interface attributes into dictionary

def iface_attributes (config):
    iface_list = get_attributes(config)

    iface_dict = {'vlans':[], 'shutdown': 'no'}

    storm_dict = {}

    vlan_num = Word(nums + '-') + ZeroOrMore(Suppress(',') + Word(nums + '-'))
	
    parse_description = Suppress('description ')     + restOfLine
    parse_type        = Suppress('switchport mode ') + restOfLine
    parse_vlans       = Suppress('switchport ')      + Suppress(MatchFirst('access vlan ' +
                        ('trunk allowed vlan ' + Optional('add ')))) + vlan_num
    parse_storm=Suppress('storm-control ') + restOfLine

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
            iface_dict['storm control']=storm_check(storm_control,storm_dict)
            continue
        except ParseException:
            pass
    return iface_dict

#Storm-control option parsing

def storm_check(storm,dct):

    parse_level  = Word(alphas) + Suppress('level ') + restOfLine
    parse_action = Suppress('action ') + Word(alphas)
    parse_type   = Word(alphas) + Suppress(Optional("include")) + Word(alphas)
    try:
        return storm_parse(parse_level, storm, 'level', dct)
    except ParseException:
        pass
    try:
        return storm_parse(parse_action, storm, 'action', dct)
    except ParseException:
        pass
    try:
        return storm_parse(parse_type, storm, 'type', dct)
    except ParseException:
        pass

#Add value to the storm_dict

def storm_parse(parse_meth,storm_str,name,storm_dict):

    value = parse_meth.parseString(storm_str).asList()
    storm_dict[name] = value
    return storm_dict

# Interface options parsing

def interface_parse():

    parse_iface = Suppress('interface ') + restOfLine

    filenames = ['example\\10.164.132.1.conf']
    for fname in filenames:
        iface_local = {fname: {}}
        with open(fname) as config:
            for line in config:
                try:
                    item = parse_iface.parseString(line).asList()[-1]
                    iface_local[fname][item] = iface_attributes(config)
                except ParseException:
                    pass
        print('\n', fname, 'interfaces:\n')
        for key in iface_local[fname]:
            print(key,iface_local[fname][key])

			
global_parse()
interface_parse()


# Creating 2 dictionaries with global and local options.
#
# Global dictionary
# {'file1.txt': {'active_service': [...], 'disable_service': [...], 'username': {...}, 'aaa': [...], 'ip_dhcp': [...],
#                'ip_ssh': {...}, 'line': [...]}
#  'file2.txt': {...}}
#
# Interface dictionary
# {'file1.txt': {'vlans': [1,2,3], 'shutdown': 'yes'/'no', 'description': '...', 'type': 'access'/'trunk',
#                'storm-control': {'level': {'type', 'range'}, 'action': '...'}}
#  'file2.txt': {...}}