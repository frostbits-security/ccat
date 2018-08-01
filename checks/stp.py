
# STP interface options check
# Input:
#        interface dictionary
#        config result dictionary
# Output:
#        updated result dictionary
#

def check(iface_dct,result):
    if 'stp' in iface_dct:
        if iface_dct['type'] == 'access' and iface_dct['stp'] == 'portfast':
            result['stp portfast'] = 1
        elif 'trunk' in iface_dct['stp']:
            result['trunk portfast'] = 1
        return result