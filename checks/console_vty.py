# Console and vty options check
# Input:
#        global dictionary with defined 'line' key inside global_params
#        config result dictionary
# Output:
#        updated result dictionary
#

def check(global_params,results_dict):
# enable password section
    if 'enable_password' in global_params:
        try:
            if global_params['enable_password'][1]   == '5':
                results_dict['enable_password']['type'] = [2, 'MD5']
            elif global_params['enable_password'][1] == '7':
                results_dict['enable_password']['type'] = [0, 'Weak encryption', 'Change encryption type to strong type']
            elif global_params['enable_password'][1] == '4':
                results_dict['enable_password']['type'] = [2, 'SHA-256']
            elif global_params['enable_password'][1] == '8':
                results_dict['enable_password']['type'] = [2, 'PBKDF2-SHA-256']
            elif global_params['enable_password'][1] == '9':
                results_dict['enable_password']['type'] = [2, 'scrypt']
        except IndexError:
            results_dict['enable_password']['type'] = [0, 'No encryption', 'Encrypt EXEC mode password']
    else:
        results_dict['enable_password']['type'] = [0, 'No password', 'Set password on EXEC mode']

# console and vty lines section
    for line in global_params['line']:
        results_dict['line'][line] = {}
        if 'log_sync' in global_params['line'][line]:
            if global_params['line'][line]['log_sync'] == 'yes':
                results_dict['line'][line]['log_sync'] = [2,'ENABLED']
            else:
                results_dict['line'][line]['log_sync'] = [1,'DISABLED', 'You may want to enable it to prevent command'
                                                                        'typing interrupt']
        if 'exec_timeout' in global_params['line'][line]:
            if   0  < global_params['line'][line]['exec_timeout'] < 15:
                results_dict['line'][line]['exec_timeout'] = [2, 'Exec-timeout is ' +
                                                              str(global_params['line'][line]['exec_timeout'])]
            elif 15 < global_params['line'][line]['exec_timeout'] <= 30:
                results_dict['line'][line]['exec_timeout'] = [1, 'Exec-timeout is ' +
                                                              str(global_params['line'][line]['exec_timeout']),
                                                              'You may want to decrease it']
            elif      global_params['line'][line]['exec_timeout'] > 30:
                results_dict['line'][line]['exec_timeout'] = [0, 'Exec-timeout is ' +
                                                              str(global_params['line'][line]['exec_timeout']),
                                                              'Decrease it due to security reasons']
            elif      global_params['line'][line]['exec_timeout'] == 0:
                results_dict['line'][line]['exec_timeout'] = [0, 'Exec-timeout is ' +
                                                              str(global_params['line'][line]['exec_timeout']),
                                                              'Turn on exec timeout for this console']
        if 'privilege' in global_params['line'][line]:
            if global_params['line'][line]['privilege'] == '15':
                results_dict['line'][line]['privilege'] = [1, 'High privilege level',
                                                            'You may want to decrease it']
        if 'transp_in' in global_params['line'][line]:
            if global_params['line'][line]['transp_in'] == 'ssh':
                results_dict['line'][line]['transp_in'] = [2, 'SSH only']
            else:
                results_dict['line'][line]['transp_in'] = [1, 'Not SSH only',
                                                            'You may want to turn ssh only connection on']
        if 'transp_out' in global_params['line'][line]:
            if global_params['line'][line]['transp_out'] == 'ssh':
                results_dict['line'][line]['transp_out'] = [2, 'SSH only']
            else:
                results_dict['line'][line]['transp_out'] = [1, 'Not SSH only',
                                                            'You may want to turn ssh only connection on']

    return results_dict
