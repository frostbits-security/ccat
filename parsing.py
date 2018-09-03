# Cisco config parsing
# Create 2 dictionaries with global and interface options
#
# Global dictionary
# {'ip': {'dhcp_snooping': {...}, 'arp_inspection': {...}, 'ssh': {...}, 'active_service': [...], 'http': {...}},
#                'active_service': [...], 'disable_service': [...], 'aaa': {'authentication': {...},
#                'authorization': {...}, 'accounting': {...}}, 'users': {...}, 'line': {...}, 'stp': {...}, 'ipv6': {...},
#                'vtp':{...} , 'version': '...', 'model': '...', 'enable_password': '...'}
#
# Interface dictionary
# {'Interface_1': {'vlans': [...], 'shutdown': '...', 'type': '...', 'port-security': {...}, 'dhcp_snoop': {...},
#                 'arp_insp': {...}, 'ipv6': {...}, 'storm-control': {...}, 'cdp': '...', 'dtp': {...},
#                 'description': '...'},
# 'Interface_2': {...}}


from pyparsing import Suppress, Optional, restOfLine, ParseException, MatchFirst, Word, nums, ZeroOrMore, NotAny, White, \
    Or, printables, oneOf, alphas, OneOrMore
from json import load
import util
import parsing_checks
from parsing_checks import *

iface_local = {}
parse_iface = Suppress('interface ') + restOfLine

iface_global = {}
parse_enable_password = Suppress('enable') + MatchFirst(['secret', 'password']) + Optional(
    Word(nums) + Suppress(White(exact=1))) + Suppress(restOfLine)
parse_active_service = Suppress('service ') + restOfLine
parse_disable_service = Suppress('no service ') + restOfLine
parse_version = Suppress('version ') + restOfLine
parse_ipv6 = Suppress('ipv6 ') + restOfLine
parse_ipv6_sourceguard = Suppress('source-guard ') + restOfLine
parse_ipv6_snooping = Suppress('snooping ') + restOfLine
parse_ipv6_raguard = Suppress('nd raguard ') + restOfLine
parse_ipv6_destinationguard = Suppress('destination-guard ') + restOfLine
parse_ipv6_dhcpguard = Suppress('dhcp guard ') + restOfLine
parse_lldp = Suppress('lldp ') + restOfLine
parse_model = Suppress('boot system flash bootflash:') + restOfLine
parse_username = Suppress('username ') + restOfLine
parse_aaa = Suppress('aaa ') + restOfLine
parse_stp = Suppress('spanning-tree ') + restOfLine
parse_line = Suppress('line ') + restOfLine
parse_ip_ssh = Suppress('ip ssh ') + restOfLine
parse_vstack = Suppress('no') + 'vstack'
parse_ip_dhcp = NotAny(White()) + Suppress('ip dhcp snooping') + Optional(
    Suppress('vlan') + Word(nums) + ZeroOrMore(Suppress(',') + Word(nums)))
parse_ip_arp = NotAny(White()) + Suppress('ip arp inspection') + Suppress('vlan') + Word(nums) + ZeroOrMore(
    Suppress(',') + Word(nums))
parse_ip_service = NotAny(White()) + Suppress('ip') + MatchFirst(['finger', 'identd', 'source-route', 'bootp server'])
parse_ip_http = NotAny(White()) + Suppress('ip http ') + restOfLine
authentication = Suppress('authentication ') + restOfLine
authorization = Suppress('authorization ') + restOfLine
accounting = Suppress('accounting ') + restOfLine
parse_vtp = Suppress('vtp ') + restOfLine


# Parse any attributes with whitespace as first symbol into list
# Input:  line with futher options (starts with whitespaces)
# Sample:    interface Loopback1
# Output: further options list, next line (otherwise program may skip next line due to cursor placement)
# Sample:    ['description -= MGMT - core.nnn048.nnn =-', 'ip address 172.21.24.140 255.255.255.255'], '!'
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


