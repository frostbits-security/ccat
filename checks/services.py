# Services options check
# Input:
#        global dictionary
#        config result dictionary
# Output:
#        updated result dictionary
#

def check(global_params,global_params_results_dict):
# active services section
    if 'password-encryption' in global_params['active_service']:
        global_params_results_dict['active_service']['password-encryption'] = [2, 'ENABLED']
    else:
        global_params_results_dict['active_service']['password-encryption'] = [0, 'DISABLED',
                                                                               'Turn it on to ecrypt passwords']
    if 'tcp-keepalives-in' in global_params['active_service']:
        global_params_results_dict['active_service']['tcp-keepalives-in'] = [2, 'ENABLED']
    else:
        global_params_results_dict['active_service']['tcp-keepalives-in'] = [1, 'DISABLED',
                                                                             'You may need it to prevent stuck sessions']
    if 'udp-small-servers' in global_params['active_service']:
        global_params_results_dict['active_service']['udp-small-servers'] = [0, 'ENABLED',
                                                                             'Turn it on to prevent lalala']
    else:
        global_params_results_dict['active_service']['udp-small-servers'] = [2, 'DISABLED']
    if 'tcp-small-servers' in global_params['active_service']:
        global_params_results_dict['active_service']['tcp-small-servers'] = [0, 'ENABLED',
                                                                             'Turn it on to prevent lalala']
    else:
        global_params_results_dict['active_service']['tcp-small-servers'] = [2, 'DISABLED']

# disable services section
    if 'pad' in global_params['disable_service']:
        global_params_results_dict['disable_service']['pad'] = [2, 'DISABLED']
    else:
        global_params_results_dict['disable_service']['pad'] = [0, 'ENABLED', 'Turn it off']

    return global_params_results_dict
