
import util

def check(global_params,result_dict):
    enabled=0
    snooping_vlans=[]
    result_dict['IP options']['DHCP snooping']={}

    ### Globals
    # Checking if dhcp snooping is enabled
    if(global_params['ip']['dhcp_snooping']['active']=='yes'):
        enabled=1
        result_dict['IP options']['DHCP snooping'] = [2,'ENABLED']
        if ('vlans' in global_params['ip']['dhcp_snooping']):
            snooping_vlans=util.intify(global_params['ip']['dhcp_snooping']['vlans'])
    else:
        result_dict['IP options']['DHCP snooping'] = [0,'DISABLED', 'Enable this feature to prevent MITM and DHCP starvation attacks']

    return result_dict,enabled