# Parse username options
# Input:  line with user options
# Sample:    vasya privilege 15 secret 5 $1$0k5Q$3h/ZPjj8T0iHu9DL/Ejt30
# Output: user's options dictionary
# Sample:    {'vasya': {'password_type': '5', 'privilege': '15'}}
def _globalParse___username_attributes(line):
    username_dict = {}
    username = (Word(printables))('user')
    privilege = (Suppress('privilege') + Word(nums))('priv_num')
    password_type = (Suppress(MatchFirst(['secret', 'password'])) + Word(nums))('pass_type')
    parse_username = (username + Optional(privilege) + password_type + Suppress(restOfLine))
    result = parse_username.parseString(line)

    username_dict[result.user] = {}
    username_dict[result.user]['password_type'] = result.pass_type.asList()[0]
    try:
        username_dict[result.user]['privilege'] = result.priv_num.asList()[0]
    except AttributeError:
        pass
    return username_dict


# Parse AAA options
# Input:  line with AAA options, type of AAA, login count
# Sample:    login default group radius local, authentication, 1
# Output: AAA option dictionary
# Sample:    {'login1': {'list': 'default', 'methods': ['radius', 'local']}}
def _globalParse___aaa_attributes(line, type, count_aaa):
    aaa_dict = {}

    parse_authentication_options = Suppress('login') + Word(printables) + OneOrMore(Optional(Suppress('group'))
                                                                                    + Word(printables))
    parse_authorization_options = MatchFirst(['exec', 'login']) + Word(printables) + OneOrMore(
        Optional(Suppress('group'))
        + Word(printables))
    parse_accounting_options = MatchFirst(['exec', 'network']) + Word(printables) + \
                               MatchFirst(['start-stop', 'stop-only', 'stop']) + OneOrMore(Optional(Suppress('group')) +
                                                                                           Word(printables))

    if type == 'authentication':
        result = parse_authentication_options.parseString(line)
        aaa_dict.update({'login' + str(count_aaa): {}})
        aaa_dict['login' + str(count_aaa)]['list'] = result.pop(0)
        aaa_dict['login' + str(count_aaa)]['methods'] = result.asList()
    elif type == 'authorization':
        result = parse_authorization_options.parseString(line)
        aaa_dict.update({'login' + str(count_aaa): {}})
        aaa_dict['login' + str(count_aaa)]['login'] = result.pop(0)
        aaa_dict['login' + str(count_aaa)]['list'] = result.pop(0)
        aaa_dict['login' + str(count_aaa)]['methods'] = result.asList()
    elif type == 'accounting':
        result = parse_accounting_options.parseString(line)
        aaa_dict.update({'login' + str(count_aaa): {}})
        aaa_dict['login' + str(count_aaa)]['login'] = result.pop(0)
        aaa_dict['login' + str(count_aaa)]['list'] = result.pop(0)
        aaa_dict['login' + str(count_aaa)]['record'] = result.pop(0)
        aaa_dict['login' + str(count_aaa)]['methods'] = result.asList()

    return aaa_dict





# Parse SSH options
# Input:  line with ssh option
# Sample:    ip ssh time-out 30
# Output: ssh option dictionary
# Sample:    {'time-out': '30'}
def _globalParse___ssh_attributes(line):
    ssh_dict = {}
    ssh_option = (Word(alphas + '-'))('option')
    ssh_value = (restOfLine)('value')
    result = (ssh_option + White() + ssh_value).parseString(line)

    if result.option == 'logging':
        ssh_dict['logging-events'] = 'yes'
    elif result.option == 'authentication-retries':
        ssh_dict['authentication_retries'] = result.value.split()[0]
    elif result.option == 'port':
        ssh_dict['port_rotary'] = result.value.split()[0]
    elif result.option == 'maxstartups':
        ssh_dict['maxstartups'] = result.value.split()[0]
    elif result.option == 'time-out':
        ssh_dict['time-out'] = result.value.split()[0]
    elif result.option == 'version':
        ssh_dict['version'] = result.value.split()[0]

    return ssh_dict


