
# Mode check
# Input:
#        interface dictionary
#        config result dictionary
# Output:
#        updated result dictionary[0-access,1-trunk]
#

def check(iface_dct,result_dict):
    for iface in iface_dct:
        result = {}

        if 'type' in iface_dct[iface]:
            if iface_dct[iface]['type'] == 'access':
                result['type'] = [2, 'ACCESS']
            else:
                result['type'] = [2, 'TRUNK']
            result_dict[iface].update(result)

    return result_dict