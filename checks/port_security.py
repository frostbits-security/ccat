# Port-security options check
# Input:
#        interface dictionary
#
# Output:
#        updated result dictionary


def port_sec_check(iface_dct, max_mac, result, scale):
    if 'port-security' in iface_dct and len(iface_dct['port-security']) != 0:
        port_sec_dct = iface_dct['port-security']

        if 'maximum' in port_sec_dct:
            # fix of #11
            ps_max_num = (port_sec_dct['maximum'][0]).split()
            if int(ps_max_num[0]) > max_mac:
                result.update({'Maximum for mac-address port-security': [scale[0], port_sec_dct['maximum'][0],
                                                                         "Maximum for mac-address port-security should be less than {}".format(
                                                                             str(max_mac))]})
            else:
                result.update({'Maximum for mac-address port-security': [scale[2], port_sec_dct['maximum'][0]]})

        #         # [protect,restrict,shutdown]
        if 'violation' in port_sec_dct:
            violation = ['restrict', 'shutdown']
            if port_sec_dct['violation'][0] in violation:
                result.update({'Port-security violation': [scale[2], 'OK']})
            else:
                result.update({'Port-security violation': [scale[1], 'WARNING',
                                                           "Port-security violation should be 'restrict' or 'shutdown'"]})
        else:
            result.update({'Port-security violation': [3, 'Shutdown',
                                                       "Port-security violation should be set up mode 'restrict' or 'shutdown'"]})

        # The aging_time range is 1 to 1440 minutes (default is 0)
        if 'aging time' in port_sec_dct:
            if int(port_sec_dct['aging time'][0]) > 20:
                result.update({'MAC Address Aging time port-security': [scale[0], port_sec_dct['aging time'][0],
                                                                        "MAC Address Aging is equal 0 by default"]})
            else:
                result.update({'MAC Address Aging time port-security': [scale[2], port_sec_dct['aging time'][0]]})
        else:
            result.update({'MAC Address Aging time port-security': [scale[1], 'DEFAULT',
                                                                    "MAC Address Aging is equal 0 by default"]})
        return result
    return 0


def check(iface_dct, vlanmap_type, max_mac=10):
    result = {}

    # If this network segment is TRUSTED - enabled cdp is not a red type of threat, it will be colored in orange
    if vlanmap_type == 'MANAGEMENT':
        port_sec_check(iface_dct, max_mac, result, [1, 1, 2])

    # Otherwise if network segment is CRITICAL or UNKNOWN or vlanmap is not defined - enabled cdp is a red type of threat
    else:
        port_sec_check(iface_dct, max_mac, result, [0, 1, 2])

    return result

