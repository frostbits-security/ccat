#############################
# Source guard check

def check(iface_dct,dhcp_flag):
    result={}
    if 'source_guard' in iface_dct and dhcp_flag:
        result['Source Guard'] = [2, 'ENABLED', 'A source_guard should be enable on access port']
    else:
        result['Source Guard'] = [1, 'DISABLED', 'A source_guard should be enable on access port']
    return result
