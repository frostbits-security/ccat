def check(global_dct):
    result={}
    if global_dct['vtp']:
        if 'mode' in global_dct['vtp']:
            result['VLAN Trunking Protocol(VTP) mode']=[3,global_dct['vtp']['mode'][0].capitalize(),'VTP should be turned off']
        elif 'domain' in global_dct['vtp']:
            result['VLAN Trunking Protocol(VTP) mode'] = [1, 'Server/Client mode', 'VTP should be turned off']
        else:
            result['VLAN Trunking Protocol(VTP) mode'] = [1, 'Server/Client mode','VTP should be turned off']
    return {'VLAN Trunking Protocol':result}