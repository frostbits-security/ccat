# Users options check
# Input:
#        global dictionary with defined 'users' key inside global_params
#        config result dictionary
# Output:
#        updated result dictionary
#

def check(global_params,results_dict):
    admin_count = 0
    for user in global_params['users']:
        results_dict['users'][user] = {}
        if global_params['users'][user]['password_type'] == '5':
            results_dict['users'][user]['password_type'] = [2, 'MD5']
        elif global_params['users'][user]['password_type'] == '4':
            results_dict['users'][user]['password_type'] = [2, 'SHA-256']
        elif global_params['users'][user]['password_type'] == '8':
            results_dict['users'][user]['password_type'] = [2, 'PBKDF2-SHA-256']
        elif global_params['users'][user]['password_type'] == '9':
            results_dict['users'][user]['password_type'] = [2, 'scrypt']
        elif global_params['users'][user]['password_type'] == '7':
            results_dict['users'][user]['password_type'] = [0, 'Weak encryption', 'Change encryption type to strong type']
        elif global_params['users'][user]['password_type'] == '0':
            results_dict['users'][user]['password_type'] = [0, 'No encryption', 'Encrypt password']

        if 'privilege' in global_params['users'][user]:
            if global_params['users'][user]['privilege'] == '15':
                if admin_count <= 1:
                    results_dict['users'][user]['privilege_level'] = [2, global_params['users'][user]['privilege']]
                else:
                    results_dict['users'][user]['privilege_level'] = [1, global_params['users'][user]['privilege'],
                                                                'There are more than 2 admin accounts in system, you '
                                                                'may want to divide privileges']
            admin_count += 1

    return results_dict
