# Cisco config parsing
# Creates 2 dictionaries with global and interface options
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
parse_active_service        = Suppress('service ')                     + restOfLine
parse_disable_service       = Suppress('no service ')                  + restOfLine
parse_version               = Suppress('version ')                     + restOfLine
parse_model                 = Suppress('boot system flash bootflash:') + restOfLine
parse_ipv6                  = Suppress('ipv6 ')                        + restOfLine
parse_ipv6_sourceguard      = Suppress('source-guard ')                + restOfLine
parse_ipv6_snooping         = Suppress('snooping ')                    + restOfLine
parse_ipv6_raguard          = Suppress('nd raguard ')                  + restOfLine
parse_ipv6_destinationguard = Suppress('destination-guard ')           + restOfLine
parse_ipv6_dhcpguard        = Suppress('dhcp guard ')                  + restOfLine
parse_lldp                  = Suppress('lldp ')                        + restOfLine
parse_username              = Suppress('username ')                    + restOfLine
parse_aaa                   = Suppress('aaa ')                         + restOfLine
parse_stp                   = Suppress('spanning-tree ')               + restOfLine
# parse_vtp                   = Suppress('vtp ')                         + restOfLine
parse_line                  = Suppress('line ')                        + restOfLine
parse_ip_ssh                = Suppress('ip ssh ')                      + restOfLine
parse_arp_proxy             = Suppress('ip arp proxy ')                + restOfLine
parse_vstack                = Suppress('no') + 'vstack'



parse_enable_password = Suppress('enable') + MatchFirst(['secret', 'password']) + Optional(Word(nums) + Suppress(White(exact=1))) + Suppress(restOfLine)
parse_ip_dhcp         = NotAny(White()) + Suppress('ip dhcp snooping') + Optional(Suppress('vlan') + Word(nums) + ZeroOrMore(Suppress(',') + Word(nums)))
parse_ip_arp          = NotAny(White()) + Suppress('ip arp inspection') + Suppress('vlan') + Word(nums) + ZeroOrMore(Suppress(',') + Word(nums))
parse_ip_service      = NotAny(White()) + Suppress('ip') + MatchFirst(['finger', 'identd', 'source-route', 'bootp server'])
parse_ip_http         = NotAny(White()) + Suppress('ip http ') + restOfLine

# aaa_authorization  = Suppress('authorization ')  + restOfLine
aaa_authentication = Suppress('authentication ') + restOfLine
aaa_accounting     = Suppress('accounting ')     + restOfLine
aaa_groups         = Suppress('group server ')   + restOfLine

utill=lambda parse_meth,featur_str:parse_meth.parseString(featur_str).asList()


def catch_exception(func):
    def wrapper(slf):
        try:
            func(slf)
        except ParseException:
            pass
    return wrapper


def catch_exception1(func):
    def wrapper(slf):
        try:
            func(slf)
        except AttributeError:
            pass
    return wrapper

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
    global aaa_authentication
    # global aaa_authorization
    global aaa_accounting
    # global parse_vtp

    count_authen, count_author, count_acc = 1, 1, 1



    # it is attempt to do class



    class VTP:

        def __init__(self):
            self.dct = {}


        def new_line(self,line):
            parse_vtp = Suppress('vtp ') + restOfLine
            try:
                self.vtp_str = parse_vtp.parseString(line).asList()[-1]
                self.info_domain()
                self.info_mode()
            except ParseException:
                pass


        def add_dct(self):
            iface_global['vtp'] = self.dct


        @catch_exception
        def parse_domain(self):
            domain = Suppress('domain ') + restOfLine
            self.domain = utill(domain, self.vtp_str)

        @catch_exception
        def parse_mode(self):
            mode = Suppress('mode ') + restOfLine
            self.mode = utill(mode, self.vtp_str)

        @catch_exception1
        def info_mode(self):
            self.parse_mode()
            self.dct['mode'] = self.mode

        @catch_exception1
        def info_domain(self):
            self.parse_domain()
            self.dct['domain'] = self.domain


    cl_vtp = VTP()

    for line in config:
        cl_vtp.new_line(line)
        if 'no cdp run' in line:
            iface_global['cdp'] = 1

        try:
            iface_global['lldp']    = parse_lldp   .parseString(line).asList()[0]
            continue
        except ParseException:
            pass

        try:
            iface_global['version'] = parse_version.parseString(line).asList()[0]
            continue
        except ParseException:
            pass

        try:
            iface_global['model']   = parse_model  .parseString(line).asList()[0]
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
            iface_global['users'].update(parsing_checks.username._globalParse___username_attributes(current_line))
            continue
        except ParseException:
            pass


        try:
            current_line = parse_aaa.parseString(line).asList()[-1]
            try:
                current_line = aaa_groups.parseString(current_line)[0].split()
                iface_global['aaa'].setdefault('groups',{})
                iface_global['aaa']['groups'].setdefault(current_line[0],[])
                iface_global['aaa']['groups'][current_line[0]].append(current_line[1])
                continue
            except ParseException:
                pass

            try:
                current_line = aaa_authentication.parseString(current_line).asList()[-1]
                iface_global['aaa'].setdefault('authentication',{})
                iface_global['aaa']['authentication'].update(parsing_checks.aaa._globalParse___aaa_attributes(current_line,'authentication',count_authen))
                count_authen += 1
                continue
            except ParseException:
                pass
            # try:
            #     current_line = aaa_authorization.parseString(current_line).asList()[-1]
            #     iface_global['aaa'].setdefault('authorization',{})
            #     iface_global['aaa']['authorization'].update(parsing_checks.aaa._globalParse___aaa_attributes(current_line,'authorization',count_author))
            #     count_author += 1
            #     continue
            # except ParseException:
            #     pass
            try:
                current_line = aaa_accounting.parseString(current_line).asList()[-1]
                iface_global['aaa'].setdefault('accounting',{})
                iface_global['aaa']['accounting'].update(parsing_checks.aaa._globalParse___aaa_attributes(current_line,'accounting',count_acc))
                count_acc += 1
                continue
            except:
                pass
        except ParseException:
            pass

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
            iface_global['ip']['ssh'].update(parsing_checks.ssh._globalParse___ssh_attributes(current_line))
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
            iface_global['ip']['http'].update(parsing_checks.http._globalParse___http_attributes(current_line))
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
            iface_global['arp_proxy'] = parse_arp_proxy.parseString(line).asList()[-1]
            continue
        except ParseException:
            pass

        try:
            while line != '!':
                item = parse_line.parseString(line).asList()[-1]
                iface_global['line'][item], next_line = parsing_checks.lines._globalParse___line_attributes(config)
                line = next_line
            continue
        except ParseException:
            pass
    cl_vtp.add_dct()

