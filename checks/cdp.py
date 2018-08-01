# CDP interface options check
# Input:
#        interface dictionary
#        config result dictionary
# Output:
#        updated result dictionary
#

def check(iface_dct,result):
    if 'cdp' in iface_dct:
        if iface_dct['cdp'] == 'no':
            result['cdp'] = 0
        else:
            result['cdp'] = 1
        return result