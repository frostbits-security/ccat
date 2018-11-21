#############################
# Source guard check

def srcguard_check(iface_dct,dhcp_flag,scale,result):

    if 'source_guard' in iface_dct and dhcp_flag:
        result['Source Guard'] = [scale[1], 'ENABLED']
    else:
        result['Source Guard'] = [scale[0], 'DISABLED', 'The source guard should be enabled on an access port']
    return result

def check(iface_dct,dhcp_flag, vlanmap_type):
    result = {}
# If this network segment is TRUSTED - enabled cdp is not a red type of threat, it will be colored in orange
    if vlanmap_type == 'MANAGEMENT':
        srcguard_check(iface_dct,dhcp_flag,[1,2],result)

# Otherwise if network segment is CRITICAL or UNKNOWN or vlanmap is not defined - enabled cdp is a red type of threat
    else:
        srcguard_check(iface_dct, dhcp_flag, [0, 2],result)


    return result