# Interface attributes parsing
# Input:  open file with cursor on interface line
# Sample:    example/10.10.1.1.conf
# Output: interface options dictionary
# Sample:    {'vlans': [], 'shutdown': 'no', 'description': '-= MGMT - core.nnn048.nnn =-'}

def _interfaceParse___iface_attributes(config, check_disabled):
    iface_list = util.get_attributes(config)[0]

    # if iface isn`t enable and unused
    if iface_list:
        iface_dict = {'shutdown': 'no', 'vlans': [], 'cdp': 'yes', 'dhcp_snoop': {'mode': 'untrust'},
                      'arp_insp': {'mode': 'untrust'},
                      'storm control': {}, 'port-security': {}, 'ipv6': {}}

        vlan_num = Word(nums + '-') + ZeroOrMore(Suppress(',') + Word(nums + '-'))

        parse_description     = Suppress('description ')              + restOfLine
        parse_type            = Suppress('switchport mode ')          + restOfLine
        parse_port_sec        = Suppress('switchport port-security ') + restOfLine
        parse_stp_port        = Suppress('spanning-tree ')            + restOfLine
        parse_dhcp_snoop      = Suppress('ip dhcp snooping ')         + restOfLine
        parse_arp_insp        = Suppress('ip arp inspection ')        + restOfLine
        parse_source_guard    = Suppress('ip verify source ')         + restOfLine
        parse_arp_proxy_iface = Optional(Word(alphas))   + Suppress('ip proxy-arp')

        parse_vlans = Suppress('switchport ') + Suppress(MatchFirst('access vlan ' + ('trunk allowed vlan ' + Optional('add ')))) + vlan_num

        class Storm:

            def __init__(self):
                self.dct = {'type': []}

            def new_line(self,line):
                parse_storm = Suppress('storm-control ') + restOfLine

                try:
                    self.storm_line = parse_storm.parseString(line).asList()[-1]
                    self.level_info()
                    self.action_info()
                    self.type_info()
                except ParseException:
                    pass

            @catch_exception
            def parse_level(self):
                parse_level = Word(alphas) + Suppress('level ') + restOfLine
                value = parse_level.parseString(self.storm_line).asList()
                if 'level' in self.dct:
                    self.dct['level'].append(value)
                else:
                    self.dct['level'] = [value]

            @catch_exception
            def parse_action(self):
                action = Suppress('action ') + Word(alphas)
                self.action = utill(action, self.storm_line)

            @catch_exception
            def parse_type(self):
                type = Word(alphas) + Suppress(Optional("include")) + Word(alphas)
                self.type = utill(type, self.storm_line)

            @catch_exception1
            def action_info(self):
                self.parse_action()
                self.dct['action'] = self.action

            @catch_exception1
            def type_info(self):
                self.parse_type()

                for each in self.type:

                    if each not in self.dct['type'] and each in ['broadcast', 'multicast', 'unicast']:
                        self.dct['type'].append(each)

            @catch_exception1
            def level_info(self):
                self.parse_level()

        cl_storm = Storm()

        # Reserved options list is using due to 'shutdown' option is usually located at the end of the list, so it breaks cycle if interface is shutdown and function speed increases
        for option in iface_list[::-1]:
            cl_storm.new_line(option)
            iface_dict['storm control']=cl_storm.dct
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
                # making a str:str instead of str:list
                # see issue #5
                if'mode' in iface_dict['arp_insp']:
                    iface_dict['arp_insp']['mode']=iface_dict['arp_insp']['mode'][0]
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
            try:
                arp_proxy_iface = parse_arp_proxy_iface.parseString(option).asList()[-1]
                iface_dict['arp_proxy'] = arp_proxy_iface
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
            res.append(vlanmap['dmz'])         # critical
            res.append(vlanmap['other'])      # unknown
            res.append(vlanmap['management'])  # trusted
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
