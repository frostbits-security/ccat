# Users options check
# Input:
#        global dictionary with defined 'users' key inside it
# Output:
#        user options dictionary
def check(global_params):
# create new 'Users' section for further display
    results_dict = {'Users':{}}


# users section
    # admin count in system, more than 2 is insecure by default
    admin_count = 0
    for user in global_params['users']:

        # create new dictionary for next user
        results_dict['Users']['user "'+user+'"'] = {}

        if   global_params['users'][user]['password_type'] == '5':
            results_dict['Users']['user "'+user+'"']['encryption type']    = [2, 'MD5']
        elif global_params['users'][user]['password_type'] == '7':
            results_dict['Users']['user "'+user+'"']['encryption type']    = [0, 'Vigenere', 'Change encryption type to strong type']
        elif global_params['users'][user]['password_type'] == '4':
            results_dict['Users']['user "'+user+'"']['encryption type']    = [2, 'SHA-256']
        elif global_params['users'][user]['password_type'] == '8':
            results_dict['Users']['user "'+user+'"']['encryption type']    = [2, 'PBKDF2-SHA-256']
        elif global_params['users'][user]['password_type'] == '9':
            results_dict['Users']['user "'+user+'"']['encryption type']    = [2, 'scrypt']
        elif global_params['users'][user]['password_type'] == '0':
            results_dict['Users']['user "'+user+'"']['encryption type']    = [0, 'NO', 'Encrypt password']

        # if user has privilege level 15
        if 'privilege' in global_params['users'][user] and global_params['users'][user]['privilege'] == '15':
            if admin_count < 2:
                results_dict['Users']['user "'+user+'"']['privilege level'] = [2, global_params['users'][user]['privilege']]
            else:
                results_dict['Users']['user "'+user+'"']['privilege level'] = [1, global_params['users'][user]['privilege'], 'There are more than 2 admin accounts in system, you may want to divide privileges']
            admin_count += 1


    return results_dict
