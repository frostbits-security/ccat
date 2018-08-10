
# STP interface options check
# Input:
#        interface dictionary
#        config result dictionary
# Output:
#        updated result dictionary
#           {{'iface1': {'STP': {'portfast': [severity(int), 'message', 'best practice']}, 'iface2':...}}
#

def check(iface_dct):

    result={}
    if 'stp' in iface_dct:
        # Please fix me. Sincerely, Try-except.
        try:
            if iface_dct['type'] == 'access' and iface_dct['stp'] == 'portfast':
                result['portfast'] = [2, 'OK', 'A portfast on access port should be enable']
        except KeyError:
            pass
        if 'portfast trunk' in iface_dct['stp']:
            result['portfast'] =[1, 'WARNING', 'A Portfast on trunk port']
        else:
            result['portfast on trunk'] = [1, 'WARNING', 'A Portfast on trunk port']
    else:
        result['portfast'] = [1, 'DISABLED', 'A portfast on access port should be enable']

    return result



