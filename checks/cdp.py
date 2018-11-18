# CDP interface options check
# Input:
#        interface dictionary
#        interface type from vlanmap
# Output:
#        result dictionary
#           {'Cisco Discovery Protocol(CDP)': {'cdp': [severity(int), 'message', 'best practice']}
#
def _iface_check__cdp_check(result,scale,dct):
    if dct['cdp'] == 'no':
        result['Cisco Discovery Protocol(CDP)'] = [scale[1], 'DISABLED']
    else:
        result['Cisco Discovery Protocol(CDP)'] = [scale[0], 'ENABLED', 'CDP should not be enabled']
    return result

def iface_check(iface_dct, vlanmap_type,flag):
    result = {}
    # If CDP isn`t disabled at global
    if flag!=1:
# If this network segment is TRUSTED - enabled cdp is not a red type of threat, it will be colored in orange
        if vlanmap_type == 'MANAGEMENT':
            _iface_check__cdp_check(result,[1,2],iface_dct)

    # Otherwise if network segment is CRITICAL or UNKNOWN or vlanmap is not defined - enabled cdp is a red type of threat
        else:
            _iface_check__cdp_check(result, [0, 2], iface_dct)

        return result
    else:
        return 0

def global_check(global_dct):
    if 'cdp' in global_dct:
        return {'Cisco Discovery Protocol(CDP)':{'Cisco Discovery Protocol(CDP) by default':[2,'DISABLED']}},1
    else:
        return 0,0