# Cisco config parsing
# Creating 2 dictionaries with global and local options.
#
# Global dictionary
# {'file1.txt': {'ip_dhcp_snoop': {...}, 'ip_arp_inspection': {...}, 'active_service': [...], 'disable_service': [...],
#                'aaa': {...}, 'users': {...}, 'ip_ssh': {...}, 'line': {...}, 'version': '...'}
#  'file2.txt': {...}}
#
# Interface dictionary
# {'file1.txt': {'vlans': [...], 'shutdown': 'yes'/'no', 'type': 'access'/'trunk', 'port-security': {'mac-address': ['type','mac'},
#                'description': '...', 'storm-control': {'level': {'type', 'range'}, 'action': '...'}, 'cdp': 'yes/no'}
#  'file2.txt': {...}}
#
#
# FOR DEBUG
# import sys
# sys.path.append(r"C:\\Program Files (x86)\\Python36-32\\Lib\\site-packages")

from pyparsing import Suppress, Optional, restOfLine, ParseException, MatchFirst, Word, nums, ZeroOrMore, NotAny, White,\
                      Or, printables, oneOf, alphas, OneOrMore
import re
import util


# Parse any attributes with whitespace as first symbol into list
# INPUT:  line with futher options (starts with whitespaces)
# SAMPLE: interface Loopback1
# OUTPUT: futher options list, next line (otherwise program may skip next line due to cursor placement)
# SAMPLE: ['description -= MGMT - core.nnn048.nnn =-', 'ip address 172.21.24.140 255.255.255.255'], '!'
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
# INPUT:  line with user options
# SAMPLE: vasya privilege 15 secret 5 $1$0P5Q$9h/ZPJj8T0iHu9DL/Ejt30
# OUTPUT: user's options dictionary
# SAMPLE: {'vasya': {'password_type': '5', 'privilege': '15'}}
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


# AAA options parsing
# INPUT:  line with AAA options, type of AAA, login count
# SAMPLE: login default group radius local, authentication, 1
# OUTPUT: AAA option dictionary
# SAMPLE: {'login1': {'list': 'default', 'methods': ['radius', 'local']}}
def _globalParse___aaa_attributes(line, type, count_aaa):
    aaa_dict = {}

    authentication_options = Suppress('login')               + Word(printables) + OneOrMore(Optional(Suppress('group'))
                                                                                            + Word(printables))
    authorization_options  = MatchFirst(['exec', 'login'])   + Word(printables) + OneOrMore(Optional(Suppress('group'))
                                                                                            + Word(printables))
    accounting_options     = MatchFirst(['exec', 'network']) + Word(printables) +\
                             MatchFirst(['start-stop','stop-only','stop']) + OneOrMore(Optional(Suppress('group')) +
                             Word(printables))

    if type == 'authentication':
        timelist = authentication_options.parseString(line)
        aaa_dict.update({'login'+str(count_aaa): {}})
        aaa_dict['login'+str(count_aaa)]['list']    = timelist.pop(0)
        aaa_dict['login'+str(count_aaa)]['methods'] = timelist.asList()
    elif type == 'authorization':
        timelist = authorization_options.parseString(line)
        aaa_dict.update({'login'+str(count_aaa): {}})
        aaa_dict['login'+str(count_aaa)]['login']   = timelist.pop(0)
        aaa_dict['login'+str(count_aaa)]['list']    = timelist.pop(0)
        aaa_dict['login'+str(count_aaa)]['methods'] = timelist.asList()
    elif type == 'accounting':
        timelist = accounting_options.parseString(line)
        aaa_dict.update({'login'+str(count_aaa): {}})
        aaa_dict['login'+str(count_aaa)]['login']   = timelist.pop(0)
        aaa_dict['login'+str(count_aaa)]['list']    = timelist.pop(0)
        aaa_dict['login'+str(count_aaa)]['record']  = timelist.pop(0)
        aaa_dict['login'+str(count_aaa)]['methods'] = timelist.asList()
    return aaa_dict


# Ssh options parsing
# INPUT:  line with ssh option
# SAMPLE: ip ssh time-out 30
# OUTPUT: ssh option dictionary
# SAMPLE: {'time-out': '30'}
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
# INPUT:  line with console or vty line name
# SAMPLE: vty 0 4
# OUTPUT: console or line options dictionary, next line (otherwise program will skip next line due to cursor placement)
# SAMPLE: {'log_syng': 'no', 'access-class': {'name': 'ssh-in', 'type': 'in'}, 'privilege': '15'}, 'line vty 5 15'
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

# STP option parsing
# Input:
#        string, which start with word 'spanning-tree'
#        dictionary for settings
# Output:
#        dictionary with settings
#

