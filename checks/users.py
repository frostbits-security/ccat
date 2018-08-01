# Users options check
# Input:
#        global dictionary
#        config result dictionary
# Output:
#        updated result dictionary
#

def check(global_params,global_params_results_dict):
    for user in global_params['users']:
        global_params_results_dict['users'][user] = {}
        if global_params['users'][user]['password_type'] == '5':
            global_params_results_dict['users'][user]['password_type'] = [2, 'Encrypted with MD5']
        else:
            global_params_results_dict['users'][user]['password_type'] = [0, 'Weak encryption',
                                                                          'Change encryption type to MD5']
        if 'privilege' in global_params['users'][user]:
            if global_params['users'][user]['privilege'] == '15':
                global_params_results_dict['users'][user]['privilege'] = [1, 'Privilege level is ' +
                                                                          global_params['users'][user]['privilege'],
                                                                          'You may want to decrease it']

    return global_params_results_dict
