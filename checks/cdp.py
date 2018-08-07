# CDP interface options check
# Input:
#        interface dictionary
#        config result dictionary
# Output:
#        updated result dictionary
#           {{'iface1': {'CDP': {'cdp': [severity(int), 'message', 'best practice']}, 'iface2':...}}
#

def check(iface_dct,dct):
    for iface in iface_dct:
        result = {}
        if 'cdp' in iface_dct[iface]:
            if iface_dct[iface]['cdp'] == 'no':
                result['cdp'] = [2, 'OK', 'CDP should not be enable']
            else:
                result['cdp'] = [0, 'BAD', 'CDP should not be enable']
        else:
            result['cdp'] = [0, 'BAD', 'CDP should not be enable']
        # At first iteration creates new empty dictionary, add it to begin of the global iteration function for interface attributes check !!!
        dct[iface] = {}
        dct[iface].update(result)
    return dct