def _globalParse___stp_attributes(stp,dct):
    # print(stp,dct)
    parse_portfast=Suppress('portfast ')+restOfLine
    parse_bpdu=Suppress('portfast bpduguard')+restOfLine
    parse_loop=Suppress('loopguard')+restOfLine
    try:
        return util.int_dict_parse(parse_bpdu, stp, 'bpdu', dct)
    except ParseException:
        pass
    try:
        return util.int_dict_parse(parse_loop, stp, 'loopguard', dct)
    except ParseException:
        pass
    try:
        return util.int_dict_parse(parse_portfast, stp, 'portfast', dct)
    except ParseException:
        pass
    return 0

# Global options parsing
# INPUT:  files list to parse
# SAMPLE: ['example/10.164.132.1.conf','example/172.17.135.196.conf']
# OUTPUT: global options dictionary
# SAMPLE: see on top of this file

def global_parse(filenames):
    iface_global = {}

    parse_version = Suppress('boot system flash bootflash:') + restOfLine
    parse_active_service  =                   Suppress('service ')    + restOfLine
    parse_disable_service =                   Suppress('no service ') + restOfLine
    parse_username        =                   Suppress('username ')   + restOfLine
    parse_ip_ssh          =                   Suppress('ip ssh ')     + restOfLine
    parse_line            =                   Suppress('line ')       + restOfLine
    parse_aaa             =                   Suppress('aaa')         + restOfLine
    parse_ip_dhcp         = NotAny(White()) + Suppress('ip dhcp snooping') + Optional(Suppress('vlan') + Word(nums) +
                                                                                ZeroOrMore(Suppress(',') + Word(nums)))
    parse_ip_arp          = NotAny(White()) + Suppress('ip arp inspection') + Suppress('vlan')         + Word(nums) +\
                                                                                ZeroOrMore(Suppress(',') + Word(nums))
    parse_stp = Suppress('spanning-tree ') + restOfLine

    authentication = Suppress('authentication ') + restOfLine
    authorization  = Suppress('authorization ')  + restOfLine
    accounting     = Suppress('accounting ')     + restOfLine

    for fname in filenames:
        with open(fname) as config:
            count_authen, count_author, count_acc = 1, 1, 1
            iface_global.update({fname: {'ip_dhcp_snoop':{'active':'no'},'ip_arp_inspection':{'active':'no'},
                                         'active_service': [], 'disable_service': [], 'aaa': {}, 'users': {},
                                         'ip_ssh': {}, 'line': {},'stp':{}}})
            
            #debug
            #print(fname)
            try:
                for line in config:
                    try:
                        iface_global[fname]['version'] = parse_version.parseString(line).asList()[0]
                        continue
                    except ParseException:
                        pass
                    try:
                        current_line = parse_ip_dhcp.parseString(line).asList()
                        iface_global[fname]['ip_dhcp_snoop']['active'] = 'yes'
                        if current_line:
                            iface_global[fname]['ip_dhcp_snoop']['vlans']  = current_line
                        continue
                    except ParseException:
                        pass
                    try:
                        current_line = parse_ip_arp.parseString(line).asList()
                        iface_global[fname]['ip_arp_inspection']['active'] = 'yes'
                        if current_line:
                            iface_global[fname]['ip_arp_inspection']['vlans']  = current_line
                        continue
                    except ParseException:
                        pass
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
                        stp_str = parse_stp.parseString(line).asList()[-1]
                        stp_line=_globalParse___stp_attributes(stp_str, iface_global[fname]['stp'])
                        if stp_line!=0:
                            iface_global[fname]['users'].update(stp_line)
                        continue
                    except ParseException:
                        pass
                    try:
                        current_line = parse_aaa.parseString(line).asList()[-1]
                        try:
                            current_line = authentication.parseString(current_line).asList()[-1]
                            iface_global[fname]['aaa'].setdefault('authentication',{})
                            iface_global[fname]['aaa']['authentication'].update(_globalParse___aaa_attributes(current_line,'authentication',count_authen))
                            count_authen += 1
                            continue
                        except ParseException:
                            pass
                        try:
                            current_line = authorization.parseString(current_line).asList()[-1]
                            iface_global[fname]['aaa'].setdefault('authorization',{})
                            iface_global[fname]['aaa']['authorization'].update(_globalParse___aaa_attributes(current_line,'authorization',count_author))
                            count_author += 1
                            continue
                        except ParseException:
                            pass
                        try:
                            current_line = accounting.parseString(current_line).asList()[-1]
                            iface_global[fname]['aaa'].setdefault('accounting',{})
                            iface_global[fname]['aaa']['accounting'].update(_globalParse___aaa_attributes(current_line,'accounting',count_acc))
                            count_acc += 1
                            continue
                        except ParseException:
                            pass
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
            except:
                print('Error processing file: '+fname)
                pass
    return iface_global


# Interface attributes parsing
# INPUT:  open file with cursor on interface line
# SAMPLE: example/10.164.132.1.conf
# OUTPUT: interface options dictionary
# SAMPLE: {'vlans': [], 'shutdown': 'no', 'description': '-= MGMT - core.nnn048.nnn =-'}

