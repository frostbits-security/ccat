
# STP global options check
# Input:
#        global dictionary
#        config result dictionary
# Output:
#        updated result dictionary
#           {{'iface1': {'global stp': {'portfast': [severity(int), 'message', 'best practice'],'loopguard','bpdu'}, 'iface2':...}}
#

def _check__check_stp(global_dct):
    stp_res = {'portfast':0,'loopguard':0,'bpduguard':0}
    for option in stp_res:
        if option in global_dct['stp']:
            if global_dct['stp'][option]==['default']:
                stp_res[option]=[2,'OK',option.capitalize()+' should be turn on']
            else:
                stp_res[option] = [1, 'Warning', option.capitalize() + ' should be turn on']
        else:
            stp_res[option] = [1, 'Warning', option.capitalize() + ' should be turn on']
    return (stp_res)

def check(global_dct, result):
    if 'stp' in global_dct:
        result['global stp'] = _check__check_stp(global_dct)
        return {'global STP':result}