# Parse HTTP options
# Input:  line with http option
# Sample:    ip http secure-server
# Output: http option dictionary
# Sample:    {'type': 'HTTPS'}
def _globalParse___http_attributes(line):
    http_dict = {}

    if line == 'server':
        http_dict['type'] = 'http'
    elif line == 'secure-server':
        http_dict['type'] = 'https'
    elif line.split()[0] == 'max-connections':
        http_dict['max_connections'] = line.split()[-1]
    elif line.split()[0] == 'port':
        http_dict['port'] = line.split()[-1]

    return http_dict



# Parse console and vty line options
# Input:  line with console or vty line name
# Sample:    vty 0 4
# Output: console or line options dictionary, next line (otherwise program will skip next line due to cursor placement)
# Sample:    {'log_syng': 'no', 'access-class': {'name': 'ssh-in', 'type': 'in'}, 'privilege': '15'}, 'line vty 5 15'
def _globalParse___line_attributes(config):
    line_list, next_line = get_attributes(config)
    line_dict = {'log_syng': 'no', 'no_exec': 'no', 'access-class': {}}

    parse_login_type = Suppress('login ' + Optional('authentication ')) + restOfLine
    parse_exec_timeout = Suppress('exec-timeout ') + restOfLine
    parse_pass_type = Suppress('password ') + restOfLine
    parse_privilege = Suppress('privilege level ') + restOfLine
    parse_transp_in = Suppress('transport input ') + restOfLine
    parse_transp_out = Suppress('transport output ') + restOfLine
    parse_rotary = Suppress('rotary ') + restOfLine
    parse_access_class = Suppress('access-class') + Word(alphas + '-') + MatchFirst(['in', 'out']) + \
                         Suppress(Optional(restOfLine))

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


