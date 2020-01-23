# Console and vty options check
# Input:
#        global dictionary with defined 'line' key inside it
# Output:
#        lines options dictionary
def check(global_params):
# create new 'Lines' section for further display
    results_dict = {'Lines':{}}


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
                    results_dict['Lines'][line]['privilege level']  = [1, '15', 'You may want to decrease it']

            if 'transp_in'    in global_params['line'][line]:
                if   global_params['line'][line]['transp_in'] == 'ssh':
                    results_dict['Lines'][line]['inbound protocol'] = [2, 'SSH']
                elif global_params['line'][line]['transp_in'] == 'none':
                    results_dict['Lines'][line]['inbound protocol'] = [2, 'NONE']
                else:
                    results_dict['Lines'][line]['inbound protocol'] = [1, 'INSECURE', 'You may want to turn ssh only connection on or disable it']

        if 'transp_out'       in global_params['line'][line]:
            if   global_params['line'][line]['transp_out'] == 'ssh':
                results_dict['Lines'][line]['outbound protocol']    = [2, 'SSH']
            elif global_params['line'][line]['transp_out'] == 'none':
                results_dict['Lines'][line]['outbound protocol']    = [2, 'NONE']
            else:
                results_dict['Lines'][line]['outbound protocol']    = [1, 'INSECURE', 'You may want to turn ssh only connection on or disable it']


    return results_dict
