# DTP interface options check
# Input:
#        interface dictionary
#        config result dictionary
# Output:
#        updated result dictionary
#           {{'iface1': {'DTP': {'dtp': [severity(int), 'message', 'best practice']}, 'iface2':...}}
#

def check(iface_dct):

    result={}
    if 'dtp' in iface_dct:
        if iface_dct['dtp'] == 'no':
            result['dtp'] = [2, 'DISABLED', 'DTP should not be enable']
        else:
            result['dtp'] = [0, 'ENABLED', 'DTP should not be enable']
    else:
        result['dtp'] = [0, 'ENABLED', 'DTP should not be enable']
    return result





