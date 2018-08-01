
# Mode check
# Input:
#        interface dictionary
#        config result dictionary
# Output:
#        updated result dictionary[0-access,1-trunk]
#

def check(iface_dct,result):
    if 'type' in iface_dct:
        if iface_dct['type'] == 'access':
            result['type'] = 0
        else:
            result['type'] = 1