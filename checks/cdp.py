# CDP interface options check
# Input:
#        interface dictionary
#        config result dictionary
# Output:
#        updated result dictionary
#           {{'iface1': {'CDP': {'cdp': [severity(int), 'message', 'best practice']}, 'iface2':...}}
#

def cdp_check(result,scale,dct):
    if 'cdp' in dct:
        if dct['cdp'] == 'no':
            result['Cisco Discovery Protocol(CDP)'] = [scale[1], 'DISABLED']
        else:
            result['Cisco Discovery Protocol(CDP)'] = [scale[0], 'ENABLED', 'CDP should not be enable']
    else:
        result['Cisco Discovery Protocol(CDP)'] = [scale[0], 'ENABLED', 'CDP should not be enable']
    return result

def check(iface_dct, vlanmap_type):
    result = {}

# If this network segment is TRUSTED - enabled cdp is not a red type of threat, it will be colored in orange
    if vlanmap_type == 'TRUSTED':
        cdp_check(result,[1,2],iface_dct)

# Otherwise if network segment is CRITICAL or UNKNOWN or vlanmap is not defined - enabled cdp is a red type of threat
    else:
        cdp_check(result, [0, 2], iface_dct)


    return result
