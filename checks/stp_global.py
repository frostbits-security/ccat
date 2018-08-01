
# STP global options check
# Input:
#        global dictionary
#        config result dictionary
# Output:
#        updated result dictionary
#

def check_stp(global_dct):
    stp_res = {'portfast':0,'loopguard':0,'bpdu':0}
    for option in stp_res:
        if option in global_dct['stp']:
            stp_res[option]=1
    return (stp_res)

def check(global_dct, result):
    if 'stp' in global_dct[config]:
        result['global stp'] = check_stp(global_dct)
        return result