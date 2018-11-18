# MOP interface options check
# Input:
#        interface dictionary
#        interface type from vlanmap
#        interface name
# Output:
#        result dictionary
#           {'Maintenance Operations Protocol (MOP)': [severity(int), 'message', 'best practice']}
#
def mop_check(result, scale, dct, iface):
    if 'mop' in dct:
        if dct['mop'] == 'no':
            result['Maintenance Operations Protocol (MOP)'] = [scale[1], 'DISABLED']
        else:
            result['Maintenance Operations Protocol (MOP)'] = [scale[0], 'ENABLED', 'MOP should not be enabled']

    # By default, MOP is enabled on all Ethernet interfaces, and disabled on all other type of interfaces
    elif 'Ethernet' in iface:
        result['Maintenance Operations Protocol (MOP)'] = [scale[0], 'ENABLED', 'MOP should not be enabled']
    else:
        result['Maintenance Operations Protocol (MOP)'] = [scale[1], 'DISABLED']

    return result

def check(iface_dct, vlanmap_type, iface):
    result = {}

# If this network segment is TRUSTED - enabled mop is not a red type of threat, it will be colored in orange
    if vlanmap_type == 'MANAGEMENT':
        mop_check(result, [1, 2], iface_dct, iface)

# Otherwise if network segment is CRITICAL or UNKNOWN or vlanmap is not defined - enabled mop is a red type of threat
    else:
        mop_check(result, [0, 2], iface_dct, iface)


    return result
