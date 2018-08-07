# Services options check
# Input:
#        global dictionary with defined 'active_service' key inside global_params
#        config result dictionary
# Output:
#        updated result dictionary
#

def check(global_params,results_dict):
# 'should be enable' services section
    if 'password-encryption' in global_params['active_service']:
        results_dict['services']['password-encryption'] = [2, 'ENABLED']
    else:
        results_dict['services']['password-encryption'] = [0, 'DISABLED', 'Turn it on to encrypt passwords']
    if 'tcp-keepalives-in' in global_params['active_service']:
        results_dict['services']['tcp-keepalives-in']   = [2, 'ENABLED']
    else:
        results_dict['services']['tcp-keepalives-in']   = [1, 'DISABLED', 'You may need it to prevent stuck sessions']

# 'should be disable' services section
    if 'pad' in global_params['disable_service']:
        results_dict['services']['pad'] = [2, 'DISABLED']
    else:
        results_dict['services']['pad'] = [0, 'ENABLED', 'Turn it off to prevent potential unauthorized access']
    if 'udp-small-servers' in global_params['active_service']:
        results_dict['services']['udp-small-servers']   = [0, 'ENABLED', 'Turn it off to prevent potential information'
                                                                         'leak and DOS attack']
    else:
        results_dict['services']['udp-small-servers']   = [2, 'DISABLED']
    if 'tcp-small-servers' in global_params['active_service']:
        results_dict['services']['tcp-small-servers']   = [0, 'ENABLED', 'Turn it off to prevent potential information'
                                                                         'leak and DOS attack']
    else:
        results_dict['services']['tcp-small-servers']   = [2, 'DISABLED']

    return results_dict
