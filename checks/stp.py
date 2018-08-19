
# STP interface options check
# Input:
#        interface dictionary
#        config result dictionary
# Output:
#        updated result dictionary
#           {{'iface1': {'STP': {'portfast': [severity(int), 'message', 'best practice']}, 'iface2':...}}
#

def stp_check(iface_dct,flag,result,scale):
    # result = {}
    if 'type' in iface_dct:
        if iface_dct['type'] == 'access':
            if flag==3:
                return 0
            elif 'stp' in iface_dct:
                if iface_dct['stp'] == 'portfast' and flag == 1:
                    result['Portfast'] = [scale[1], 'ENABLED']
                elif iface_dct['stp'] == 'portfast' and flag == 2:
                    result['Portfast'] = [scale[0], 'BPDUGUARD DISABLED', 'The portfast is enabled but bpduguard is disabled']
            else:
                result['Portfast'] = [scale[0], 'DISABLED', 'The portfast must be enabled on the access port']
        else:
            if 'stp' in iface_dct and 'portfast trunk' in iface_dct['stp'] and flag == 1:
                result['Portfast on a trunk port'] = [scale[0], 'WARNING', 'The portfast is enabled on a trunk port']
            elif 'stp' in iface_dct and 'portfast trunk' in iface_dct['stp'] and flag == 0:
                result['Portfast on a trunk port'] = [scale[0], 'WARNING', 'The portfast is enabled on a trunk port and bpduguard is disabled']
        return result
    return 0

def check(iface_dct,flag, vlanmap_type):
    result = {}

# If this network segment is TRUSTED - enabled cdp is not a red type of threat, it will be colored in orange
    if vlanmap_type == 'TRUSTED':
        stp_check(iface_dct,flag,result,[1,2])

# Otherwise if network segment is CRITICAL or UNKNOWN or vlanmap is not defined - enabled cdp is a red type of threat
    else:
        stp_check(iface_dct,flag,result, [0, 2])


    return result




