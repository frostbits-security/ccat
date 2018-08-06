# SSH and global IP options check
# Input:
#        global dictionary with defined dictionaries inside it: global_params = {'ip':{'ssh': {}, 'active service': {}}
#        config result dictionary
# Output:
#        updated result dictionary
#

def check(global_params,results_dict):
# ssh section
    if 'version' in global_params['ip']['ssh']:
        if global_params['ip']['ssh']['version'] == '2':
            results_dict['ip']['ssh']['version'] = [2, 'Version 2']
        else:
            results_dict['ip']['ssh']['version'] = [1, 'Version 2 is disabled',
                                                    'You may want to turn it on']
    if 'authentication-retries' in global_params['ip']['ssh']:
        if int(global_params['ip']['ssh']['authentication-retries']) > 5:
            results_dict['ip']['ssh']['authentication-retries'] = [1, 'Authentication retries number is '
                                                            + str(global_params['ip']['ssh']['authentication-retries']),
                                                            'You may want to decrease it']
        else:
            results_dict['ip']['ssh']['authentication-retries'] = [2, 'Authentication retries number is '
                                                            + str(global_params['ip']['ssh']['authentication-retries'])]

    if 'time-out' in global_params['ip']['ssh']:
        if         int(global_params['ip']['ssh']['time-out']) < 100:
            results_dict['ip']['ssh']['time-out'] = [2, 'Timeout is ' + str(global_params['ip']['ssh']['time-out'])]
        elif 100 < int(global_params['ip']['ssh']['time-out']) <= 300:
            results_dict['ip']['ssh']['time-out'] = [1, 'Timeout is ' + str(global_params['ip']['ssh']['time-out']),
                                                     'You may want to decrease it']
        elif       int(global_params['ip']['ssh']['time-out']) > 300:
            results_dict['ip']['ssh']['time-out'] = [0, 'Timeout is ' + str(global_params['ip']['ssh']['time-out']),
                                                     'Decrease it due to security reasons']

# ip options section
    if 'finger' in global_params['ip']['active_service']:
        results_dict['ip']['active_service']['finger'] = [0, 'ENABLED',
                                                          'Disable it to prevent user to view other active users']
    else:
        results_dict['ip']['active_service']['finger'] = [2, 'DISABLED']

    if 'identd' in global_params['ip']['active_service']:
        results_dict['ip']['active_service']['identd'] = [0, 'ENABLED',
                                                          'Disable it to prevent user connection information leaks']
    else:
        results_dict['ip']['active_service']['identd'] = [2, 'DISABLED']

    if 'source-route' in global_params['ip']['active_service']:
        results_dict['ip']['active_service']['source-route'] = [0, 'ENABLED',
                                                                'Disable it to prevent packet route leak']
    else:
        results_dict['ip']['active_service']['source-route'] = [2, 'DISABLED']

    if 'bootp server' in global_params['ip']['active_service']:
        results_dict['ip']['active_service']['bootp_server'] = [0, 'ENABLED',
                                                                'Disable it to prevent possible IOS image stealing']
    else:
        results_dict['ip']['active_service']['bootp_server'] = [2, 'DISABLED']

    if 'http server' in global_params['ip']['active_service']:
        results_dict['ip']['active_service']['http_server'] = [0, 'ENABLED',
                                                               'Disable it to prevent unsecure connection. You may turn'
                                                               'on secure server with "ip http secure-server" command']
    else:
        results_dict['ip']['active_service']['http_server'] = [2, 'DISABLED']

    return results_dict
