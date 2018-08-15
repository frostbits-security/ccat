# Console and vty options check
# Input:
#        global dictionary with defined 'line' and 'enable_password' keys inside it
# Output:
#        lines and EXEC password options dictionary
def check(global_params):
# create new 'EXEC password' and 'Lines' sections for further display
    results_dict = {'EXEC password':{},'Lines':{}}


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


# lines section
    for line in global_params['line']:

    # create new dictionary for next line
        results_dict['Lines'][line] = {}
        if 'log_sync'         in global_params['line'][line]:
            if global_params['line'][line]['log_sync'] == 'yes':
                results_dict['Lines'][line]['logging synchronous']  = [2,'ENABLED']
            else:
                results_dict['Lines'][line]['logging synchronous']  = [1,'DISABLED', 'You may want to enable it to prevent command typing interrupt']

        if global_params['line'][line]['no_exec'] == 'yes':
            results_dict['Lines'][line]['inbound connection']       = [2, 'CLOSED']
        else:
            if 'exec_timeout' in global_params['line'][line]:
                if   0  < global_params['line'][line]['exec_timeout'] < 15:
                    results_dict['Lines'][line]['exec timeout']     = [2, str(global_params['line'][line]['exec_timeout'])]
                elif 15 < global_params['line'][line]['exec_timeout'] <= 30:
                    results_dict['Lines'][line]['exec timeout']     = [1, str(global_params['line'][line]['exec_timeout']), 'You may want to decrease it']
                elif      global_params['line'][line]['exec_timeout'] > 30:
                    results_dict['Lines'][line]['exec timeout']     = [0, str(global_params['line'][line]['exec_timeout']), 'Decrease it due to security reasons']
                elif      global_params['line'][line]['exec_timeout'] == 0:
                    results_dict['Lines'][line]['exec timeout']     = [0, str(global_params['line'][line]['exec_timeout']), 'Turn on exec timeout for this console']

            if 'privilege'    in global_params['line'][line]:
                if global_params['line'][line]['privilege'] == '15':
                    results_dict['Lines'][line]['privilege level']  = [1, 'High privilege level', 'You may want to decrease it']

            if 'transp_in'    in global_params['line'][line]:
                if   global_params['line'][line]['transp_in'] == 'ssh':
                    results_dict['Lines'][line]['inbound protocol'] = [2, 'SSH']
                elif global_params['line'][line]['transp_in'] == 'none':
                    results_dict['Lines'][line]['inbound protocol'] = [2, 'NONE']
                else:
                    results_dict['Lines'][line]['inbound protocol'] = [1, 'UNSECURE', 'You may want to turn ssh only connection on or disable it']

        if 'transp_out'       in global_params['line'][line]:
            if   global_params['line'][line]['transp_out'] == 'ssh':
                results_dict['Lines'][line]['outbound protocol']    = [2, 'SSH']
            elif global_params['line'][line]['transp_out'] == 'none':
                results_dict['Lines'][line]['outbound protocol']    = [2, 'NONE']
            else:
                results_dict['Lines'][line]['outbound protocol']    = [1, 'UNSECURE', 'You may want to turn ssh only connection on or disable it']


    return results_dict
