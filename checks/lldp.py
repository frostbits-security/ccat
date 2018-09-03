def check(global_dct):
    if 'lldp' in global_dct:
        return {'Link Layer Discovery Protocol(LLDP)':{'LLDP':[1,'ENABLED','LLDP should be disabled']}}
    else:
        return {'Link Layer Discovery Protocol(LLDP)':{'LLDP':[2, 'DISABLED']}}