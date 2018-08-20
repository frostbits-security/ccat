#############################
# ARP inspection check

import util


def check_global(global_params, result_dict):
    enabled = 0
    snooping_vlans = []
    result_dict['IP options']['ARP inspection'] = {}

    # globals
    if (global_params['ip']['arp_inspection']['active'] == 'yes'):
        enabled = 1
        result_dict['IP options']['ARP inspection'] = [2, 'ENABLED']
        if ('vlans' in global_params['ip']['arp_inspection']):
            snooping_vlans = util.intify(global_params['ip']['arp_inspection']['vlans'])
    else:
        result_dict['IP options']['ARP inspection'] = [0, 'DISABLED', 'Turn it on to prevent spoofing attack']
    return result_dict, enabled

def check_iface(iface_params, vlanmap_type, allinterf, enabled):
    result_dict={}
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

            if ((mode == 'trust') and  not(vlanmap_type=='TRUSTED')):
                result_dict[i]['ARP inspection']['vlans'] = [0,
                                                                 'Interface set as trusted, but vlanmap is different',
                                                                 'This interface is not trusted according to vlanmap, but marked as trusted. ARP spoofing is possible.']
            else:
                result_dict = 0
    return result_dict