# Parse global options
# Input:  files list to parse
# Sample:    ['example/10.164.132.1.conf','example/172.17.135.196.conf']
# Output: global options dictionary
# Sample:    see on top of this file
def global_parse(config):
    global iface_global
    global parse_ipv6
    global parse_enable_password
    global parse_active_service
    global parse_disable_service
    global parse_version
    global parse_username
    global parse_aaa
    global parse_stp
    global parse_line
    global parse_ip_ssh
    global parse_ip_dhcp
    global parse_ip_arp
    global parse_ip_service
    global parse_ip_http
    global authentication
    global authorization
    global accounting
    global parse_vtp

    # count_authen, count_author, count_acc = 1, 1, 1
    for line in config:
        if 'no cdp run' in line:
            iface_global['cdp'] = 1
        try:
            iface_global['lldp'] = parse_lldp.parseString(line).asList()[0]
            continue
        except ParseException:
            pass
        try:
            iface_global['version'] = parse_version.parseString(line).asList()[0]
            continue
        except ParseException:
            pass
        try:
            iface_global['model'] = parse_model.parseString(line).asList()[0]
            continue
        except ParseException:
            pass
        try:
            iface_global['active_service'].append(parse_active_service.parseString(line).asList()[-1])
            continue
        except ParseException:
            pass
        try:
            curr = parse_ipv6.parseString(line).asList()[-1]
            try:
                tmp = parse_ipv6_raguard.parseString(curr).asList()[-1].split(' ')
                iface_global['ipv6']['raguard'][tmp[0]] = tmp[1]
            except ParseException:
                pass
            try:
                tmp = parse_ipv6_sourceguard.parseString(curr).asList()[-1].split(' ')
                iface_global['ipv6']['source-guard'][tmp[0]] = tmp[1]
            except ParseException:
                pass
            try:
                tmp = parse_ipv6_snooping.parseString(curr).asList()[-1].split(' ')
                iface_global['ipv6']['snooping'][tmp[0]] = tmp[1]
            except ParseException:
                pass
            try:
                tmp = parse_ipv6_dhcpguard.parseString(curr).asList()[-1].split(' ')
                iface_global['ipv6']['dhcp-guard'][tmp[0]] = tmp[1]
            except ParseException:
                pass
            try:
                tmp = parse_ipv6_destinationguard.parseString(curr).asList()[-1].split(' ')
                iface_global['ipv6']['destination-guard'][tmp[0]] = tmp[1]
            except ParseException:
                pass

        except ParseException:
            pass
        try:
            iface_global['disable_service'].append(parse_disable_service.parseString(line).asList()[-1])
            continue
        except ParseException:
            pass
        try:
            iface_global['disable_service'].append(parse_vstack.parseString(line).asList()[-1])
            continue
        except ParseException:
            pass
        try:
            current_line = parse_enable_password.parseString(line).asList()
            try:
                if iface_global['enable_password'][0] != 'secret':
                    iface_global['enable_password'] = current_line
            except KeyError:
                iface_global['enable_password'] = current_line
            continue
        except ParseException:
            pass
        try:
            current_line = parse_username.parseString(line).asList()[-1]
            iface_global['users'].update(_globalParse___username_attributes(current_line))
            continue
        except ParseException:
            pass
        try:
            vtp = parse_vtp.parseString(line).asList()[-1]
            result_parse_vtp = parsing_checks.vtp._globalParse___vtp_attributes(vtp, iface_global['vtp'])
            if result_parse_vtp:
                iface_global['vtp'] = result_parse_vtp
        except ParseException:
            pass
        # try:
        #     current_line = parse_aaa.parseString(line).asList()[-1]
        #     try:
        #         current_line = authentication.parseString(current_line).asList()[-1]
        #         iface_global['aaa'].setdefault('authentication',{})
        #         iface_global['aaa']['authentication'].update(_globalParse___aaa_attributes(current_line,'authentication',count_authen))
        #         count_authen += 1
        #         continue
        #     except ParseException:
        #         pass
        #     try:
        #         current_line = authorization.parseString(current_line).asList()[-1]
        #         iface_global['aaa'].setdefault('authorization',{})
        #         iface_global['aaa']['authorization'].update(_globalParse___aaa_attributes(current_line,'authorization',count_author))
        #         count_author += 1
        #         continue
        #     except ParseException:
        #         pass
        #     try:
        #         current_line = accounting.parseString(current_line).asList()[-1]
        #         iface_global['aaa'].setdefault('accounting',{})
        #         iface_global['aaa']['accounting'].update(_globalParse___aaa_attributes(current_line,'accounting',count_acc))
        #         count_acc += 1
        #         continue
        #     except:
        #         pass
        # except ParseException:
        #     pass
        try:
            current_line = parse_ip_dhcp.parseString(line).asList()
            iface_global['ip']['dhcp_snooping']['active'] = 'yes'
            if current_line:
                iface_global['ip']['dhcp_snooping']['vlans'] = current_line
        except ParseException:
            pass
        try:
            current_line = parse_ip_arp.parseString(line).asList()
            iface_global['ip']['arp_inspection']['active'] = 'yes'
            if current_line:
                iface_global['ip']['arp_inspection']['vlans'] = current_line
            continue
        except ParseException:
            pass
        try:
            current_line = parse_ip_ssh.parseString(line).asList()[-1]
            iface_global['ip']['ssh'].update(_globalParse___ssh_attributes(current_line))
            continue
        except ParseException:
            pass
        try:
            iface_global['ip']['active_service'].append(parse_ip_service.parseString(line).asList()[-1])
            continue
        except ParseException:
            pass
        try:
            current_line = parse_ip_http.parseString(line).asList()[-1]
            iface_global['ip']['http'].update(_globalParse___http_attributes(current_line))
            continue
        except ParseException:
            pass
        try:
            stp_str = parse_stp.parseString(line).asList()[-1]
            stp_line = parsing_checks.stp_global._globalParse___stp_attributes(stp_str, iface_global['stp'])
            if stp_line != 0:
                iface_global['stp'].update(stp_line)
            continue
        except ParseException:
            pass
        try:
            while line != '!':
                item = parse_line.parseString(line).asList()[-1]
                iface_global['line'][item], next_line = _globalParse___line_attributes(config)
                line = next_line
            continue
        except ParseException:
            pass


