# CDP interface options check
# Input:
#        interface dictionary
#        config result dictionary
# Output:
#        updated result dictionary
#           {{'iface1': {'CDP': {'cdp': [severity(int), 'message', 'best practice']}, 'iface2':...}}
#

def check(iface_dct, vlanmap_type):
    result = {}

# If this network segment is TRUSTED - enabled cdp is not a red type of threat, it will be colored in orange
    if vlanmap_type == 'TRUSTED':
        if 'cdp' in iface_dct:
            if iface_dct['cdp'] == 'no':
                result['cdp'] = [2, 'DISABLED']
            else:
                result['cdp'] = [1, 'ENABLED', 'CDP should not be enable']
        else:
            result['cdp'] = [1, 'ENABLED', 'CDP should not be enable']

# Otherwise if network segment is CRITICAL or UNKNOWN or vlanmap is not defined - enabled cdp is a red type of threat
    else:
        if 'cdp' in iface_dct:
            if iface_dct['cdp'] == 'no':
                result['cdp'] = [2, 'DISABLED']
            else:
                result['cdp'] = [0, 'ENABLED', 'CDP should not be enable']
        else:
            result['cdp'] = [0, 'ENABLED', 'CDP should not be enable']

    return result
