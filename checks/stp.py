# STP interface options check
# Input:
#        interface dictionary
#        config result dictionary
# Output:
#        updated result dictionary
#           {{'iface1': {'STP': {'portfast': [severity(int), 'message', 'best practice']}, 'iface2':...}}
#

def _iface_check__stp_check(iface_dct,flag,result,scale):
    # result = {}
    if 'type' in iface_dct:
        if iface_dct['type'] == 'access':
            if flag==3:
                return 0
            elif 'stp' in iface_dct:
                if iface_dct['stp'] == 'portfast' and flag == 1:
                    result['Portfast'] = [scale[1], 'ENABLED']
                elif iface_dct['stp'] == 'portfast' and flag == 2:
                    result['Portfast'] = [scale[0], 'BPDUGUARD DISABLED', 'The portfast is enabled but bpduguard is disabled']
            else:
                result['Portfast'] = [scale[0], 'DISABLED', 'The portfast must be enabled on the access port']
        else:
            if 'stp' in iface_dct and 'portfast trunk' in iface_dct['stp'] and flag == 1:
                result['Portfast on a trunk port'] = [scale[0], 'WARNING', 'The portfast is enabled on a trunk port']
            elif 'stp' in iface_dct and 'portfast trunk' in iface_dct['stp'] and flag == 0:
                result['Portfast on a trunk port'] = [scale[0], 'WARNING', 'The portfast is enabled on a trunk port and bpduguard is disabled']
        return result
    return 0

def iface_check(iface_dct,flag, vlanmap_type):
    result = {}

# If this network segment is TRUSTED
    if vlanmap_type == 'MANAGEMENT':
        _iface_check__stp_check(iface_dct,flag,result,[1,2])

# Otherwise if network segment is CRITICAL or UNKNOWN or vlanmap is not defined
    else:
        _iface_check__stp_check(iface_dct,flag,result, [0, 2])

    return result


def _global_check__check_stp(global_dct):
    stp_res = {'Portfast':0,'Loopguard':0,'Bpduguard':0}
    for option in stp_res:
        if option.lower() in global_dct:
            if global_dct[option.lower()][0]=='default':
                stp_res[option]=[2,'OK',option.capitalize()+' should be turned on']
            else:
                stp_res[option] = [1, 'WARNING', option.capitalize() + ' should be turned on']
        else:
            stp_res[option] = [1, 'WARNING', option.capitalize() + ' should be turned on']
    return (stp_res)

def global_check(global_dct):
    if 'stp' in global_dct:
        flag=0
        result={}
        result['Spanning-tree options']=_global_check__check_stp(global_dct['stp'])
        if 'bpduguard' in global_dct['stp'] and 'portfast' in global_dct['stp'] and global_dct['stp']['portfast']==['default']:
            flag=3
        elif 'portfast' in global_dct['stp'] and global_dct['stp']['portfast']==['default']:
            flag=2
        elif 'bpduguard' in global_dct['stp']:
            flag=1

        return (result,flag)