# Interface attributes parsing
# Input:  open file with cursor on interface line
# Sample:    example/10.10.1.1.conf
# Output: interface options dictionary
# Sample:    {'vlans': [], 'shutdown': 'no', 'description': '-= MGMT - core.nnn048.nnn =-'}
def _interfaceParse___iface_attributes(config, check_disabled):
    iface_list = get_attributes(config)[0]
    # if iface isn`t enable and unused
    if iface_list:
        iface_dict = {'shutdown': 'no', 'vlans': [], 'cdp': 'yes', 'dhcp_snoop': {'mode': 'untrust'},
                      'arp_insp': {'mode': 'untrust'},
                      'storm control': {}, 'port-security': {}, 'ipv6': {}}

        vlan_num = Word(nums + '-') + ZeroOrMore(Suppress(',') + Word(nums + '-'))
        parse_description = Suppress('description ') + restOfLine
        parse_type = Suppress('switchport mode ') + restOfLine
        parse_storm = Suppress('storm-control ') + restOfLine
        parse_port_sec = Suppress('switchport port-security ') + restOfLine
        parse_stp_port = Suppress('spanning-tree ') + restOfLine
        parse_dhcp_snoop = Suppress('ip dhcp snooping ') + restOfLine
        parse_arp_insp = Suppress('ip arp inspection ') + restOfLine
        parse_source_guard = Suppress('ip verify source ') + restOfLine
        parse_vlans = Suppress('switchport ') + Suppress(MatchFirst('access vlan ' +
                                                                    ('trunk allowed vlan ' + Optional(
                                                                        'add ')))) + vlan_num

        # Reserved options list is using due to 'shutdown' option is usually located at the end of the list, so it breaks cycle if interface is shutdown and function speed increases
        for option in iface_list[::-1]:
            if option == 'shutdown':
                if check_disabled:
                    iface_dict['shutdown'] = 'yes'
                    pass
                else:
                    iface_dict = {'shutdown': 'yes'}
                    break
            if option == 'switchport nonegotiate':
                iface_dict['dtp'] = 'no'
                continue
            if option == 'no cdp enable':
                iface_dict['cdp'] = 'no'
                continue
            if option == 'no mop enabled':
                iface_dict['mop'] = 'no'
                continue
            elif option == 'mop enabled':
                iface_dict['mop'] = 'yes'
                continue
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
                storm_control = parse_storm.parseString(option).asList()[-1]
                iface_dict['storm control'] = parsing_checks.storm_control.__ifaceAttributes___storm_check(storm_control,
                                                                                                   iface_dict[
                                                                                                       'storm control'])
                continue
            except ParseException:
                pass
            try:
                port_sec = parse_port_sec.parseString(option).asList()[-1]
                iface_dict['port-security'] = parsing_checks.port_security.__ifaceAttributes___port_sec_parse(port_sec, iface_dict['port-security'])
                continue
            except ParseException:
                pass
            try:
                dhcp_snoop = parse_dhcp_snoop.parseString(option).asList()[-1]
                iface_dict['dhcp_snoop'] = parsing_checks.ip_iface.__ifaceAttributes___ip_parse(dhcp_snoop, iface_dict['dhcp_snoop'])
                continue
            except ParseException:
                pass
            try:
                arp_insp = parse_arp_insp.parseString(option).asList()[-1]
                iface_dict['arp_insp'] = parsing_checks.ip_iface.__ifaceAttributes___ip_parse(arp_insp, iface_dict['arp_insp'])
                continue
            except ParseException:
                pass
            try:
                stp_port = parse_stp_port.parseString(option).asList()[-1]
                iface_dict['stp'] = stp_port
                continue
            except ParseException:
                pass
            try:
                source_guard = parse_source_guard.parseString(option).asList()[-1]
                iface_dict['source_guard'] = source_guard
                continue
            except ParseException:
                pass
            try:
                ipv6 = parse_ipv6.parseString(option).asList()[-1]
                __ifaceAttributes___ipv6_parse(ipv6, iface_dict['ipv6'])
                continue
            except ParseException:
                pass

        return iface_dict
    else:
        return {'unknown_iface': 1}


