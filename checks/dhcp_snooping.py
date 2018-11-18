import util

def check_iface(iface_params, vlanmap_type, allinterf, enabled):
    result_dict={}
    if (enabled):
        try:
            iface_snoop = iface_params['dhcp_snoop']
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
            if not ('DHCP snooping' in result_dict):
                result_dict['DHCP snooping'] = {}
            mode = iface_snoop['mode']
        if (mode == 'untrust'):
            # check if limit is set and range is good
            if 'limit' in iface_snoop:
                chkres = 0
                chkres = int(iface_snoop['limit'][0]) > 100
                # TODO: need to handle something like '100 burst 10'
                # TODO: i belive it was here, but broken by someone (check git history)
                # except:
                #     print(int(iface_snoop['limit'][0].split(' ')[0]))
                #     # push first number
                #     chkres = int(iface_snoop['limit'][0].split(' ')[0]) > 100
                if (chkres):
                    result_dict['DHCP snooping']['rate limit'] = [1, 'Too high','DHCP starvation prevention is inefficient']
                else:
                    result_dict['DHCP snooping']['rate limit'] = [2, 'OK','DHCP starvation prevention is efficient']

            else:
                result_dict['DHCP snooping']['rate limit'] = [1, 'Not set', 'Needed to prevent DHCP starvation']
        # check if trusted interface is marked as trusted in vlamap
        elif ((mode == 'trust') and not (vlanmap_type == 'MANAGEMENT')):
            result_dict['DHCP snooping']['vlans'] = [0, 'Interface set as trusted, but vlanmap is different',
                                                     'This interface is not trusted according to vlanmap, but marked as trusted. Unauthorized DHCP server can work here']
        else:
            result_dict = 0
    return result_dict

def check_global(global_params,result_dict):
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
