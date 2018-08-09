# CDP interface options check
# Input:
#        interface dictionary
#        config result dictionary
# Output:
#        updated result dictionary
#           {{'iface1': {'CDP': {'cdp': [severity(int), 'message', 'best practice']}, 'iface2':...}}
#

def check(iface_dct):

    result = {}
    if 'cdp' in iface_dct:
        if iface_dct['cdp'] == 'no':
            result['cdp'] = [2, 'DISABLED', 'CDP should not be enable']
        else:
            result['cdp'] = [0, 'ENABLED', 'CDP should not be enable']
    else:
        result['cdp'] = [0, 'ENABLED', 'CDP should not be enable']

    return result



