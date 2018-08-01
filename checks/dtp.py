# DTP interface options check
# Input:
#        interface dictionary
#        config result dictionary
# Output:
#        updated result dictionary
#

def check(iface_dct,result):
    if 'dtp' in iface_dct:
        if iface_dct['dtp'] == 'no':
            result['dtp'] = 0
        else:
            result['dtp'] = 1
        return result