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
        if global_params['enable_password'] == '5':
            results_dict['enable_password'] = [2, 'Encrypted with MD5']
        else:
            results_dict['enable_password'] = [0, 'Weak encryption', 'Change encryption type to MD5']

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
            if        global_params['line'][line]['exec_timeout'] < 15:
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
