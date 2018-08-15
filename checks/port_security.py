# Port-security options check
# Input:
#        interface dictionary
#
# Output:
#        updated result dictionary


def check(iface_dct,max_mac=10):
    result={}
    if 'port-security' in iface_dct and len(iface_dct['port-security']) != 0:
        port_sec_dct=iface_dct['port-security']

        if 'maximum' in port_sec_dct:
            if int(port_sec_dct['maximum'][0])>max_mac:
                result.update({'Maximum for mac-address port-security': [0, port_sec_dct['maximum'][0], "Maximum for mac-address port-security should be less than 10"]})
            else:
                result.update({'Maximum for mac-address port-security': [2, port_sec_dct['maximum'][0], "Maximum for mac-address port-security should be less than 10"]})
        # [protect,restrict,shutdown]
        if 'violation' in port_sec_dct:
            violation=['restrict','shutdown']
            if port_sec_dct['violation'][0] in violation:
                result.update({'Violation for port-security': [2, 'OK', "Port-security violation should be 'restrict' or 'shutdown'"]})
            else:
                result.update({'Violation for port-security': [1, 'WARNING', "Port-security violation should be 'restrict' or 'shutdown'"]})
        else:
            result.update({'Violation for port-security': [0, 'DISABLE',
                                                           "Port-security violation should be set up mode 'restrict' or 'shutdown'"]})

        # The aging_time range is 1 to 1440 minutes (default is 0)
        if 'aging time' in port_sec_dct:
            if int(port_sec_dct['aging time'][0])>20:
                result.update({'MAC Address Aging time port-security': [0, port_sec_dct['aging time'][0],
                                                                        "MAC Address Aging is equal 0 by default"]})
            else:
                result.update({'MAC Address Aging time port-security': [2, port_sec_dct['aging time'][0],
                                                                        "MAC Address Aging is equal 0 by default"]})
        else:
            result.update({'MAC Address Aging time port-security': [1, 'DEFAULT',
                                                           "MAC Address Aging is equal 0 by default"]})
        return result
    return 0
