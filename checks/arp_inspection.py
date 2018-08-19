#############################
# ARP inspection check

def arp_check(iface_params, vlanmap, allinterf, enabled,result_dict,scale):
    ### Interfaces
    # result_dict = {}
    if (enabled):
        try:
            iface_arp = iface_params['arp_insp']
        except:
            pass
        iface_vlans = []
        # check if interface has vlans on it
        if 'vlans' in iface_params:
            iface_vlans = iface_params['vlans']
        # check if interface is turned off, and if we need to check disabled interfaces
        if (not (allinterf) and iface_params['shutdown'] == 'yes'):
            pass
        else:
            # create dictionary for output
            if not ('ARP inspection' in result_dict):
                result_dict['ARP inspection'] = {}
            mode = iface_arp['mode']

            if ((mode == 'trust') and vlanmap and iface_vlans):
                if (set(vlanmap[2]).isdisjoint(iface_vlans)):
                    result_dict[i]['ARP inspection']['vlans'] = [scale,
                                                                 'Interface set as trusted, but vlanmap is different',
                                                                 'This interface is not trusted according to vlanmap, but marked as trusted. ARP spoofing is possible.']
            else:
                result_dict = 0
    return result_dict

def check(iface_params, vlanmap, allinterf, enabled,vlanmap_type):
    result = {}
# If this network segment is TRUSTED - enabled cdp is not a red type of threat, it will be colored in orange
    if vlanmap_type == 'TRUSTED':
        arp_check(iface_params, vlanmap, allinterf, enabled, result, 1)

# Otherwise if network segment is CRITICAL or UNKNOWN or vlanmap is not defined - enabled cdp is a red type of threat
    else:
        arp_check(iface_params, vlanmap, allinterf, enabled, result, 0)
    return result