# TODO: description
def ___ipv6_parse___subparser(parser, ptype, ipv6, dct):
    dct = util.int_dict_parse(parser, ipv6, ptype, dct)
    tmp = dct[ptype][0].split(' ')
    dct[ptype] = {tmp[0]: tmp[1]}
    return dct


# TODO: description
def __ifaceAttributes___ipv6_parse(ipv6, dct):
    global parse_ipv6_sourceguard
    global parse_ipv6_raguard
    global parse_ipv6_destinationguard
    global parse_ipv6_dhcpguard
    try:
        return ___ipv6_parse___subparser(parse_ipv6_sourceguard, 'source-guard', ipv6, dct)
    except ParseException:
        pass
    try:
        return ___ipv6_parse___subparser(parse_ipv6_raguard, 'ra-guard', ipv6, dct)
    except ParseException:
        pass
    try:
        return ___ipv6_parse___subparser(parse_ipv6_destinationguard, 'destination-guard', ipv6, dct)
    except ParseException:
        pass
    try:
        return ___ipv6_parse___subparser(parse_ipv6_dhcpguard, 'dhcp-guard', ipv6, dct)
    except ParseException:
        pass



# Parse interface options
# Input:  files list to parse
# Sample:    'example/10.10.1.1.conf'
# Output: interface options dictionary
# Sample:    see on top of this file
def interface_parse(config, check_disabled):
    global parse_ipv6
    global parse_iface
    global iface_local
    for line in config:
        try:
            item = parse_iface.parseString(line).asList()[-1]
            iface_local[item] = _interfaceParse___iface_attributes(config, check_disabled)
        except ParseException:
            pass
    return 0


# main function
def parseconfigs(filename, check_disabled):
    global iface_local
    global iface_global

    iface_local = {}
    iface_global = {
        'ip': {'dhcp_snooping': {'active': 'no'}, 'arp_inspection': {'active': 'no'}, 'ssh': {}, 'active_service': [],
               'http': {}}, 'active_service': [], 'disable_service': [], 'aaa': {}, 'users': {}, 'line': {}, 'stp': {},
        'ipv6': {'raguard': {}, 'source-guard': {}, 'snooping': {}}, 'vtp': {}}
    with open(filename) as config:
        try:
            global_parse(config)
            config.seek(0)
            interface_parse(config, check_disabled)
        except Exception as e:
            print("Error in file " + filename)
            print(e)
    return 0


# vlanmap parsing, returns list of three lists with ints
# returns 0 if no vlanmap given
def vlanmap_parse(filename):
    if (filename):
        vlanmap = load(open(filename))
        res = []
        try:
            res.append(vlanmap['critical_area'])  # critical
            res.append(vlanmap['unknown_area'])  # unknown
            res.append(vlanmap['trusted_area'])  # trusted
            cnt = 0
            for zone in res:
                for i in zone:
                    if type(i) is str:
                        rng = i.split('-')
                        res[cnt].remove(i)
                        for n in range(int(rng[0]), int(rng[1]) + 1):
                            res[cnt].append(n)
                cnt += 1
        except:
            print("Error in vlanmap syntax")
            exit()
        return res
    else:
        return 0
