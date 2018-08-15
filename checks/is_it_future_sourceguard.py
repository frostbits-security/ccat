#############################
# Port security check

def check(iface_dct):
    result={}
    chk=0
    try:
        chk=iface_dct['port_security']=={}
    except:
        pass
    if not chk:
        result['Port security'] = [0, 'DISABLED', 'ARP spoofing is possible']
    else:
        result['Port security'] = [2, 'ENABLED']

    return result
