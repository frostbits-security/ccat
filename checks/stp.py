
# STP interface options check
# Input:
#        interface dictionary
#        config result dictionary
# Output:
#        updated result dictionary
#           {{'iface1': {'STP': {'portfast': [severity(int), 'message', 'best practice']}, 'iface2':...}}
#

def check(iface_dct,dct):
    for each in iface_dct:
        result={}
        if 'stp' in iface_dct[each]:
            if iface_dct[each]['type'] == 'access' and iface_dct[each]['stp'] == 'portfast':
                result['portfast'] = [2, 'OK', 'Portfast should be enable']
            elif 'portfast trunk' in iface_dct[each]['stp']:
                result['portfast'] =[1, 'WARNING', 'Portfast should be enable']
            else:
                result['portfast on trunk'] = [1, 'WARNING', 'Portfast is on the trunk mode port']
        else:
            result['portfast'] = [0, 'BAD', 'Portfast should be enable']
        dct.update({each: {'STP': result}})
    return dct



