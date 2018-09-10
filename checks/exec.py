# EXEC options check
# Input:
#        global dictionary with defined 'enable_password' key inside it
# Output:
#        EXEC password options dictionary
def check(global_params):
# create new 'EXEC password' section for further display
    results_dict = {'EXEC password':{}}


# EXEC password section
    if 'enable_password' in global_params:
        try:
            if   global_params['enable_password'][1] == '5':
                results_dict['EXEC password']['encryption type'] = [2, 'MD5']
            elif global_params['enable_password'][1] == '7':
                results_dict['EXEC password']['encryption type'] = [0, 'Vigenere', 'Change encryption type to strong type']
            elif global_params['enable_password'][1] == '4':
                results_dict['EXEC password']['encryption type'] = [2, 'SHA-256']
            elif global_params['enable_password'][1] == '8':
                results_dict['EXEC password']['encryption type'] = [2, 'PBKDF2-SHA-256']
            elif global_params['enable_password'][1] == '9':
                results_dict['EXEC password']['encryption type'] = [2, 'scrypt']
        except IndexError:
            results_dict    ['EXEC password']['type']            = [0, 'No encryption', 'Encrypt EXEC mode password']
    else:
        results_dict        ['EXEC password']['type']            = [0, 'No password', 'Set password on EXEC mode']


    return results_dict
