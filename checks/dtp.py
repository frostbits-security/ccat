# DTP interface options check
# Input:
#        interface dictionary
#        config result dictionary
# Output:
#        updated result dictionary
#           {{'iface1': {'DTP': {'dtp': [severity(int), 'message', 'best practice']}, 'iface2':...}}
#

def check(iface_dct,dct):
    for iface in iface_dct:
        result={}
        if 'dtp' in iface_dct[iface]:
            if iface_dct[iface]['dtp'] == 'no':
                result['dtp'] = [2, 'OK', 'DTP should not be enable']
            else:
                result['dtp'] = [0, 'BAD', 'DTP should not be enable']
        else:
            result['dtp'] = [0, 'BAD', 'DTP should not be enable']
        dct.update({iface:{'DTP':result}})
    return dct



