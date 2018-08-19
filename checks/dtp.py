# DTP interface options check
# Input:
#        interface dictionary
#        config result dictionary
# Output:
#        updated result dictionary
#           {{'iface1': {'DTP': {'dtp': [severity(int), 'message', 'best practice']}, 'iface2':...}}
#

def dtp_check(global_dct,iface_dct,result,scale):

    if 'version' in global_dct and float(global_dct['version'])>12.2:
        print(float(global_dct['version']))
        result['Dynamic Trunking Protocol(DTP)'] = [scale[1], 'DISABLED']
    else:
        if 'dtp' in iface_dct:
            if iface_dct['dtp'] == 'no':
                result['Dynamic Trunking Protocol(DTP)'] = [scale[1], 'DISABLED']
            else:
                result['Dynamic Trunking Protocol(DTP)'] = [scale[0], 'ENABLED', 'DTP should not be enable']
        else:
            result['Dynamic Trunking Protocol(DTP)'] = [scale[0], 'ENABLED', 'DTP should not be enable']
    return result


def check(global_dct,iface_dct, vlanmap_type):
    result = {}

# If this network segment is TRUSTED - enabled cdp is not a red type of threat, it will be colored in orange
    if vlanmap_type == 'TRUSTED':
        dtp_check(global_dct,iface_dct,result,[1,2])

# Otherwise if network segment is CRITICAL or UNKNOWN or vlanmap is not defined - enabled cdp is a red type of threat
    else:
        dtp_check(global_dct,iface_dct,result, [0, 2])


    return result





