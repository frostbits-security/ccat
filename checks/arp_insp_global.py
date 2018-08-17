import util


def check(global_params, result_dict):
    enabled = 0
    snooping_vlans = []
    result_dict['ip']['ARP inspection'] = {}

    # globals
    if (global_params['ip']['arp_inspection']['active'] == 'yes'):
        enabled = 1
        result_dict['ip']['ARP inspection'] = [2, 'ENABLED']
        if ('vlans' in global_params['ip']['arp_inspection']):
            snooping_vlans = util.intify(global_params['ip']['arp_inspection']['vlans'])
    else:
        result_dict['ip']['ARP inspection'] = [0, 'DISABLED', 'Turn it on to prevent spoofing attack']
    return result_dict, enabled