def _interfaceParse___iface_attributes (config):
    iface_list = get_attributes(config)[0]

    iface_dict = {'vlans':[], 'shutdown': 'no', 'dhcp_snoop': {'mode':'untrust'},'arp_insp':{'mode':'untrust'},'storm control': {}, 'port-security': {}}


    vlan_num = Word(nums + '-') + ZeroOrMore(Suppress(',') + Word(nums + '-'))
	
    parse_description = Suppress('description ')              + restOfLine
    parse_type        = Suppress('switchport mode ')          + restOfLine
    parse_storm       = Suppress('storm-control ')            + restOfLine
    parse_port_sec    = Suppress('switchport port-security ') + restOfLine
    parse_dhcp_snoop=Suppress('ip dhcp snooping ')+restOfLine
    parse_arp_insp=Suppress('ip arp inspection ')+restOfLine
    parse_vlans       = Suppress('switchport ')               + Suppress(MatchFirst('access vlan ' +
                                                       ('trunk allowed vlan ' + Optional('add ')))) + vlan_num

    for option in iface_list:
        if option == 'shutdown':
            iface_dict['shutdown'] = 'yes'
            continue
        # if option == 'ip dhcp snooping trust':
        #     iface_dict['dhcp_snoop'] = 'trust'
        #     continue
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
            iface_dict['storm control']=__ifaceAttributes___storm_check(storm_control,iface_dict['storm control'])
            continue
        except ParseException:
            pass
        if option == 'switchport nonegotiate':
            iface_dict['dtp'] = 'no'
            continue
        if option == 'no cdp enable':
            iface_dict['cdp'] = 'no'
            continue
        try:
            port_sec=parse_port_sec.parseString(option).asList()[-1]
            iface_dict['port-security'] = __ifaceAttributes___port_sec_parse(port_sec, iface_dict['port-security'])
            continue
        except ParseException:
            pass
        try:
            dhcp_snoop=parse_dhcp_snoop.parseString(option).asList()[-1]
            iface_dict['dhcp_snoop'] = __ifaceAttributes___ip_parse(dhcp_snoop, iface_dict['dhcp_snoop'])
            continue
        except ParseException:
            pass
        try:
            arp_insp=parse_arp_insp.parseString(option).asList()[-1]
            iface_dict['dhcp_snoop'] = __ifaceAttributes___ip_parse(arp_insp, iface_dict['arp_insp'])
            continue
        except ParseException:
            pass
    return iface_dict

# Dhcp snooping/Arp inspection option parsing
# Input:
#        string, which start with word 'ip dhcp snooping'/ 'ip arp inspection'
#        dictionary for settings
# Output:
#        dictionary with settings
#

def __ifaceAttributes___ip_parse(dhcp_snoop, dct):
    parse_mode=Word(alphas)
    parse_rate=Suppress('limit rate ')+restOfLine
    try:
        return util.int_dict_parse(parse_rate, dhcp_snoop, 'limit', dct)
    except ParseException:
        pass
    try:
        return util.int_dict_parse(parse_mode, dhcp_snoop, 'mode', dct)
    except ParseException:
        pass

# Storm-control option parsing
# Input:
#        string, which start with word 'storm-control'
#        dictionary for storm-control settings
# Output:
#        dictionary with storm-control settings
#

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


# Port-security option parsing
# Input:
#        string, which start with word 'port-security'
#        dictionary for port-security settings
# Output:
#        dictionary with port-security settings
#

def __ifaceAttributes___port_sec_parse(port,dct):
    parse_aging_time = Suppress('aging time ')+restOfLine
    parse_aging_type = Suppress('aging type ') + restOfLine
    parse_violat = Suppress('violation ')+restOfLine
    parse_mac=Suppress('mac-address ')+Optional('sticky')+restOfLine
    parse_max=Suppress('maximum ')+restOfLine
    try:
        return util.int_dict_parse(parse_aging_time, port, 'aging time', dct)
    except ParseException:
        pass
    try:
        return util.int_dict_parse(parse_aging_type, port, 'aging type', dct)
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
# INPUT:  files list to parse
# SAMPLE: ['example/10.164.132.1.conf','example/172.17.135.196.conf']
# OUTPUT: interface options dictionary
# SAMPLE: see on top of this file
def interface_parse(filenames):
    iface_local = {}

    parse_iface = Suppress('interface ') + restOfLine
        # ip ARP INSPECTION LIMIT RATE, trust
    for fname in filenames:
        #debug
        #print(fname)
        iface_local.update({fname: {}})
        with open(fname) as config:
            try:
                for line in config:
                    try:
                        item = parse_iface.parseString(line).asList()[-1]
                        iface_local[fname][item] = _interfaceParse___iface_attributes(config)
                    except ParseException:
                        pass
            except:
                print('Error processing file: '+fname)
                pass
    return iface_local


# OUTPUT FOR DEBUG
# filenames = ['example/10.164.132.1.conf','example/172.17.135.196.conf']
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