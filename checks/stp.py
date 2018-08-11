
# STP interface options check
# Input:
#        interface dictionary
#        config result dictionary
# Output:
#        updated result dictionary
#           {{'iface1': {'STP': {'portfast': [severity(int), 'message', 'best practice']}, 'iface2':...}}
#

def check(iface_dct,flag):
    result = {}
    if 'type' in iface_dct:
        if iface_dct['type'] == 'access':
            if flag==3:
                return 0
            elif 'stp' in iface_dct:
                if iface_dct['stp'] == 'portfast' and flag == 1:
                    result['portfast'] = [2, 'OK', 'A portfast should be enable on access port']
                elif iface_dct['stp'] == 'portfast' and flag == 2:
                    result['portfast'] = [1, 'BPDUGUARD DISABLE', 'A portfast enable but bpduguard disable']
            else:
                result['portfast'] = [1, 'DISABLE', 'A portfast should be enable on access port']
        else:
            if 'stp' in iface_dct and 'portfast trunk' in iface_dct['stp'] and flag == 1:
                result['portfast on trunk'] = [1, 'WARNING', 'A Portfast is on trunk port']
            elif 'stp' in iface_dct and 'portfast trunk' in iface_dct['stp'] and flag == 0:
                result['portfast on trunk'] = [1, 'WARNING', 'A Portfast is on trunk port and bpduguard disable']
        return result
    return 0






