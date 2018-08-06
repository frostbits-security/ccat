# Users options check
# Input:
#        global dictionary with defined 'users' key inside global_params
#        config result dictionary
# Output:
#        updated result dictionary
#

def check(global_params,results_dict):
    for user in global_params['users']:
        results_dict['users'][user] = {}
        if global_params['users'][user]['password_type'] == '5':
            results_dict['users'][user]['password_type'] = [2, 'Encrypted with MD5']
        else:
            results_dict['users'][user]['password_type'] = [0, 'Weak encryption',
                                                            'Change encryption type to MD5']
        if 'privilege' in global_params['users'][user]:
            if global_params['users'][user]['privilege'] == '15':
                results_dict['users'][user]['privilege'] = [1, 'Privilege level is ' +
                                                            global_params['users'][user]['privilege'],
                                                            'You may want to decrease privilege level']

    return results_dict
