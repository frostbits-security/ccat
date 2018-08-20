# Trunk/access mode check
#
# Input:
#        interface dictionary
# Output:
#        mode dictionary
#
def check(iface_dct):
    result = {}
    if 'type' in iface_dct:
        if iface_dct['type'] == 'access':
            result['type'] = [3, 'ACCESS']
        else:
            result['type'] = [3, 'TRUNK']

    return result