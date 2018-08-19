
# STP global options check
# Input:
#        global dictionary
#        config result dictionary
# Output:
#        updated result dictionary
#           {{'iface1': {'global stp': {'portfast': [severity(int), 'message', 'best practice'],'loopguard','bpdu'}, 'iface2':...}}
#

def _check__check_stp(global_dct):
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

def check(global_dct):
    if 'stp' in global_dct:
        flag=0
        result={}
        result['Spanning-tree options']=_check__check_stp(global_dct['stp'])
        if 'bpduguard' in global_dct['stp'] and 'portfast' in global_dct['stp'] and global_dct['stp']['portfast']==['default']:
            flag=3
        elif 'portfast' in global_dct['stp'] and global_dct['stp']['portfast']==['default']:
            flag=2
        elif 'bpduguard' in global_dct['stp']:
            flag=1

        return (result,flag)
